"""
Main Rule Engine for Code Analysis
"""

import os
import yaml
from typing import List, Dict, Any
from pathlib import Path

from .rules.base import Rule, RuleViolation
from .rules import high_priority, medium_priority, naming_rules, frontend_rules

SUPPORTED_EXTENSIONS = {'.java', '.ts', '.tsx', '.scss'}


class RuleEngine:
    """Main engine for running code analysis rules"""
    
    def __init__(self, config_path: str = 'config/rules.yaml'):
        self.config_path = config_path
        self.rules: List[Rule] = []
        self.config = self._load_config()
        self._initialize_rules()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Warning: Config file {self.config_path} not found. Using defaults.")
            return {}
    
    def _initialize_rules(self):
        """Initialize all rules from configuration"""
        rule_config = self.config.get('rules', {})
        
        # Load high priority rules
        if 'security' in rule_config:
            self.rules.extend(high_priority.get_security_rules(rule_config['security']))
        
        if 'code_quality' in rule_config:
            self.rules.extend(high_priority.get_code_quality_rules(rule_config['code_quality']))
        
        if 'exceptions' in rule_config:
            self.rules.extend(high_priority.get_exception_rules(rule_config['exceptions']))
        
        # Load medium priority rules
        if 'imports' in rule_config:
            self.rules.extend(medium_priority.get_import_rules(rule_config['imports']))
        
        if 'formatting' in rule_config:
            self.rules.extend(medium_priority.get_formatting_rules(rule_config['formatting']))
        
        if 'best_practices' in rule_config:
            self.rules.extend(medium_priority.get_best_practice_rules(rule_config['best_practices']))
        
        # Load naming rules
        if 'naming' in rule_config:
            self.rules.extend(naming_rules.get_naming_rules(rule_config['naming']))
        
        # Load logging rules
        if 'logging' in rule_config:
            self.rules.extend(medium_priority.get_logging_rules(rule_config['logging']))
        
        # Load frontend rules
        frontend_config = self.config.get('frontend_rules', {})
        if frontend_config:
            self.rules.extend(frontend_rules.get_frontend_rules(frontend_config))
    
    def analyze_file(self, file_path: str, content: str) -> List[RuleViolation]:
        """
        Analyze a single file
        
        Args:
            file_path: Path to the file
            content: Content of the file
            
        Returns:
            List of violations found
        """
        violations = []
        
        for rule in self.rules:
            if rule.is_enabled() and rule.applies_to_file(file_path):
                try:
                    rule_violations = rule.check(file_path, content)
                    violations.extend(rule_violations)
                except Exception as e:
                    print(f"Error running rule {rule.rule_id}: {str(e)}")
        
        return violations
    
    def analyze_files(self, files: Dict[str, str]) -> Dict[str, Any]:
        """
        Analyze multiple files
        
        Args:
            files: Dictionary mapping file paths to their content
            
        Returns:
            Analysis results with violations categorized by severity
        """
        all_violations = []
        
        for file_path, content in files.items():
            if Path(file_path).suffix.lower() in SUPPORTED_EXTENSIONS:
                violations = self.analyze_file(file_path, content)
                all_violations.extend(violations)
        
        return self._categorize_violations(all_violations)
    
    def _categorize_violations(self, violations: List[RuleViolation]) -> Dict[str, Any]:
        """Categorize violations by severity"""
        categorized = {
            'CRITICAL': [],
            'HIGH': [],
            'MEDIUM': [],
            'LOW': []
        }
        
        for violation in violations:
            severity = violation.severity
            if severity in categorized:
                categorized[severity].append(violation.to_dict())
        
        # Calculate summary
        total = len(violations)
        blocking_count = len(categorized['CRITICAL']) + len(categorized['HIGH'])
        
        return {
            'total_violations': total,
            'blocking_violations': blocking_count,
            'should_block': blocking_count > 0,
            'violations': categorized,
            'summary': {
                'critical': len(categorized['CRITICAL']),
                'high': len(categorized['HIGH']),
                'medium': len(categorized['MEDIUM']),
                'low': len(categorized['LOW'])
            }
        }
    
    def get_enabled_rules(self) -> List[Dict[str, Any]]:
        """Get list of enabled rules"""
        return [
            {
                'id': rule.rule_id,
                'name': rule.name,
                'severity': rule.severity,
                'blocking': rule.blocking,
                'description': rule.description
            }
            for rule in self.rules if rule.is_enabled()
        ]
    
    def get_rule_count(self) -> Dict[str, int]:
        """Get count of rules by severity"""
        counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        for rule in self.rules:
            if rule.is_enabled() and rule.severity in counts:
                counts[rule.severity] += 1
        return counts

# Made with Bob
