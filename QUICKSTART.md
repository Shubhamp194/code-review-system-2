# 🚀 Quick Start Guide

Get the AI Code Review System up and running in 5 minutes!

## Prerequisites

- Python 3.9 or higher
- Git
- Java 11+ (for sample project)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/bobathon-code-review.git
cd bobathon-code-review
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment (Optional)

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your credentials (optional for basic usage)
# nano .env
```

## Quick Test

### Run the Test Script

```bash
# Make script executable (macOS/Linux)
chmod +x test_analyzer.sh

# Run tests
./test_analyzer.sh
```

This will:
1. List all available rules
2. Analyze BadCode.java (should find many violations)
3. Analyze GoodCode.java (should be clean)
4. Analyze the entire sample project

## Manual Usage

### List All Rules

```bash
python -m src.analyzer.main rules
```

### Analyze a Single File

```bash
python -m src.analyzer.main file sample-java-project/src/main/java/com/ibm/demo/BadCode.java --show-code
```

### Analyze Entire Project

```bash
python -m src.analyzer.main project sample-java-project --output results.json
```

## Expected Output

### For BadCode.java (Many Violations)

```
🔴 [SEC002] No Hardcoded Secrets
   Severity: CRITICAL
   File: sample-java-project/src/main/java/com/ibm/demo/BadCode.java:14
   Message: Detects hardcoded passwords, API keys, tokens, and secrets
   Code: private String password = "admin123";
   💡 Suggestion: Use environment variables or configuration files for sensitive data

🟡 [CQ001] No System.out/err.println
   Severity: HIGH
   File: sample-java-project/src/main/java/com/ibm/demo/BadCode.java:24
   Message: Use proper logging framework instead
   Code: System.out.println("Processing data");
   💡 Suggestion: Use proper logging framework (SLF4J, Log4j, etc.)

... and many more violations
```

### For GoodCode.java (Clean)

```
✅ No violations found!
```

## GitHub Actions Integration

### Enable for Your Repository

1. Push code to GitHub
2. Create a Pull Request
3. GitHub Actions will automatically run the code review
4. Check the PR for automated comments with violations

### Manual Trigger

Go to Actions tab → Select "AI Code Review" → Click "Run workflow"

## Next Steps

### 1. Customize Rules

Edit `config/rules.yaml` to enable/disable rules or adjust severity levels.

### 2. Add to Your Java Project

```bash
# Copy analyzer to your project
cp -r src/analyzer your-java-project/
cp -r config your-java-project/
cp requirements.txt your-java-project/
cp .github/workflows/code-review.yml your-java-project/.github/workflows/
```

### 3. Configure for Your Needs

Update the workflow file to point to your Java source directory:

```yaml
- name: Run Code Analysis
  run: |
    python -m src.analyzer.main project src/main/java \
      --output analysis-results.json
```

## Common Commands

```bash
# List all rules with descriptions
python -m src.analyzer.main rules --verbose

# Analyze with custom config
python -m src.analyzer.main project . --config custom-rules.yaml

# Save results to JSON
python -m src.analyzer.main project . --output report.json

# Show code snippets in output
python -m src.analyzer.main file MyClass.java --show-code
```

## Troubleshooting

### Import Errors

```bash
# Make sure you're in the project root and venv is activated
pwd  # Should show /path/to/bobathon-code-review
which python  # Should show venv/bin/python
```

### No Java Files Found

```bash
# Check your directory structure
ls -R sample-java-project/
```

### Rules Not Loading

```bash
# Verify config file exists
cat config/rules.yaml
```

## Understanding Results

### Severity Levels

- 🔴 **CRITICAL**: Security vulnerabilities, must fix immediately
- 🟡 **HIGH**: Important code quality issues, should fix
- 🔵 **MEDIUM**: Best practices, recommended to fix
- ⚪ **LOW**: Minor issues, nice to fix

### Blocking vs Advisory

- **Blocking**: PR cannot be merged until fixed (CRITICAL, HIGH)
- **Advisory**: Suggestions for improvement (MEDIUM, LOW)

## Performance Tips

### For Large Projects

```bash
# Analyze specific directories only
python -m src.analyzer.main project src/main/java/com/myapp/core

# Limit violations displayed
python -m src.analyzer.main project . --max-violations 20
```

### Parallel Analysis

The analyzer automatically uses parallel processing for multiple files.

## Getting Help

```bash
# Show help
python -m src.analyzer.main --help

# Show command-specific help
python -m src.analyzer.main project --help
```

## What's Next?

- 📖 Read [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) for detailed architecture
- 📋 Check [RULE_SPECIFICATIONS.md](RULE_SPECIFICATIONS.md) for all rule details
- 🤖 See [AI_ENHANCEMENT_PLAN.md](AI_ENHANCEMENT_PLAN.md) for Bob AI integration
- 🏗️ Review [EXTENSIBILITY_ARCHITECTURE.md](EXTENSIBILITY_ARCHITECTURE.md) for plugins

## Support

- 📧 Email: team@example.com
- 🐛 Issues: https://github.com/your-org/bobathon-code-review/issues
- 📚 Docs: https://docs.bobathon-code-review.com

---

**Happy Coding! 🎉**