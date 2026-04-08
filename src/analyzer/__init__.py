"""
AI-Powered Code Review System
Main analyzer package
"""

from .pr_explanation_analyzer import PRExplanationAnalyzer
from .rule_engine import RuleEngine

__version__ = "1.0.0"
__author__ = "IBM Bob-a-thon Team"

__all__ = [
    "RuleEngine",
    "PRExplanationAnalyzer",
]

# Made with Bob
