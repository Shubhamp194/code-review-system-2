"""
High Priority Rules (P0) - Security and Critical Code Quality
"""

import re
from typing import List, Dict, Any
from .base import Rule, RuleViolation, PatternRule, ContextAwareRule


def get_security_rules(config: List[Dict[str, Any]]) -> List[Rule]:
    """Get security rules from configuration"""
    rules = []
    
    for rule_config in config:
        rule_id = rule_config['id']
        
        if rule_id == 'SEC001':
            rules.append(IBMLicenseHeaderRule(rule_config))
        elif rule_id == 'SEC002':
            rules.append(NoHardcodedSecretsRule(rule_config))
        elif rule_id == 'SEC003':
            rules.append(NoSQLConcatenationRule(rule_config))
        elif rule_id == 'SEC004':
            rules.append(NoRuntimeExecRule(rule_config))
        elif rule_id == 'SEC005':
            rules.append(NoLoggingSensitiveDataRule(rule_config))
    
    return rules


def get_code_quality_rules(config: List[Dict[str, Any]]) -> List[Rule]:
    """Get code quality rules from configuration"""
    rules = []
    
    for rule_config in config:
        rule_id = rule_config['id']
        
        if rule_id == 'CQ001':
            rules.append(NoSystemOutRule(rule_config))
        elif rule_id == 'CQ002':
            rules.append(NoPrintStackTraceRule(rule_config))
        elif rule_id == 'CQ003':
            rules.append(NoTODOCommentsRule(rule_config))
        elif rule_id == 'CQ004':
            rules.append(NoEmptyCatchBlockRule(rule_config))
        elif rule_id == 'CQ005':
            rules.append(NoGenericExceptionRule(rule_config))
        elif rule_id == 'CQ006':
            rules.append(NoHardcodedURLsRule(rule_config))
        elif rule_id == 'CQ007':
            rules.append(NoHardcodedPathsRule(rule_config))
        elif rule_id == 'CQ008':
            rules.append(NoCommentedCodeRule(rule_config))
    
    return rules


def get_exception_rules(config: List[Dict[str, Any]]) -> List[Rule]:
    """Get exception handling rules from configuration"""
    rules = []
    
    for rule_config in config:
        rule_id = rule_config['id']
        
        if rule_id == 'EXC001':
            rules.append(ExceptionsMustBeLoggedRule(rule_config))
        elif rule_id == 'EXC002':
            rules.append(NoThrowingGenericExceptionRule(rule_config))
    
    return rules


# Security Rules Implementation

class IBMLicenseHeaderRule(Rule):
    """Check for IBM license header"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            blocking=config.get('blocking', True),
            supported_extensions=['.java']
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


class NoHardcodedSecretsRule(PatternRule):
    """Detect hardcoded secrets"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=config.get('patterns', []),
            blocking=config.get('blocking', True),
            suggestion="Use environment variables or configuration files for sensitive data",
            supported_extensions=['.java']
        )


class NoSQLConcatenationRule(PatternRule):
    """Detect SQL injection vulnerabilities"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=config.get('patterns', []),
            blocking=config.get('blocking', True),
            suggestion="Use PreparedStatement with parameterized queries",
            supported_extensions=['.java']
        )


class NoRuntimeExecRule(PatternRule):
    """Detect command injection vulnerabilities"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=config.get('patterns', []),
            blocking=config.get('blocking', True),
            suggestion="Avoid Runtime.exec() or use strict input validation with allowlists",
            supported_extensions=['.java']
        )


class NoLoggingSensitiveDataRule(PatternRule):
    """Detect logging of sensitive data"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=config.get('patterns', []),
            blocking=config.get('blocking', True),
            suggestion="Never log sensitive data; log events without exposing credentials",
            supported_extensions=['.java']
        )


# Code Quality Rules Implementation

class NoSystemOutRule(PatternRule):
    """Detect System.out/err usage"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=config.get('patterns', []),
            blocking=config.get('blocking', True),
            suggestion="Use proper logging framework (SLF4J, Log4j, etc.)",
            supported_extensions=['.java']
        )


