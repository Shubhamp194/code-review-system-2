"""
Medium Priority Rules (P1) - Best Practices and Formatting
"""

import re
from typing import List, Dict, Any
from .base import Rule, RuleViolation, PatternRule


def get_import_rules(config: List[Dict[str, Any]]) -> List[Rule]:
    """Get import rules from configuration"""
    rules = []
    for rule_config in config:
        rule_id = rule_config['id']
        if rule_id == 'IMP001':
            rules.append(NoWildcardImportsRule(rule_config))
        elif rule_id == 'IMP002':
            rules.append(NoDuplicateImportsRule(rule_config))
    return rules


def get_formatting_rules(config: List[Dict[str, Any]]) -> List[Rule]:
    """Get formatting rules from configuration"""
    rules = []
    for rule_config in config:
        rule_id = rule_config['id']
        if rule_id == 'FMT001':
            rules.append(NoTrailingWhitespaceRule(rule_config))
        elif rule_id == 'FMT002':
            rules.append(MaxConsecutiveBlankLinesRule(rule_config))
        elif rule_id == 'FMT003':
            rules.append(LineLengthRule(rule_config))
        elif rule_id == 'FMT004':
            rules.append(FileEndsWithNewlineRule(rule_config))
    return rules


def get_best_practice_rules(config: List[Dict[str, Any]]) -> List[Rule]:
    """Get best practice rules from configuration"""
    rules = []
    for rule_config in config:
        rule_id = rule_config['id']
        if rule_id == 'BP001':
            rules.append(NoDebugFlagsRule(rule_config))
        elif rule_id == 'BP002':
            rules.append(NoSystemExitRule(rule_config))
        elif rule_id == 'BP003':
            rules.append(NoThreadSleepRule(rule_config))
        elif rule_id == 'BP004':
            rules.append(NoStringConcatInLoopsRule(rule_config))
        elif rule_id == 'BP005':
            rules.append(NoStringComparisonWithEqualsRule(rule_config))
        elif rule_id == 'BP006':
            rules.append(NoPublicFieldsRule(rule_config))
        elif rule_id == 'BP007':
            rules.append(NoStaticMutableVariablesRule(rule_config))
    return rules


def get_logging_rules(config: List[Dict[str, Any]]) -> List[Rule]:
    """Get logging rules from configuration"""
    rules = []
    for rule_config in config:
        rule_id = rule_config['id']
        if rule_id == 'LOG001':
            rules.append(NoStringConcatInLoggingRule(rule_config))
        elif rule_id == 'LOG002':
            rules.append(LoggerVariableNamingRule(rule_config))
    return rules


# Import Rules

class NoWildcardImportsRule(PatternRule):
    """Detect wildcard imports"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=config.get('patterns', []),
            blocking=config.get('blocking', False),
            suggestion="Import specific classes instead of using wildcards",
            supported_extensions=['.java']
        )


class NoDuplicateImportsRule(Rule):
    """Detect duplicate imports"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            blocking=config.get('blocking', False),
            supported_extensions=['.java']
        )
    
    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        imports = {}
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('import '):
                import_stmt = line.strip()
                if import_stmt in imports:
                    violations.append(
                        self._create_violation(
                            file_path=file_path,
                            line_number=line_num,
                            code_snippet=line,
                            message=f"Duplicate import (first seen at line {imports[import_stmt]})",
                            suggestion="Remove duplicate import statement"
                        )
                    )
                else:
                    imports[import_stmt] = line_num
        
        return violations


# Formatting Rules

class NoTrailingWhitespaceRule(Rule):
    """Detect trailing whitespace"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            blocking=config.get('blocking', False),
            supported_extensions=['.java', '.ts', '.tsx', '.scss']
        )
    
    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            if line.endswith(' ') or line.endswith('\t'):
                violations.append(
                    self._create_violation(
                        file_path=file_path,
                        line_number=line_num,
                        code_snippet=line,
                        message="Line has trailing whitespace",
                        suggestion="Remove trailing whitespace"
                    )
                )
        
        return violations


class MaxConsecutiveBlankLinesRule(Rule):
    """Check for too many consecutive blank lines"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            blocking=config.get('blocking', False),
            supported_extensions=['.java', '.ts', '.tsx', '.scss']
        )
        self.max_blank_lines = config.get('max_blank_lines', 2)
    
    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')
        consecutive_blank = 0
        start_line = 0
        
        for line_num, line in enumerate(lines, 1):
            if line.strip() == '':
                if consecutive_blank == 0:
                    start_line = line_num
                consecutive_blank += 1
            else:
                if consecutive_blank > self.max_blank_lines:
                    violations.append(
                        self._create_violation(
                            file_path=file_path,
                            line_number=start_line,
                            code_snippet=f"{consecutive_blank} consecutive blank lines",
                            message=f"Too many consecutive blank lines ({consecutive_blank})",
                            suggestion=f"Limit to {self.max_blank_lines} consecutive blank lines"
                        )
                    )
                consecutive_blank = 0
        
        return violations


