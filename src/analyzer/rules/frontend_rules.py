"""
Frontend Rules for TypeScript, TSX, and SCSS
"""

import re
from typing import List, Dict, Any
from .base import Rule, RuleViolation, PatternRule


def get_frontend_rules(config: Dict[str, List[Dict[str, Any]]]) -> List[Rule]:
    """Get frontend rules from configuration"""
    rules = []

    if 'shared' in config:
        for rule_config in config['shared']:
            rule_id = rule_config['id']
            if rule_id == 'FE001':
                rules.append(FrontendIBMLicenseHeaderRule(rule_config))
            elif rule_id == 'FE002':
                rules.append(FrontendNoHardcodedSecretsRule(rule_config))
            elif rule_id == 'FE003':
                rules.append(FrontendNoLoggingSensitiveDataRule(rule_config))
            elif rule_id == 'FE004':
                rules.append(FrontendNoTODOCommentsRule(rule_config))
            elif rule_id == 'FE005':
                rules.append(FrontendNoHardcodedURLsRule(rule_config))
            elif rule_id == 'FE006':
                rules.append(FrontendNoCommentedCodeRule(rule_config))
            elif rule_id == 'FE007':
                rules.append(FrontendNoConsoleLogRule(rule_config))
            elif rule_id == 'FE008':
                rules.append(FrontendNoDebugFlagsRule(rule_config))
            elif rule_id == 'FE009':
                rules.append(FrontendNoStringConcatInLoggingRule(rule_config))
            elif rule_id == 'FE010':
                rules.append(FrontendBooleanNamingConventionRule(rule_config))

    if 'typescript' in config:
        for rule_config in config['typescript']:
            rule_id = rule_config['id']
            if rule_id == 'TS001':
                rules.append(NoVarRule(rule_config))
            elif rule_id == 'TS002':
                rules.append(PreferConstRule(rule_config))
            elif rule_id == 'TS003':
                rules.append(UnusedVariablesRule(rule_config))
            elif rule_id == 'TS004':
                rules.append(UnusedFunctionsRule(rule_config))
            elif rule_id == 'TS005':
                rules.append(NoDebuggerRule(rule_config))
            elif rule_id == 'TS006':
                rules.append(NoExplicitAnyRule(rule_config))
            elif rule_id == 'TS007':
                rules.append(NoEvalRule(rule_config))
            elif rule_id == 'TS008':
                rules.append(NoDangerouslySetInnerHTMLRule(rule_config))
            elif rule_id == 'TS009':
                rules.append(FrontendGenericVariableNamesRule(rule_config))

    if 'tsx' in config:
        for rule_config in config['tsx']:
            rule_id = rule_config['id']
            if rule_id == 'TSX001':
                rules.append(UnusedReactStateValueRule(rule_config))
            elif rule_id == 'TSX002':
                rules.append(UnusedReactStateSetterRule(rule_config))
            elif rule_id == 'TSX003':
                rules.append(ReactStateNeverUpdatedRule(rule_config))

    if 'scss' in config:
        for rule_config in config['scss']:
            rule_id = rule_config['id']
            if rule_id == 'SCSS001':
                rules.append(NoPxRule(rule_config))
            elif rule_id == 'SCSS002':
                rules.append(NoIdSelectorsRule(rule_config))
            elif rule_id == 'SCSS003':
                rules.append(MaxNestingDepthRule(rule_config))
            elif rule_id == 'SCSS004':
                rules.append(NoHardcodedHexColorsRule(rule_config))
            elif rule_id == 'SCSS005':
                rules.append(NoEmptyScssBlocksRule(rule_config))

    return rules