class NoPrintStackTraceRule(PatternRule):
    """Detect printStackTrace usage"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=config.get('patterns', []),
            blocking=config.get('blocking', True),
            suggestion="Use proper logging: log.error(\"message\", exception)",
            supported_extensions=['.java']
        )


class NoTODOCommentsRule(PatternRule):
    """Detect TODO/FIXME comments"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=config.get('patterns', []),
            blocking=config.get('blocking', True),
            suggestion="Remove TODO/FIXME or create proper issue tracker items",
            supported_extensions=['.java']
        )


class NoEmptyCatchBlockRule(ContextAwareRule):
    """Detect empty catch blocks"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            blocking=config.get('blocking', True),
            supported_extensions=['.java']
        )
    
    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')
        
        # Simple pattern matching for empty catch blocks
        pattern = re.compile(r'catch\s*\([^)]+\)\s*\{\s*\}')
        
        for line_num, line in enumerate(lines, 1):
            if pattern.search(line):
                violations.append(
                    self._create_violation(
                        file_path=file_path,
                        line_number=line_num,
                        code_snippet=line,
                        message="Empty catch block found",
                        suggestion="Log the exception or handle it appropriately"
                    )
                )
        
        return violations
    
    def analyze_context(self, file_path: str, content: str, line_number: int) -> bool:
        # For now, simple implementation
        return True


class NoGenericExceptionRule(PatternRule):
    """Detect catching generic Exception"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=config.get('patterns', []),
            blocking=config.get('blocking', True),
            suggestion="Catch specific exception types",
            supported_extensions=['.java']
        )


class NoHardcodedURLsRule(PatternRule):
    """Detect hardcoded URLs"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=config.get('patterns', []),
            blocking=config.get('blocking', True),
            suggestion="Use configuration files or environment variables",
            supported_extensions=['.java']
        )


class NoHardcodedPathsRule(PatternRule):
    """Detect hardcoded file paths"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=config.get('patterns', []),
            blocking=config.get('blocking', True),
            suggestion="Use system properties or configuration",
            supported_extensions=['.java']
        )


class NoCommentedCodeRule(Rule):
    """Detect commented-out code blocks"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            blocking=config.get('blocking', False),
            supported_extensions=['.java']
        )
        self.min_consecutive = config.get('min_consecutive_comments', 5)
    
    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')
        consecutive_comments = 0
        start_line = 0
        
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('//'):
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


# Exception Handling Rules

class ExceptionsMustBeLoggedRule(ContextAwareRule):
    """Check if exceptions are logged in catch blocks"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            blocking=config.get('blocking', True),
            supported_extensions=['.java']
        )
    
    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')
        
        in_catch = False
        catch_start = 0
        catch_content = []
        
        for line_num, line in enumerate(lines, 1):
            if 'catch' in line and '(' in line:
                in_catch = True
                catch_start = line_num
                catch_content = []
            elif in_catch:
                catch_content.append(line)
                if '}' in line:
                    # Check if catch block has logging
                    block_text = '\n'.join(catch_content)
                    if not re.search(r'log\.(error|warn|info|debug)', block_text, re.IGNORECASE):
                        violations.append(
                            self._create_violation(
                                file_path=file_path,
                                line_number=catch_start,
                                code_snippet=f"catch block at line {catch_start}",
                                message="Exception not logged in catch block",
                                suggestion="Add logging: log.error(\"message\", exception)"
                            )
                        )
                    in_catch = False
        
        return violations
    
    def analyze_context(self, file_path: str, content: str, line_number: int) -> bool:
        return True


class NoThrowingGenericExceptionRule(PatternRule):
    """Detect throwing generic Exception"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=[config.get('pattern', 'throw\\s+new\\s+Exception\\(')],
            blocking=config.get('blocking', False),
            suggestion="Throw specific exception types",
            supported_extensions=['.java']
        )

# Made with Bob