class LineLengthRule(Rule):
    """Check line length"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            blocking=config.get('blocking', False),
            supported_extensions=['.java', '.ts', '.tsx', '.scss']
        )
        self.max_length = config.get('max_line_length', 120)
    
    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            if len(line) > self.max_length:
                violations.append(
                    self._create_violation(
                        file_path=file_path,
                        line_number=line_num,
                        code_snippet=line[:50] + '...',
                        message=f"Line too long ({len(line)} > {self.max_length})",
                        suggestion="Break long lines into multiple lines"
                    )
                )
        
        return violations


class FileEndsWithNewlineRule(Rule):
    """Check if file ends with newline"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            blocking=config.get('blocking', False),
            supported_extensions=['.java', '.ts', '.tsx', '.scss']
        )
    
    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        
        if content and not content.endswith('\n'):
            violations.append(
                self._create_violation(
                    file_path=file_path,
                    line_number=len(content.split('\n')),
                    code_snippet="<end of file>",
                    message="File does not end with newline",
                    suggestion="Add newline at end of file"
                )
            )
        
        return violations


# Best Practice Rules

class NoDebugFlagsRule(PatternRule):
    """Detect debug flags"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=config.get('patterns', []),
            blocking=config.get('blocking', False),
            suggestion="Use configuration or environment variables for debug flags",
            supported_extensions=['.java']
        )


class NoSystemExitRule(PatternRule):
    """Detect System.exit usage"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=[config.get('pattern', 'System\\.exit\\(')],
            blocking=config.get('blocking', False),
            suggestion="Use proper exception handling instead of System.exit()",
            supported_extensions=['.java']
        )


class NoThreadSleepRule(PatternRule):
    """Detect Thread.sleep usage"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=[config.get('pattern', 'Thread\\.sleep\\(')],
            blocking=config.get('blocking', False),
            suggestion="Use proper concurrency utilities (TimeUnit, ScheduledExecutorService)",
            supported_extensions=['.java']
        )


class NoStringConcatInLoopsRule(Rule):
    """Detect string concatenation in loops"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            blocking=config.get('blocking', False),
            supported_extensions=['.java']
        )
    
    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')
        in_loop = False
        loop_start = 0
        
        for line_num, line in enumerate(lines, 1):
            if re.search(r'\b(for|while)\s*\(', line):
                in_loop = True
                loop_start = line_num
            elif in_loop and re.search(r'\w+\s*\+=\s*["\']', line):
                violations.append(
                    self._create_violation(
                        file_path=file_path,
                        line_number=line_num,
                        code_snippet=line,
                        message="String concatenation in loop",
                        suggestion="Use StringBuilder for string concatenation in loops"
                    )
                )
            elif in_loop and '}' in line:
                in_loop = False
        
        return violations


class NoStringComparisonWithEqualsRule(PatternRule):
    """Detect == for string comparison"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=config.get('patterns', []),
            blocking=config.get('blocking', False),
            suggestion="Use .equals() method for string comparison",
            supported_extensions=['.java']
        )


class NoPublicFieldsRule(PatternRule):
    """Detect public fields"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=[config.get('pattern', 'public\\s+(?!class|interface|enum|static\\s+final)\\w+\\s+\\w+\\s*;')],
            blocking=config.get('blocking', False),
            suggestion="Make fields private and provide getters/setters",
            supported_extensions=['.java']
        )


class NoStaticMutableVariablesRule(PatternRule):
    """Detect static mutable variables"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=[config.get('pattern', 'static\\s+(?!final)\\w+\\s+\\w+\\s*=')],
            blocking=config.get('blocking', False),
            suggestion="Make static variables final or use thread-safe alternatives",
            supported_extensions=['.java']
        )


# Logging Rules

class NoStringConcatInLoggingRule(PatternRule):
    """Detect string concatenation in logging"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=config.get('patterns', []),
            blocking=config.get('blocking', False),
            suggestion="Use parameterized logging: log.info(\"message: {}\", value)",
            supported_extensions=['.java']
        )


class LoggerVariableNamingRule(PatternRule):
    """Check logger variable naming"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=[config.get('pattern', 'Logger\\s+(?!log|logger)\\w+\\s*=')],
            blocking=config.get('blocking', False),
            suggestion="Name logger variable as 'log' or 'logger'",
            supported_extensions=['.java']
        )

# Made with Bob