class FrontendIBMLicenseHeaderRule(Rule):
    """Check for IBM license header in frontend files"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            blocking=config.get('blocking', True),
            supported_extensions=['.ts', '.tsx', '.scss']
        )
        self.required_patterns = config.get('patterns', [])

    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        first_50_lines = '\n'.join(content.split('\n')[:50])

        missing_patterns = []
        for pattern in self.required_patterns:
            if not re.search(pattern, first_50_lines, re.IGNORECASE):
                missing_patterns.append(pattern)

        if missing_patterns:
            violations.append(
                self._create_violation(
                    file_path=file_path,
                    line_number=1,
                    code_snippet=content.split('\n')[0] if content else '',
                    message=f"Missing IBM license header. Required: {', '.join(missing_patterns)}",
                    suggestion="Add IBM copyright header at the beginning of the file"
                )
            )

        return violations


class FrontendNoHardcodedSecretsRule(PatternRule):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=config.get('patterns', []),
            blocking=config.get('blocking', True),
            suggestion="Use environment variables or secure configuration for secrets",
            supported_extensions=['.ts', '.tsx']
        )


class FrontendNoLoggingSensitiveDataRule(PatternRule):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=config.get('patterns', []),
            blocking=config.get('blocking', True),
            suggestion="Never log passwords, tokens, secrets, or api keys",
            supported_extensions=['.ts', '.tsx']
        )


class FrontendNoTODOCommentsRule(PatternRule):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=config.get('patterns', []),
            blocking=config.get('blocking', False),
            suggestion="Remove TODO/FIXME or create a tracked issue",
            supported_extensions=['.ts', '.tsx', '.scss']
        )


class FrontendNoHardcodedURLsRule(PatternRule):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=config.get('patterns', []),
            blocking=config.get('blocking', False),
            suggestion="Use environment variables or configuration for URLs",
            supported_extensions=['.ts', '.tsx']
        )


class FrontendNoCommentedCodeRule(Rule):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            blocking=config.get('blocking', False),
            supported_extensions=['.ts', '.tsx', '.scss']
        )
        self.min_consecutive = config.get('min_consecutive_comments', 4)

    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')
        consecutive_comments = 0
        start_line = 0

        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*') or stripped.startswith('*/'):
                if consecutive_comments == 0:
                    start_line = line_num
                consecutive_comments += 1
            else:
                if consecutive_comments >= self.min_consecutive:
                    violations.append(
                        self._create_violation(
                            file_path=file_path,
                            line_number=start_line,
                            code_snippet=f"{consecutive_comments} consecutive comment lines",
                            message=f"Found {consecutive_comments} consecutive commented lines",
                            suggestion="Remove commented code; use version control instead"
                        )
                    )
                consecutive_comments = 0

        return violations


class FrontendNoConsoleLogRule(PatternRule):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=config.get('patterns', []),
            blocking=config.get('blocking', False),
            suggestion="Use approved logging utilities instead of console statements",
            supported_extensions=['.ts', '.tsx']
        )


class FrontendNoDebugFlagsRule(PatternRule):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=config.get('patterns', []),
            blocking=config.get('blocking', False),
            suggestion="Avoid hardcoded debug flags; use environment-based config",
            supported_extensions=['.ts', '.tsx']
        )


class FrontendNoStringConcatInLoggingRule(PatternRule):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=config.get('patterns', []),
            blocking=config.get('blocking', False),
            suggestion="Avoid string concatenation in logging statements",
            supported_extensions=['.ts', '.tsx']
        )


class FrontendBooleanNamingConventionRule(PatternRule):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=[config.get('pattern', r'\b(?:const|let|var)\s+(?!is|has|should|can|will)[a-zA-Z_]\w*\s*:\s*boolean\b')],
            blocking=config.get('blocking', False),
            suggestion="Boolean variables should start with is/has/should/can/will",
            supported_extensions=['.ts', '.tsx']
        )


class NoVarRule(PatternRule):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=[config.get('pattern', r'\bvar\s+\w+')],
            blocking=config.get('blocking', False),
            suggestion="Use let or const instead of var",
            supported_extensions=['.ts', '.tsx']
        )


class PreferConstRule(Rule):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            blocking=config.get('blocking', False),
            supported_extensions=['.ts', '.tsx']
        )

    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')

        for line_num, line in enumerate(lines, 1):
            match = re.search(r'\blet\s+([a-zA-Z_$][\w$]*)\s*=', line)
            if not match:
                continue

            variable_name = match.group(1)
            reassigned = False

            for later_line in lines[line_num:]:
                if re.search(rf'\b{re.escape(variable_name)}\s*=', later_line) or \
                   re.search(rf'\b{re.escape(variable_name)}\+\+', later_line) or \
                   re.search(rf'\+\+{re.escape(variable_name)}\b', later_line) or \
                   re.search(rf'\b{re.escape(variable_name)}--', later_line) or \
                   re.search(rf'--{re.escape(variable_name)}\b', later_line) or \
                   re.search(rf'\b{re.escape(variable_name)}\s*[\+\-\*/%]?=', later_line):
                    reassigned = True
                    break

            if not reassigned:
                violations.append(
                    self._create_violation(
                        file_path=file_path,
                        line_number=line_num,
                        code_snippet=line,
                        message=f"'{variable_name}' is declared with let but never reassigned",
                        suggestion="Use const instead of let"
                    )
                )

        return violations


class UnusedVariablesRule(Rule):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            blocking=config.get('blocking', False),
            supported_extensions=['.ts', '.tsx']
        )

    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')
        declarations = []

        declaration_patterns = [
            r'\b(?:const|let|var)\s+([a-zA-Z_$][\w$]*)\b',
            r'\bfunction\s+([a-zA-Z_$][\w$]*)\s*\(',
            r'\bconst\s+\[\s*([a-zA-Z_$][\w$]*)\s*,\s*([a-zA-Z_$][\w$]*)\s*\]\s*='
        ]

        for line_num, line in enumerate(lines, 1):
            for pattern in declaration_patterns:
                match = re.search(pattern, line)
                if match:
                    for group in match.groups():
                        if group and not group.startswith('_'):
                            declarations.append((group, line_num, line))

        content_without_declarations = content
        for name, _, declaration_line in declarations:
            content_without_declarations = content_without_declarations.replace(declaration_line, '', 1)
            if len(re.findall(rf'\b{re.escape(name)}\b', content_without_declarations)) == 0:
                violations.append(
                    self._create_violation(
                        file_path=file_path,
                        line_number=_,
                        code_snippet=declaration_line,
                        message=f"'{name}' is declared but never used",
                        suggestion="Remove unused variable or use it"
                    )
                )

        return violations


class UnusedFunctionsRule(Rule):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            blocking=config.get('blocking', False),
            supported_extensions=['.ts', '.tsx']
        )

    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')
        functions = []

        patterns = [
            r'\bfunction\s+([a-zA-Z_$][\w$]*)\s*\(',
            r'\bconst\s+([a-zA-Z_$][\w$]*)\s*=\s*\([^)]*\)\s*=>',
            r'\bconst\s+([a-zA-Z_$][\w$]*)\s*=\s*[a-zA-Z_$][\w$]*\s*=>',
            r'\b([a-zA-Z_$][\w$]*)\s*\([^)]*\)\s*\{'
        ]

        for line_num, line in enumerate(lines, 1):
            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    function_name = match.group(1)
                    if function_name not in ['if', 'for', 'while', 'switch', 'catch']:
                        functions.append((function_name, line_num, line))
                        break

        for function_name, line_num, line in functions:
            occurrences = len(re.findall(rf'\b{re.escape(function_name)}\b', content))
            if occurrences <= 1:
                violations.append(
                    self._create_violation(
                        file_path=file_path,
                        line_number=line_num,
                        code_snippet=line,
                        message=f"Function/method '{function_name}' is declared but never used",
                        suggestion="Remove unused function/method or use it"
                    )
                )

        return violations


class NoDebuggerRule(PatternRule):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=[config.get('pattern', r'\bdebugger\b')],
            blocking=config.get('blocking', False),
            suggestion="Remove debugger statements before merge",
            supported_extensions=['.ts', '.tsx']
        )


class NoExplicitAnyRule(PatternRule):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=config.get('patterns', [r':\s*any\b', r'<any>', r'\bas\s+any\b']),
            blocking=config.get('blocking', False),
            suggestion="Use a specific type instead of any",
            supported_extensions=['.ts', '.tsx']
        )


class NoEvalRule(PatternRule):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=[config.get('pattern', r'\beval\s*\(')],
            blocking=config.get('blocking', True),
            suggestion="Avoid eval(); use safer alternatives",
            supported_extensions=['.ts', '.tsx']
        )


class NoDangerouslySetInnerHTMLRule(PatternRule):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=[config.get('pattern', r'dangerouslySetInnerHTML')],
            blocking=config.get('blocking', True),
            suggestion="Avoid dangerouslySetInnerHTML unless content is fully sanitized",
            supported_extensions=['.tsx']
        )


class FrontendGenericVariableNamesRule(Rule):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            blocking=config.get('blocking', False),
            supported_extensions=['.ts', '.tsx']
        )
        self.blacklist = config.get('blacklist', [])

    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')

        for line_num, line in enumerate(lines, 1):
            for bad_name in self.blacklist:
                pattern = rf'\b(?:const|let|var|function)\s+{re.escape(bad_name)}\b'
                if re.search(pattern, line):
                    violations.append(
                        self._create_violation(
                            file_path=file_path,
                            line_number=line_num,
                            code_snippet=line,
                            message=f"Generic variable/function name '{bad_name}' found",
                            suggestion="Use descriptive names"
                        )
                    )

        return violations


class UnusedReactStateValueRule(Rule):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            blocking=config.get('blocking', False),
            supported_extensions=['.tsx']
        )

    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')
        state_hooks = re.finditer(
            r'const\s*\[\s*([a-zA-Z_$][\w$]*)\s*,\s*([a-zA-Z_$][\w$]*)\s*\]\s*=\s*useState\b',
            content
        )

        for match in state_hooks:
            state_name = match.group(1)
            setter_name = match.group(2)
            declaration_line = content[:match.start()].count('\n') + 1
            later_content = content[match.end():]

            if len(re.findall(rf'\b{re.escape(state_name)}\b', later_content)) == 0:
                line = lines[declaration_line - 1]
                violations.append(
                    self._create_violation(
                        file_path=file_path,
                        line_number=declaration_line,
                        code_snippet=line,
                        message=f"React state '{state_name}' is declared but never used",
                        suggestion=f"Remove '{state_name}' or use it in component logic/rendering"
                    )
                )

        return violations


class UnusedReactStateSetterRule(Rule):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            blocking=config.get('blocking', False),
            supported_extensions=['.tsx']
        )

    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')
        state_hooks = re.finditer(
            r'const\s*\[\s*([a-zA-Z_$][\w$]*)\s*,\s*([a-zA-Z_$][\w$]*)\s*\]\s*=\s*useState\b',
            content
        )

        for match in state_hooks:
            setter_name = match.group(2)
            declaration_line = content[:match.start()].count('\n') + 1
            later_content = content[match.end():]

            if len(re.findall(rf'\b{re.escape(setter_name)}\b', later_content)) == 0:
                line = lines[declaration_line - 1]
                violations.append(
                    self._create_violation(
                        file_path=file_path,
                        line_number=declaration_line,
                        code_snippet=line,
                        message=f"React state setter '{setter_name}' is declared but never used",
                        suggestion=f"Remove '{setter_name}' or update state through it"
                    )
                )

        return violations


class ReactStateNeverUpdatedRule(Rule):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            blocking=config.get('blocking', False),
            supported_extensions=['.tsx']
        )

    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')
        state_hooks = re.finditer(
            r'const\s*\[\s*([a-zA-Z_$][\w$]*)\s*,\s*([a-zA-Z_$][\w$]*)\s*\]\s*=\s*useState\b',
            content
        )

        for match in state_hooks:
            state_name = match.group(1)
            setter_name = match.group(2)
            declaration_line = content[:match.start()].count('\n') + 1
            later_content = content[match.end():]

            if len(re.findall(rf'\b{re.escape(setter_name)}\s*\(', later_content)) == 0:
                line = lines[declaration_line - 1]
                violations.append(
                    self._create_violation(
                        file_path=file_path,
                        line_number=declaration_line,
                        code_snippet=line,
                        message=f"React state '{state_name}' is never updated",
                        suggestion=f"Use '{setter_name}' to update state or replace useState with a constant"
                    )
                )

        return violations


class NoPxRule(Rule):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            blocking=config.get('blocking', False),
            supported_extensions=['.scss']
        )

    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')

        for line_num, line in enumerate(lines, 1):
            matches = re.finditer(r'(\d*\.?\d+)px\b', line)
            for match in matches:
                px_value = float(match.group(1))
                rem_value = px_value / 16
                rem_text = f"{rem_value:.4f}".rstrip('0').rstrip('.')
                violations.append(
                    self._create_violation(
                        file_path=file_path,
                        line_number=line_num,
                        code_snippet=line,
                        message=f"Use rem instead of px ({match.group(0)} found)",
                        suggestion=f"Replace {match.group(0)} with {rem_text}rem (1rem = 16px)"
                    )
                )

        return violations


class NoIdSelectorsRule(PatternRule):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=[config.get('pattern', r'^\s*#[a-zA-Z_-][\w-]*\s*\{')],
            blocking=config.get('blocking', False),
            suggestion="Avoid id selectors; prefer class-based styling",
            supported_extensions=['.scss']
        )


class MaxNestingDepthRule(Rule):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            blocking=config.get('blocking', False),
            supported_extensions=['.scss']
        )
        self.max_depth = config.get('max_depth', 3)

    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')
        depth = 0

        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            opens = stripped.count('{')
            closes = stripped.count('}')

            if opens > 0 and not stripped.startswith('@'):
                depth += opens
                if depth > self.max_depth:
                    violations.append(
                        self._create_violation(
                            file_path=file_path,
                            line_number=line_num,
                            code_snippet=line,
                            message=f"SCSS nesting depth exceeds maximum ({depth} > {self.max_depth})",
                            suggestion=f"Reduce nesting depth to {self.max_depth} or less"
                        )
                    )

            depth = max(0, depth - closes)

        return violations


class NoHardcodedHexColorsRule(PatternRule):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=[config.get('pattern', r'#[0-9a-fA-F]{3,8}\b')],
            blocking=config.get('blocking', False),
            suggestion="Use design tokens or SCSS variables instead of hardcoded hex colors",
            supported_extensions=['.scss']
        )


class NoEmptyScssBlocksRule(Rule):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            blocking=config.get('blocking', False),
            supported_extensions=['.scss']
        )

    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')

        for line_num, line in enumerate(lines, 1):
            if re.search(r'\{\s*\}', line):
                violations.append(
                    self._create_violation(
                        file_path=file_path,
                        line_number=line_num,
                        code_snippet=line,
                        message="Empty SCSS block found",
                        suggestion="Remove empty block or add declarations"
                    )
                )

        return violations

# Made with Bob