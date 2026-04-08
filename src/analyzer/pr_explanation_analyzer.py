"""
PR change explanation analyzer for summarizing changed and created files.
"""

import json
import os
import re
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional


DEFAULT_SUPPORTED_EXTENSIONS = {'.java', '.ts', '.tsx', '.scss'}
DEFAULT_EXCLUDED_DIRECTORIES = {
    '.git',
    '.hg',
    '.svn',
    '.idea',
    '.next',
    '.nuxt',
    '.turbo',
    '.cache',
    'node_modules',
    'dist',
    'build',
    'coverage',
    'target',
    'out',
    '__pycache__'
}


class PRExplanationAnalyzer:
    """Generate point-based PR explanations using deterministic heuristics."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.explanation_config = self.config.get('pr_explanation', {})
        configured_extensions = self.explanation_config.get('include_extensions')
        configured_exclusions = self.explanation_config.get('exclude_directories')
        self.supported_extensions = set(configured_extensions or DEFAULT_SUPPORTED_EXTENSIONS)
        self.excluded_directories = set(configured_exclusions or DEFAULT_EXCLUDED_DIRECTORIES)
        self.max_summary_points = self.explanation_config.get('max_summary_points', 5)
        self.max_file_points = self.explanation_config.get('max_file_points', 4)
        self.provider = self.explanation_config.get('provider', 'heuristic')
        self.ollama_model = self.explanation_config.get('model', 'qwen2.5-coder:1.5b')
        self.ollama_base_url = self.explanation_config.get('base_url', 'http://127.0.0.1:11434')
        self.fallback_to_heuristic = self.explanation_config.get('fallback_to_heuristic', True)
        self.ollama_timeout_seconds = self.explanation_config.get('timeout_seconds', 120)

    def analyze(self,
                changed_files: List[Dict[str, Any]],
                pr_title: str = "",
                pr_description: str = "") -> Dict[str, Any]:
        """Analyze changed/created files and produce PR-level explanation."""
        relevant_files = [
            file_info for file_info in changed_files
            if self._should_explain(file_info)
        ]

        file_explanations = [
            self._explain_file(file_info, pr_title, pr_description)
            for file_info in relevant_files
        ]

        return {
            'enabled': self.explanation_config.get('enabled', True),
            'pr_title': pr_title,
            'pr_description': pr_description,
            'total_files_considered': len(relevant_files),
            'files': file_explanations,
            'summary': self._build_summary(file_explanations, pr_title, pr_description)
        }

    def analyze_project_files(self,
                              project_root: str,
                              pr_title: str = "",
                              pr_description: str = "") -> Dict[str, Any]:
        """Build file metadata from a local project and generate explanation."""
        changed_files = []

        for root, dirs, files in os.walk(project_root):
            dirs[:] = [
                dir_name for dir_name in dirs
                if dir_name not in self.excluded_directories
            ]

            for file_name in files:
                file_path = os.path.join(root, file_name)
                extension = Path(file_path).suffix.lower()
                if extension not in self.supported_extensions:
                    continue

                try:
                    with open(file_path, 'r', encoding='utf-8') as file_handle:
                        content = file_handle.read()
                except Exception:
                    continue

                changed_files.append({
                    'path': file_path,
                    'content': content,
                    'diff': '',
                    'change_type': 'modified',
                    'additions': self._estimate_additions(content),
                    'deletions': 0
                })

        return self.analyze(changed_files, pr_title, pr_description)

    def _should_explain(self, file_info: Dict[str, Any]) -> bool:
        """Determine if file should be included in explanation analysis."""
        path = file_info.get('path', '')
        extension = Path(path).suffix.lower()

        if extension not in self.supported_extensions:
            return False

        path_parts = set(Path(path).parts)
        if path_parts.intersection(self.excluded_directories):
            return False

        return True

    def _explain_file(self,
                      file_info: Dict[str, Any],
                      pr_title: str,
                      pr_description: str) -> Dict[str, Any]:
        """Create explanation points for a single file."""
        file_path = file_info.get('path', '')
        content = file_info.get('content', '') or ''
        diff = file_info.get('diff', '') or ''
        change_type = file_info.get('change_type', 'modified')
        language = self._detect_language(file_path)

        heuristic_result = self._build_heuristic_file_explanation(
            file_path=file_path,
            content=content,
            diff=diff,
            change_type=change_type,
            language=language,
            pr_title=pr_title,
            pr_description=pr_description
        )

        if self.provider != 'ollama':
            return heuristic_result

        llm_result = self._build_ollama_file_explanation(
            file_path=file_path,
            content=content,
            diff=diff,
            change_type=change_type,
            language=language,
            pr_title=pr_title,
            pr_description=pr_description,
            heuristic_result=heuristic_result
        )

        if llm_result:
            return llm_result

        return heuristic_result

    def _build_summary(self,
                       file_explanations: List[Dict[str, Any]],
                       pr_title: str,
                       pr_description: str) -> Dict[str, List[str]]:
        """Aggregate all file explanations into PR-level bullets."""
        languages = Counter(file_info['language'] for file_info in file_explanations)
        change_types = Counter(file_info['change_type'] for file_info in file_explanations)

        what_changed = []
        if pr_title.strip():
            what_changed.append(f"PR focus: {pr_title.strip()}")

        if file_explanations:
            what_changed.append(
                f"Updated {len(file_explanations)} supported files across "
                f"{', '.join(f'{count} {language}' for language, count in languages.items())}."
            )

        if change_types:
            what_changed.append(
                "Change mix: " +
                ", ".join(f"{count} {change_type}" for change_type, count in change_types.items()) + "."
            )

        repeated_themes = self._collect_common_points(
            file_explanations,
            'what_changed',
            limit=self.max_summary_points
        )
        why_changed = self._collect_common_points(
            file_explanations,
            'why_changed',
            limit=self.max_summary_points
        )
        impact = self._collect_common_points(
            file_explanations,
            'integration_impact',
            limit=self.max_summary_points
        )

        if pr_description.strip():
            why_changed.insert(0, f"PR description context: {pr_description.strip()}")

        if not repeated_themes:
            repeated_themes = ["Code changes are localized and require file-level review for detail."]
        if not why_changed:
            why_changed = ["Intent inferred from file names, structure, and code patterns."]
        if not impact:
            impact = ["Review integration points and runtime behavior for touched modules."]

        return {
            'what_changed': (what_changed + repeated_themes)[:self.max_summary_points],
            'why_changed': why_changed[:self.max_summary_points],
            'impact': impact[:self.max_summary_points]
        }

    def _build_heuristic_file_explanation(self,
                                          file_path: str,
                                          content: str,
                                          diff: str,
                                          change_type: str,
                                          language: str,
                                          pr_title: str,
                                          pr_description: str) -> Dict[str, Any]:
        """Build deterministic file explanation."""
        structural_points = self._extract_structural_points(file_path, content)
        intent_points = self._infer_why_points(
            file_path=file_path,
            content=content,
            diff=diff,
            pr_title=pr_title,
            pr_description=pr_description
        )
        integration_points = self._infer_integration_points(content)
        risk_points = self._infer_risk_points(file_path, content)

        return {
            'file': file_path,
            'change_type': change_type,
            'language': language,
            'overview': self._build_file_overview(file_path, change_type, structural_points),
            'what_changed': structural_points,
            'why_changed': intent_points,
            'integration_impact': integration_points,
            'considerations': risk_points,
            'provider': 'heuristic'
        }

    def _build_file_overview(self,
                             file_path: str,
                             change_type: str,
                             structural_points: List[str]) -> str:
        """Generate a one-line overview for the file."""
        if structural_points:
            return f"{change_type.title()} {Path(file_path).name}: {structural_points[0]}"
        return f"{change_type.title()} {Path(file_path).name} with no strong structural signal detected."

    def _extract_structural_points(self, file_path: str, content: str) -> List[str]:
        """Infer concrete changes from code structure."""
        extension = Path(file_path).suffix.lower()
        points: List[str] = []

        if extension == '.tsx':
            components = re.findall(r'function\s+([A-Z][A-Za-z0-9_]*)\s*\(', content)
            components += re.findall(r'const\s+([A-Z][A-Za-z0-9_]*)\s*[:=]', content)
            for component_name in self._dedupe(components)[:3]:
                points.append(f"Defines or updates React component `{component_name}`.")

            hooks = re.findall(r'\buse(State|Effect|Memo|Callback|Ref)\b', content)
            for hook_name in self._dedupe([f"use{hook}" for hook in hooks])[:3]:
                points.append(f"Uses React hook `{hook_name}` to manage component behavior.")

            jsx_tags = re.findall(r'<([A-Z][A-Za-z0-9_]*)\b', content)
            for tag in self._dedupe(jsx_tags)[:3]:
                points.append(f"Composes UI using child component `{tag}`.")

        elif extension == '.ts':
            exports = re.findall(r'export\s+(?:async\s+)?(?:function|const|class|interface|type)\s+([A-Za-z_]\w*)', content)
            for export_name in self._dedupe(exports)[:4]:
                points.append(f"Adds or updates exported TypeScript member `{export_name}`.")

            api_calls = re.findall(r'\b(fetch|axios\.\w+)\b', content)
            for api_call in self._dedupe(api_calls)[:2]:
                points.append(f"Performs external data access using `{api_call}`.")

        elif extension == '.java':
            classes = re.findall(r'\bclass\s+([A-Z][A-Za-z0-9_]*)', content)
            for class_name in self._dedupe(classes)[:3]:
                points.append(f"Defines or updates Java class `{class_name}`.")

        elif extension == '.scss':
            selectors = re.findall(r'^\s*([.#]?[a-zA-Z_-][\w\-]*(?:\s+[.#]?[a-zA-Z_-][\w\-]*)*)\s*\{', content, re.MULTILINE)
            for selector in self._dedupe(selectors)[:4]:
                points.append(f"Adjusts styling rules for selector `{selector.strip()}`.")

        imports = re.findall(r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]', content)
        for imported in self._dedupe(imports)[:3]:
            points.append(f"Depends on module `{imported}`.")

        return (points or ["Touches file content without a strong language-specific structural match."])[:self.max_file_points]

    def _infer_why_points(self,
                          file_path: str,
                          content: str,
                          diff: str,
                          pr_title: str,
                          pr_description: str) -> List[str]:
        """Infer likely purpose behind the change."""
        text = " ".join([file_path, content[:1500], diff[:1500], pr_title, pr_description]).lower()
        points: List[str] = []

        if any(keyword in text for keyword in ['fix', 'bug', 'issue', 'error', 'regression']):
            points.append("Appears intended to fix an existing bug, issue, or unstable behavior.")

        if any(keyword in text for keyword in ['feature', 'enhancement', 'add', 'create', 'introduce']):
            points.append("Appears to introduce or extend user-facing functionality.")

        if any(keyword in text for keyword in ['refactor', 'cleanup', 'simplify', 'maintain']):
            points.append("Appears focused on maintainability or code structure improvement.")

        if any(keyword in text for keyword in ['style', 'scss', 'ui', 'layout', 'theme', 'responsive']):
            points.append("Appears intended to improve visual presentation or frontend usability.")

        if any(keyword in text for keyword in ['api', 'service', 'fetch', 'data', 'request']):
            points.append("Appears intended to improve data flow, service integration, or API usage.")

        if any(keyword in text for keyword in ['performance', 'optimize', 'memo', 'cache']):
            points.append("Appears intended to improve runtime performance or reduce repeated work.")

        if not points:
            points.append("Intent is inferred from file structure and naming because explicit rationale is limited.")

        return points[:self.max_file_points]

    def _infer_integration_points(self, content: str) -> List[str]:
        """Infer dependencies and integration impact."""
        points: List[str] = []

        imports = re.findall(r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]', content)
        for imported in self._dedupe(imports)[:4]:
            points.append(f"Integrates with imported module `{imported}`.")

        if 'useState' in content or 'useEffect' in content:
            points.append("Affects component state lifecycle and render behavior.")

        if any(token in content for token in ['fetch(', 'axios.', 'Promise', 'async ', 'await ']):
            points.append("Touches asynchronous behavior or remote data interactions.")

        if re.search(r'className\s*=', content) and re.search(r'import\s+[\'"].*\.scss[\'"]', content):
            points.append("Links component structure with SCSS-based presentation.")

        return (points or ["No major integration signal detected beyond local file logic."])[:self.max_file_points]

    def _infer_risk_points(self, file_path: str, content: str) -> List[str]:
        """Infer review considerations for the file."""
        extension = Path(file_path).suffix.lower()
        points: List[str] = []

        if 'dangerouslySetInnerHTML' in content:
            points.append("Review HTML injection safety and sanitization assumptions.")

        if 'eval(' in content:
            points.append("Review dynamic code execution risk carefully.")

        if extension in {'.ts', '.tsx'} and 'any' in content:
            points.append("Review type safety because loose typing may hide runtime issues.")

        if extension == '.scss':
            points.append("Validate visual regressions, responsive layout behavior, and selector scope.")

        if extension == '.tsx':
            points.append("Validate render flow, props wiring, and state update behavior.")

        if any(token in content for token in ['fetch(', 'axios.', 'async ', 'await ']):
            points.append("Validate error handling, loading states, and backend contract assumptions.")

        return (points or ["No specific high-risk consideration inferred; perform normal functional review."])[:self.max_file_points]

    def _build_ollama_file_explanation(self,
                                       file_path: str,
                                       content: str,
                                       diff: str,
                                       change_type: str,
                                       language: str,
                                       pr_title: str,
                                       pr_description: str,
                                       heuristic_result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Build file explanation using Ollama, with heuristic fallback handled by caller."""
        prompt = self._build_ollama_prompt(
            file_path=file_path,
            content=content,
            diff=diff,
            change_type=change_type,
            language=language,
            pr_title=pr_title,
            pr_description=pr_description,
            heuristic_result=heuristic_result
        )
        response_text = self._call_ollama(prompt)
        if not response_text:
            return None

        parsed = self._parse_ollama_response(response_text)
        if not parsed:
            return None

        return {
            'file': file_path,
            'change_type': change_type,
            'language': language,
            'overview': parsed.get('overview') or heuristic_result['overview'],
            'what_changed': self._truncate_points(parsed.get('what_changed'), heuristic_result['what_changed']),
            'why_changed': self._truncate_points(parsed.get('why_changed'), heuristic_result['why_changed']),
            'integration_impact': self._truncate_points(
                parsed.get('integration_impact'),
                heuristic_result['integration_impact']
            ),
            'considerations': self._truncate_points(parsed.get('considerations'), heuristic_result['considerations']),
            'provider': 'ollama'
        }

    def _build_ollama_prompt(self,
                             file_path: str,
                             content: str,
                             diff: str,
                             change_type: str,
                             language: str,
                             pr_title: str,
                             pr_description: str,
                             heuristic_result: Dict[str, Any]) -> str:
        """Build constrained prompt for Ollama."""
        trimmed_content = content[:4000]
        trimmed_diff = diff[:2000]

        return f"""You are generating a concise PR code explanation for reviewers.

Return only valid JSON with this exact shape:
{{
  "overview": "single sentence",
  "what_changed": ["bullet", "bullet"],
  "why_changed": ["bullet", "bullet"],
  "integration_impact": ["bullet", "bullet"],
  "considerations": ["bullet", "bullet"]
}}

Rules:
- Output JSON only. No markdown fences.
- Keep each list to at most {self.max_file_points} bullets.
- Keep bullets concise, factual, reviewer-friendly.
- Use the PR title/description when useful.
- Do not invent behavior not supported by file content, diff, path, or heuristic hints.
- If uncertain, stay conservative.

Context:
PR title: {pr_title}
PR description: {pr_description}
File path: {file_path}
Change type: {change_type}
Language: {language}

Heuristic hints:
{json.dumps({
    "overview": heuristic_result.get("overview", ""),
    "what_changed": heuristic_result.get("what_changed", []),
    "why_changed": heuristic_result.get("why_changed", []),
    "integration_impact": heuristic_result.get("integration_impact", []),
    "considerations": heuristic_result.get("considerations", [])
}, ensure_ascii=False)}

Diff excerpt:
{trimmed_diff if trimmed_diff else "(no diff provided)"}

File content excerpt:
{trimmed_content}
"""

    def _call_ollama(self, prompt: str) -> Optional[str]:
        """Call Ollama generate API and return response text."""
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
        """Parse Ollama JSON response with light cleanup."""
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

    def _truncate_points(self,
                         llm_points: Optional[List[str]],
                         fallback_points: List[str]) -> List[str]:
        """Normalize and truncate explanation bullets."""
        if not isinstance(llm_points, list):
            return fallback_points[:self.max_file_points]

        normalized = [
            str(point).strip() for point in llm_points
            if str(point).strip()
        ]
        if not normalized:
            return fallback_points[:self.max_file_points]

        return normalized[:self.max_file_points]

    def _collect_common_points(self,
                               file_explanations: List[Dict[str, Any]],
                               key: str,
                               limit: int = 5) -> List[str]:
        """Collect common bullets across files while preserving order."""
        collected: List[str] = []
        seen = set()

        for file_info in file_explanations:
            for point in file_info.get(key, []):
                if point not in seen:
                    seen.add(point)
                    collected.append(point)
                    if len(collected) >= limit:
                        return collected

        return collected

    def _detect_language(self, file_path: str) -> str:
        """Map file extension to display language."""
        extension = Path(file_path).suffix.lower()
        return {
            '.java': 'java',
            '.ts': 'typescript',
            '.tsx': 'tsx',
            '.scss': 'scss'
        }.get(extension, 'text')

    def _estimate_additions(self, content: str) -> int:
        """Estimate additions for local file-only analysis."""
        return len([line for line in content.splitlines() if line.strip()])

    def _dedupe(self, values: List[str]) -> List[str]:
        """Return ordered unique values."""
        seen = set()
        result = []

        for value in values:
            if value not in seen:
                seen.add(value)
                result.append(value)

        return result


# Made with Bob