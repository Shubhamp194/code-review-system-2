"""
Naming Convention Rules (P1)
"""

import re
from typing import List, Dict, Any
from .base import Rule, RuleViolation, PatternRule


def get_naming_rules(config: List[Dict[str, Any]]) -> List[Rule]:
    """Get naming rules from configuration"""
    rules = []
    for rule_config in config:
        rule_id = rule_config['id']
        if rule_id == 'NAM001':
            rules.append(LowercasePackageNamesRule(rule_config))
        elif rule_id == 'NAM002':
            rules.append(UpperCamelCaseClassNamesRule(rule_config))
        elif rule_id == 'NAM003':
            rules.append(LowerCamelCaseMethodNamesRule(rule_config))
        elif rule_id == 'NAM004':
            rules.append(UpperSnakeCaseConstantsRule(rule_config))
        elif rule_id == 'NAM005':
            rules.append(NoGenericVariableNamesRule(rule_config))
        elif rule_id == 'NAM007':
            rules.append(BooleanNamingConventionRule(rule_config))
    return rules


class LowercasePackageNamesRule(PatternRule):
    """Check for lowercase package names"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=[config.get('pattern', 'package\\s+[a-z0-9.]*[A-Z][a-z0-9.]*;')],
            blocking=config.get('blocking', False),
            suggestion="Use lowercase for package names",
            supported_extensions=['.java']
        )


class UpperCamelCaseClassNamesRule(PatternRule):
    """Check for UpperCamelCase class names"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=[config.get('pattern', '(class|interface|enum)\\s+[a-z]')],
            blocking=config.get('blocking', False),
            suggestion="Use UpperCamelCase for class names",
            supported_extensions=['.java']
        )


class LowerCamelCaseMethodNamesRule(PatternRule):
    """Check for lowerCamelCase method names"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=[config.get('pattern', '(public|private|protected)\\s+\\w+\\s+[A-Z]\\w+\\s*\\(')],
            blocking=config.get('blocking', False),
            suggestion="Use lowerCamelCase for method names",
            supported_extensions=['.java']
        )


class UpperSnakeCaseConstantsRule(PatternRule):
    """Check for UPPER_SNAKE_CASE constants"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=[config.get('pattern', 'static\\s+final\\s+\\w+\\s+[a-z]')],
            blocking=config.get('blocking', False),
            suggestion="Use UPPER_SNAKE_CASE for constants",
            supported_extensions=['.java']
        )


class NoGenericVariableNamesRule(Rule):
    """Check for generic variable names"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            blocking=config.get('blocking', False),
            supported_extensions=['.java']
        )
        self.blacklist = config.get('blacklist', [])
    
    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        violations = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            for bad_name in self.blacklist:
                # Look for variable declarations with blacklisted names
                pattern = rf'\b(int|long|double|float|String|Object|var)\s+{bad_name}\b'
                if re.search(pattern, line):
                    violations.append(
                        self._create_violation(
                            file_path=file_path,
                            line_number=line_num,
                            code_snippet=line,
                            message=f"Generic variable name '{bad_name}' found",
                            suggestion="Use descriptive variable names"
                        )
                    )
        
        return violations


class BooleanNamingConventionRule(PatternRule):
    """Check boolean naming convention"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            rule_id=config['id'],
            name=config['name'],
            severity=config['severity'],
            description=config['description'],
            patterns=[config.get('pattern', 'boolean\\s+(?!is|has|should|can|will)\\w+')],
            blocking=config.get('blocking', False),
            suggestion="Boolean variables should start with is/has/should/can/will",
            supported_extensions=['.java']
        )

# Made with Bob
