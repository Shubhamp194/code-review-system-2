"""
Design recommendation analyzer for PR-only changes using Ollama with heuristic fallback.
"""

import json
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional


DEFAULT_SUPPORTED_EXTENSIONS = {'.java', '.ts', '.tsx', '.scss'}


class PRDesignRecommendationAnalyzer:
    """Recommend language-level design patterns for changed files."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.design_config = self.config.get('pr_design_recommendation', {})
        self.supported_extensions = set(
            self.design_config.get('include_extensions', DEFAULT_SUPPORTED_EXTENSIONS)
        )
        self.provider = self.design_config.get('provider', 'ollama')
        self.ollama_model = self.design_config.get('model', 'qwen2.5-coder:1.5b')
        self.ollama_base_url = self.design_config.get('base_url', 'http://127.0.0.1:11434')
        self.ollama_timeout_seconds = self.design_config.get('timeout_seconds', 45)
        self.fallback_to_heuristic = self.design_config.get('fallback_to_heuristic', True)
        self.max_recommendations_per_file = self.design_config.get('max_recommendations_per_file', 3)

    def analyze(self,
                changed_files: List[Dict[str, Any]],
                pr_title: str = "",
                pr_description: str = "") -> Dict[str, Any]:
        """Analyze changed files for design-pattern recommendations."""
        relevant_files = [
            file_info for file_info in changed_files
            if Path(file_info.get('path', '')).suffix.lower() in self.supported_extensions
        ]

        recommendations: List[Dict[str, Any]] = []
        for file_info in relevant_files:
            if self.provider == 'ollama':
                ollama_recommendations = self._recommend_with_ollama(file_info, pr_title, pr_description)
                if ollama_recommendations is not None:
                    recommendations.extend(ollama_recommendations)
                    continue

            recommendations.extend(self._recommend_with_heuristics(file_info))

        return {
            'enabled': self.design_config.get('enabled', True),
            'provider': self.provider,
            'non_blocking': True,
            'pr_title': pr_title,
            'pr_description': pr_description,
            'total_files_considered': len(relevant_files),
            'recommendations': recommendations
        }

    def _recommend_with_heuristics(self, file_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Deterministic fallback design recommendations."""
        path = file_info.get('path', '')
        content = file_info.get('content', '')
        extension = Path(path).suffix.lower()

        recommendations: List[Dict[str, Any]] = []

        if extension == '.java':
            if 'new ' in content and 'if (' in content and 'switch' not in content:
                recommendations.append({
                    'file': path,
                    'pattern': 'Factory Pattern',
                    'current_approach': 'Direct object creation mixed with branching logic',
                    'recommendation': 'Consider a Factory pattern to centralize object creation and reduce conditional instantiation logic.',
                    'why_it_helps': [
                        'Improves extensibility when new object types are added',
                        'Keeps construction logic out of business flows'
                    ],
                    'alternatives': ['Strategy Pattern'],
                    'provider': 'heuristic'
                })

            if re.search(r'static\s+\w+\s+\w+\s*;', content) and re.search(r'getInstance\s*\(', content):
                recommendations.append({
                    'file': path,
                    'pattern': 'Singleton Pattern Review',
                    'current_approach': 'Singleton-style access pattern appears present',
                    'recommendation': 'Validate whether Singleton is truly required or if dependency injection would provide better testability and lifecycle control.',
                    'why_it_helps': [
                        'Avoids hidden shared state',
                        'Improves test isolation and flexibility'
                    ],
                    'alternatives': ['Dependency Injection'],
                    'provider': 'heuristic'
                })

        if extension in {'.ts', '.tsx'}:
            if re.search(r'if\s*\([^)]+\)\s*\{[\s\S]{0,500}return', content) and content.count('if (') >= 3:
                recommendations.append({
                    'file': path,
                    'pattern': 'Strategy Pattern',
                    'current_approach': 'Conditional-heavy branching appears in frontend logic',
                    'recommendation': 'Consider Strategy pattern or a mapping-based dispatch to reduce large conditional flows.',
                    'why_it_helps': [
                        'Makes behavior easier to extend',
                        'Improves readability and targeted testing'
                    ],
                    'alternatives': ['Lookup Map', 'Polymorphic Handlers'],
                    'provider': 'heuristic'
                })

            if 'useState' in content and content.count('useState') >= 3:
                recommendations.append({
                    'file': path,
                    'pattern': 'Reducer Pattern',
                    'current_approach': 'Component appears to manage multiple related local states with useState',
                    'recommendation': 'Consider consolidating related state transitions with useReducer for clearer event-driven state management.',
                    'why_it_helps': [
                        'Groups related transitions in one place',
                        'Reduces scattered setter logic'
                    ],
                    'alternatives': ['Custom Hook'],
                    'provider': 'heuristic'
                })

            if re.search(r'fetch\(|axios\.', content):
                recommendations.append({
                    'file': path,
                    'pattern': 'Service Layer',
                    'current_approach': 'Network access appears directly inside component or feature logic',
                    'recommendation': 'Consider moving API interaction into a service layer or custom hook to separate UI from data-access concerns.',
                    'why_it_helps': [
                        'Improves reusability and testability',
                        'Keeps presentation logic focused on rendering'
                    ],
                    'alternatives': ['Repository Pattern', 'Custom Hook'],
                    'provider': 'heuristic'
                })

        return recommendations[:self.max_recommendations_per_file]

    def _recommend_with_ollama(self,
                               file_info: Dict[str, Any],
                               pr_title: str,
                               pr_description: str) -> Optional[List[Dict[str, Any]]]:
        """Use Ollama to recommend design patterns or alternatives."""
        prompt = self._build_prompt(file_info, pr_title, pr_description)
        response_text = self._call_ollama(prompt)
        if not response_text:
            return None

        parsed = self._parse_ollama_response(response_text)
        if parsed is None:
            return None

        recommendations = parsed.get('recommendations', [])
        if not isinstance(recommendations, list):
            return []

        normalized_recommendations: List[Dict[str, Any]] = []
        for recommendation in recommendations[:self.max_recommendations_per_file]:
            if not isinstance(recommendation, dict):
                continue
            normalized_recommendations.append({
                'file': file_info.get('path', ''),
                'pattern': str(recommendation.get('pattern', 'Design Pattern Recommendation')).strip(),
                'current_approach': str(recommendation.get('current_approach', '')).strip(),
                'recommendation': str(recommendation.get('recommendation', '')).strip(),
                'why_it_helps': self._normalize_list(recommendation.get('why_it_helps')),
                'alternatives': self._normalize_list(recommendation.get('alternatives')),
                'provider': 'ollama'
            })

        return normalized_recommendations

    def _build_prompt(self,
                      file_info: Dict[str, Any],
                      pr_title: str,
                      pr_description: str) -> str:
        """Build constrained design-recommendation prompt."""
        file_path = file_info.get('path', '')
        content = (file_info.get('content', '') or '')[:5000]
        diff = (file_info.get('diff', '') or '')[:2500]
        change_type = file_info.get('change_type', 'modified')

        return f"""You are reviewing only the changed code in a pull request to recommend software design patterns or better design alternatives used in programming languages.

Focus on patterns such as Singleton, Factory, Strategy, Builder, Observer, Adapter, Facade, Template Method, Repository, Service Layer, Reducer pattern, composition over inheritance, or dependency injection where relevant.

Return only valid JSON with this exact shape:
{{
  "recommendations": [
    {{
      "pattern": "recommended pattern name",
      "current_approach": "brief description of current design approach",
      "recommendation": "concise recommendation",
      "why_it_helps": ["benefit 1", "benefit 2"],
      "alternatives": ["alternative 1", "alternative 2"]
    }}
  ]
}}

Rules:
- Output JSON only. No markdown.
- Focus only on code evidence in this changed file.
- Recommend only language/software design patterns or structural coding patterns.
- If an existing pattern appears questionable, suggest a better alternative.
- Be conservative. Do not force a pattern where none is justified.
- If no meaningful design recommendation is suggested, return {{"recommendations": []}}.

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