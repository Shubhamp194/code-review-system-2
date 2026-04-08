"""
Base classes for rule definitions
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path
import re


@dataclass
class RuleViolation:
    """Represents a rule violation"""
    rule_id: str
    rule_name: str
    severity: str
    file_path: str
    line_number: int
    column: Optional[int]
    message: str
    code_snippet: str
    suggestion: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'rule_id': self.rule_id,
            'rule_name': self.rule_name,
            'severity': self.severity,
            'file': self.file_path,
            'line': self.line_number,
            'column': self.column,
            'message': self.message,
            'code': self.code_snippet,
            'suggestion': self.suggestion
        }


class Rule(ABC):
    """Base class for all rules"""
    
    def __init__(self, rule_id: str, name: str, severity: str,
                 description: str, blocking: bool = False,
                 supported_extensions: Optional[List[str]] = None):
        self.rule_id = rule_id
        self.name = name
        self.severity = severity
        self.description = description
        self.blocking = blocking
        self.enabled = True
        self.supported_extensions = [ext.lower() for ext in (supported_extensions or ['.java'])]
    
    @abstractmethod
    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        """
        Check the file content for violations
        
        Args:
            file_path: Path to the file being analyzed
            content: Content of the file
            
        Returns:
            List of violations found
        """
        pass
    
    def is_enabled(self) -> bool:
        """Check if rule is enabled"""
        return self.enabled
    
    def should_block(self) -> bool:
        """Check if violations should block PR merge"""
        return self.blocking
    
    def applies_to_file(self, file_path: str) -> bool:
        """Check if rule applies to the given file type"""
        return Path(file_path).suffix.lower() in self.supported_extensions
    
    def _create_violation(self, file_path: str, line_number: int, 
                         code_snippet: str, message: str,
                         column: Optional[int] = None,
                         suggestion: Optional[str] = None) -> RuleViolation:
        """Helper to create a violation"""
        return RuleViolation(
            rule_id=self.rule_id,
            rule_name=self.name,
            severity=self.severity,
            file_path=file_path,
            line_number=line_number,
            column=column,
            message=message,
            code_snippet=code_snippet.strip(),
            suggestion=suggestion
        )


class PatternRule(Rule):
    """Rule based on regex patterns"""
    
    def __init__(self, rule_id: str, name: str, severity: str,
                 description: str, patterns: List[str],
                 blocking: bool = False, suggestion: Optional[str] = None,
                 supported_extensions: Optional[List[str]] = None):
        super().__init__(rule_id, name, severity, description, blocking, supported_extensions)
        self.patterns = [re.compile(p, re.IGNORECASE) for p in patterns]
        self.default_suggestion = suggestion
    
    def check(self, file_path: str, content: str) -> List[RuleViolation]:
        """Check file content against patterns"""
        violations = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            for pattern in self.patterns:
                if pattern.search(line):
                    violations.append(
                        self._create_violation(
                            file_path=file_path,
                            line_number=line_num,
                            code_snippet=line,
                            message=f"{self.description}",
                            suggestion=self.default_suggestion
                        )
                    )
                    break  # Only report once per line
        
        return violations


class ContextAwareRule(Rule):
    """Rule that requires context analysis"""
    
    def __init__(self, rule_id: str, name: str, severity: str,
                 description: str, blocking: bool = False,
                 supported_extensions: Optional[List[str]] = None):
        super().__init__(rule_id, name, severity, description, blocking, supported_extensions)
    
    @abstractmethod
    def analyze_context(self, file_path: str, content: str, 
                       line_number: int) -> bool:
        """
        Analyze context around a potential violation
        
        Returns:
            True if it's a violation, False otherwise
        """
        pass

# Made with Bob
