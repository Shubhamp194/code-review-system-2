"""
Main CLI entry point for code analysis across Java, TypeScript, TSX, and SCSS
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List
import colorama
from colorama import Fore, Style

from .rule_engine import RuleEngine


colorama.init(autoreset=True)


def read_file(file_path: str) -> str:
    """Read file content"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"{Fore.RED}Error reading {file_path}: {str(e)}")
        return ""


SUPPORTED_EXTENSIONS = ('.java', '.ts', '.tsx', '.scss')


def find_supported_files(directory: str) -> List[str]:
    """Find all supported source files in directory"""
    supported_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(SUPPORTED_EXTENSIONS):
                supported_files.append(os.path.join(root, file))
    return supported_files


def print_violation(violation: Dict, show_code: bool = True):
    """Print a single violation with color"""
    severity = violation['severity']
    
    # Color based on severity
    if severity == 'CRITICAL':
        color = Fore.RED
        icon = '🔴'
    elif severity == 'HIGH':
        color = Fore.YELLOW
        icon = '🟡'
    elif severity == 'MEDIUM':
        color = Fore.CYAN
        icon = '🔵'
    else:
        color = Fore.WHITE
        icon = '⚪'
    
    print(f"\n{color}{icon} [{violation['rule_id']}] {violation['rule_name']}")
    print(f"{color}   Severity: {severity}")
    print(f"{color}   File: {violation['file']}:{violation['line']}")
    print(f"{color}   Message: {violation['message']}")
    
    if show_code and violation.get('code'):
        print(f"{Fore.WHITE}   Code: {violation['code'][:100]}")
    
    if violation.get('suggestion'):
        print(f"{Fore.GREEN}   💡 Suggestion: {violation['suggestion']}")


def print_summary(results: Dict):
    """Print analysis summary"""
    summary = results['summary']
    
    print(f"\n{Style.BRIGHT}{'='*60}")
    print(f"{Style.BRIGHT}ANALYSIS SUMMARY")
    print(f"{Style.BRIGHT}{'='*60}")
    
    print(f"\n{Fore.WHITE}Total Violations: {results['total_violations']}")
    print(f"{Fore.RED}  Critical: {summary['critical']}")
    print(f"{Fore.YELLOW}  High: {summary['high']}")
    print(f"{Fore.CYAN}  Medium: {summary['medium']}")
    print(f"{Fore.WHITE}  Low: {summary['low']}")
    
    if results['should_block']:
        print(f"\n{Fore.RED}{Style.BRIGHT}❌ PR SHOULD BE BLOCKED")
        print(f"{Fore.RED}   {results['blocking_violations']} blocking violations found")
    else:
        print(f"\n{Fore.GREEN}{Style.BRIGHT}✅ PR CAN BE MERGED")
        print(f"{Fore.GREEN}   No blocking violations found")


def analyze_file_cmd(args):
    """Analyze a single file"""
    engine = RuleEngine(args.config)
    
    content = read_file(args.file)
    if not content:
        return 1
    
    print(f"{Fore.CYAN}Analyzing: {args.file}")
    violations = engine.analyze_file(args.file, content)
    
    if violations:
        print(f"\n{Fore.YELLOW}Found {len(violations)} violations:")
        for violation in violations:
            print_violation(violation.to_dict(), args.show_code)
    else:
        print(f"{Fore.GREEN}✅ No violations found!")
    
    return 0


def analyze_project_cmd(args):
    """Analyze entire project"""
    engine = RuleEngine(args.config)
    
    print(f"{Fore.CYAN}Scanning for supported files in: {args.project}")
    supported_files = find_supported_files(args.project)
    
    if not supported_files:
        print(f"{Fore.YELLOW}No supported files found ({', '.join(SUPPORTED_EXTENSIONS)})")
        return 0
    
    print(f"{Fore.CYAN}Found {len(supported_files)} supported files")
    
    # Read all files
    files = {}
    for file_path in supported_files:
        content = read_file(file_path)
        if content:
            files[file_path] = content
    
    # Analyze
    print(f"{Fore.CYAN}Running analysis...")
    results = engine.analyze_files(files)
    
    # Print violations by severity
    for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
        violations = results['violations'][severity]
        if violations:
            print(f"\n{Style.BRIGHT}{severity} Violations ({len(violations)}):")
            for violation in violations[:args.max_violations]:
                print_violation(violation, args.show_code)
            
            if len(violations) > args.max_violations:
                print(f"{Fore.WHITE}   ... and {len(violations) - args.max_violations} more")
    
    # Print summary
    print_summary(results)
    
    # Save to file if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n{Fore.GREEN}Results saved to: {args.output}")
    
    return 1 if results['should_block'] else 0


def list_rules_cmd(args):
    """List all enabled rules"""
    engine = RuleEngine(args.config)
    rules = engine.get_enabled_rules()
    counts = engine.get_rule_count()
    
    print(f"{Style.BRIGHT}Enabled Rules ({len(rules)}):")
    print(f"{Style.BRIGHT}{'='*60}\n")
    
    # Group by severity
    for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
        severity_rules = [r for r in rules if r['severity'] == severity]
        if severity_rules:
            print(f"{Style.BRIGHT}{severity} ({len(severity_rules)}):")
            for rule in severity_rules:
                blocking = "🚫 BLOCKING" if rule['blocking'] else "ℹ️  Advisory"
                print(f"  [{rule['id']}] {rule['name']} - {blocking}")
                if args.verbose:
                    print(f"      {rule['description']}")
            print()
    
    print(f"{Style.BRIGHT}Summary:")
    print(f"  Total Rules: {len(rules)}")
    print(f"  Critical: {counts['CRITICAL']}")
    print(f"  High: {counts['HIGH']}")
    print(f"  Medium: {counts['MEDIUM']}")
    print(f"  Low: {counts['LOW']}")
    
    return 0


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='AI-Powered Code Review System for Java, TypeScript, TSX, and SCSS',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--config',
        default='config/rules.yaml',
        help='Path to rules configuration file'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Analyze file command
    file_parser = subparsers.add_parser('file', help='Analyze a single file')
    file_parser.add_argument('file', help='Path to supported source file (.java, .ts, .tsx, .scss)')
    file_parser.add_argument('--show-code', action='store_true', help='Show code snippets')
    
    # Analyze project command
    project_parser = subparsers.add_parser('project', help='Analyze entire project for supported source files')
    project_parser.add_argument('project', help='Path to project directory')
    project_parser.add_argument('--output', '-o', help='Output file for results (JSON)')
    project_parser.add_argument('--show-code', action='store_true', help='Show code snippets')
    project_parser.add_argument('--max-violations', type=int, default=10, 
                               help='Max violations to display per severity')
    
    # List rules command
    rules_parser = subparsers.add_parser('rules', help='List all enabled rules')
    rules_parser.add_argument('--verbose', '-v', action='store_true', 
                             help='Show rule descriptions')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == 'file':
            return analyze_file_cmd(args)
        elif args.command == 'project':
            return analyze_project_cmd(args)
        elif args.command == 'rules':
            return list_rules_cmd(args)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Analysis interrupted")
        return 1
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

# Made with Bob
