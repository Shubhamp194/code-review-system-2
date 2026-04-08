"""
Potential defect detector for PR-only changes using Ollama with heuristic fallback.
"""

import json
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional


DEFAULT_SUPPORTED_EXTENSIONS = {'.java', '.ts', '.tsx', '.scss'}


class PRDefectDetector:
    """Detect likely defects introduced by changed files."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.detector_config = self.config.get('pr_defect_detection', {})
        self.supported_extensions = set(
            self.detector_config.get('include_extensions', DEFAULT_SUPPORTED_EXTENSIONS)
        )
        self.provider = self.detector_config.get('provider', 'ollama')
        self.ollama_model = self.detector_config.get('model', 'qwen2.5-coder:1.5b')
        self.ollama_base_url = self.detector_config.get('base_url', 'http://127.0.0.1:11434')
        self.ollama_timeout_seconds = self.detector_config.get('timeout_seconds', 45)
        self.fallback_to_heuristic = self.detector_config.get('fallback_to_heuristic', True)
        self.max_findings_per_file = self.detector_config.get('max_findings_per_file', 3)

    def analyze(self,
                changed_files: List[Dict[str, Any]],
                pr_title: str = "",
                pr_description: str = "") -> Dict[str, Any]:
        """Analyze changed files for likely defects."""
        relevant_files = [
            file_info for file_info in changed_files
            if Path(file_info.get('path', '')).suffix.lower() in self.supported_extensions
        ]

        findings: List[Dict[str, Any]] = []
        for file_info in relevant_files:
            if self.provider == 'ollama':
                ollama_findings = self._detect_with_ollama(file_info, pr_title, pr_description)
                if ollama_findings is not None:
                    findings.extend(ollama_findings)
                    continue

            findings.extend(self._detect_with_heuristics(file_info))

        return {
            'enabled': self.detector_config.get('enabled', True),
            'provider': self.provider,
            'non_blocking': True,
            'pr_title': pr_title,
            'pr_description': pr_description,
            'total_files_considered': len(relevant_files),
            'findings': findings
        }

    def _detect_with_heuristics(self, file_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Deterministic fallback defect detection."""
        path = file_info.get('path', '')
        content = file_info.get('content', '')
        extension = Path(path).suffix.lower()

        findings: List[Dict[str, Any]] = []

        if extension in {'.ts', '.tsx'}:
            if re.search(r'<form\b', content, re.IGNORECASE):
                has_validation = any(
                    token in content for token in ['required', 'pattern=', 'validate', 'zod', 'yup']
                )
                if not has_validation:
                    findings.append({
                        'file': path,
                        'severity': 'MEDIUM',
                        'title': 'Form input validation may be missing',
                        'summary': 'A form structure appears present without obvious input validation safeguards.',
                        'potential_impacts': [
                            'Users may submit malformed or inconsistent data',
                            'Server-side validation burden may increase',
                            'Business rules may be bypassed in the UI flow'
                        ],
                        'recommendations': [
                            'Add field-level validation for required inputs and allowed formats',
                            'Validate both client-side and server-side'
                        ],
                        'provider': 'heuristic'
                    })

            if re.search(r'name\s*[:=]', content, re.IGNORECASE) and not re.search(
                r'(regex|pattern|required|minLength|maxLength|validate)', content, re.IGNORECASE
            ):
                findings.append({
                    'file': path,
                    'severity': 'LOW',
                    'title': 'Name-like field may accept invalid characters',
                    'summary': 'A name-related field appears without obvious character or format validation.',
                    'potential_impacts': [
                        'Names with numbers or special characters may be accepted unexpectedly',
                        'Downstream display or reporting quality may degrade'
                    ],
                    'recommendations': [
                        'Restrict accepted characters where business rules require alphabetic names',
                        'Add normalization and validation tests for edge-case inputs'
                    ],
                    'provider': 'heuristic'
                })

            if 'fetch(' in content or 'axios.' in content:
                if 'catch' not in content and '.catch(' not in content:
                    findings.append({
                        'file': path,
                        'severity': 'MEDIUM',
                        'title': 'Network error handling may be incomplete',
                        'summary': 'Remote call logic appears without obvious error handling paths.',
                        'potential_impacts': [
                            'Unhandled failures may break user flows',
                            'Users may not receive useful feedback during API failures'
                        ],
                        'recommendations': [
                            'Add try/catch or promise rejection handling',
                            'Define user-visible failure and retry behavior'
                        ],
                        'provider': 'heuristic'
                    })

        if extension == '.java':
            if 'new Scanner(' in content and '.close()' not in content:
                findings.append({
                    'file': path,
                    'severity': 'LOW',
                    'title': 'Resource may not be closed',
                    'summary': 'A resource allocation pattern appears without a matching close call.',
                    'potential_impacts': [
                        'Resource leakage may accumulate over time',
                        'Tests may pass while production usage degrades'
                    ],
                    'recommendations': [
                        'Use try-with-resources where possible',
                        'Ensure allocated resources are closed on all paths'
                    ],
                    'provider': 'heuristic'
                })

            if re.search(r'\bcatch\s*\(', content) and 'log.' not in content:
                findings.append({
                    'file': path,
                    'severity': 'LOW',
                    'title': 'Exception path may be hard to diagnose',
                    'summary': 'Catch handling appears present without obvious structured logging.',
                    'potential_impacts': [
                        'Operational debugging may become harder',
                        'Failure context may be lost during incidents'
                    ],
                    'recommendations': [
                        'Log exceptions with context',
                        'Add targeted tests for failure paths'
                    ],
                    'provider': 'heuristic'
                })

        return findings[:self.max_findings_per_file]

    def _detect_with_ollama(self,
                            file_info: Dict[str, Any],
                            pr_title: str,
                            pr_description: str) -> Optional[List[Dict[str, Any]]]:
        """Use Ollama to detect likely changed-code defects."""
        prompt = self._build_prompt(file_info, pr_title, pr_description)
        response_text = self._call_ollama(prompt)
        if not response_text:
            return None

        parsed = self._parse_ollama_response(response_text)
        if parsed is None:
            return None

        findings = parsed.get('findings', [])
        if not isinstance(findings, list):
            return []

        normalized_findings: List[Dict[str, Any]] = []
        for finding in findings[:self.max_findings_per_file]:
            if not isinstance(finding, dict):
                continue
            normalized_findings.append({
                'file': file_info.get('path', ''),
                'severity': str(finding.get('severity', 'MEDIUM')).upper(),
                'title': str(finding.get('title', 'Potential defect')).strip(),
                'summary': str(finding.get('summary', '')).strip(),
                'potential_impacts': self._normalize_list(finding.get('potential_impacts')),
                'recommendations': self._normalize_list(finding.get('recommendations')),
                'provider': 'ollama'
            })

        return normalized_findings

    def _build_prompt(self,
                      file_info: Dict[str, Any],
                      pr_title: str,
                      pr_description: str) -> str:
        """Build constrained defect-detection prompt."""
        file_path = file_info.get('path', '')
        content = (file_info.get('content', '') or '')[:5000]
        diff = (file_info.get('diff', '') or '')[:2500]
        change_type = file_info.get('change_type', 'modified')

        return f"""You are reviewing only the changed code in a pull request to identify likely potential defects.

Return only valid JSON with this exact shape:
{{
  "findings": [
    {{
      "severity": "LOW|MEDIUM|HIGH",
      "title": "short defect title",
      "summary": "one concise sentence",
      "potential_impacts": ["impact 1", "impact 2"],
      "recommendations": ["action 1", "action 2"]
    }}
  ]
}}

Rules:
- Output JSON only. No markdown.
- Focus on likely defects introduced or exposed by this changed file.
- Consider functional, validation, error-handling, integration, state-management, and security-adjacent defects.
- Be conservative. Do not invent issues without code evidence.
- If no meaningful defect is suggested, return {{"findings": []}}.

PR title: {pr_title}
PR description: {pr_description}
File path: {file_path}
Change type: {change_type}

Diff excerpt:
{diff if diff else "(no diff provided)"}

File content excerpt:
{content}
"""

    def _call_ollama(self, prompt: str) -> Optional[str]:
        """Call Ollama generate API."""
        payload = json.dumps({
            'model': self.ollama_model,
            'prompt': prompt,
            'stream': False
        }).encode('utf-8')
        endpoint = f"{self.ollama_base_url.rstrip('/')}/api/generate"
        request = urllib.request.Request(
            endpoint,
            data=payload,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )

        try:
            with urllib.request.urlopen(request, timeout=self.ollama_timeout_seconds) as response:
                response_data = json.loads(response.read().decode('utf-8'))
                return response_data.get('response', '').strip()
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError):
            if self.fallback_to_heuristic:
                return None
            raise

    def _parse_ollama_response(self, response_text: str) -> Optional[Dict[str, Any]]:
        """Parse JSON response from Ollama."""
        cleaned = response_text.strip()
        json_match = re.search(r'\{.*\}', cleaned, re.DOTALL)
        if json_match:
            cleaned = json_match.group(0)

        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError:
            return None

        if not isinstance(parsed, dict):
            return None

        return parsed

    def _normalize_list(self, value: Any) -> List[str]:
        """Normalize JSON array-ish values."""
        if not isinstance(value, list):
            return []
        return [str(item).strip() for item in value if str(item).strip()]


# Made with Bob