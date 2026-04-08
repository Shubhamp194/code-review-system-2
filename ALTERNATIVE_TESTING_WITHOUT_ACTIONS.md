# Alternative Testing Guide (Without GitHub Actions)

## 🚨 Issue Identified
GitHub Actions has been **disabled by enterprise administrators** in your IBM GitHub environment.

**Screenshot shows:**
- "This setting has been disabled by enterprise administrators"
- "Disable actions" is selected
- Cannot enable GitHub Actions workflows

## ✅ Alternative Solution: Local Testing + Manual Integration

Since we cannot use GitHub Actions, we'll test the code review system locally and provide alternative integration options.

---

## Option 1: Local Testing (Immediate)

### Step 1: Test the Analyzer Locally

Run the analyzer on the test file we created:

```bash
cd /Users/shubhampandey/Bobathon

# Test on the file with violations
python src/analyzer/main.py analyze-file sample-java-project/src/main/java/com/ibm/demo/TestPRFile.java

# Test on entire project
python src/analyzer/main.py analyze-project sample-java-project/src/main/java/

# Generate JSON report
python src/analyzer/main.py analyze-project sample-java-project/src/main/java/ --output test-pr-results.json
```

### Step 2: Review the Results

The analyzer will output:
- Total violations found
- Breakdown by severity (Critical, High, Medium, Low)
- Specific line numbers and descriptions
- Blocking vs. non-blocking issues

### Step 3: Verify Expected Violations

Expected output for TestPRFile.java:
```
🔍 Code Review Results

Summary:
- Total Violations: 20+
- Blocking Issues: 4 (CRITICAL)
- Warnings: 16+ (HIGH, MEDIUM, LOW)

Critical Issues (BLOCKING):
1. Missing IBM License Header (line 1)
2. Hardcoded Secret: password (line 11)
3. Hardcoded Secret: apiKey (line 12)
4. SQL Injection Risk (line 44)

High Priority Issues:
5. System.out.println usage (line 22)
6. Empty catch block (line 26-28)
7. TODO comment (line 37)
8. Hardcoded URL (line 40)
9. SQL string concatenation (line 44)
10. Generic Exception catch (line 54)
11. printStackTrace usage (line 56)
12. Commented-out code (line 66-67)
13. System.err.println usage (line 72)

... and more
```

---

## Option 2: Git Pre-Commit Hook (Local Enforcement)

Since GitHub Actions is disabled, we can use Git hooks to run checks before commits.

### Setup Pre-Commit Hook

Create a pre-commit hook that runs the analyzer:

```bash
cd /Users/shubhampandey/Bobathon

# Create hooks directory if it doesn't exist
mkdir -p .git/hooks

# Create pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

echo "🔍 Running code review checks..."

# Get list of staged Java files
JAVA_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.java$')

if [ -z "$JAVA_FILES" ]; then
    echo "✅ No Java files to check"
    exit 0
fi

# Run analyzer on staged files
BLOCKING_FOUND=false
for file in $JAVA_FILES; do
    if [ -f "$file" ]; then
        echo "Analyzing: $file"
        python src/analyzer/main.py analyze-file "$file" --blocking-only
        if [ $? -ne 0 ]; then
            BLOCKING_FOUND=true
        fi
    fi
done

if [ "$BLOCKING_FOUND" = true ]; then
    echo ""
    echo "❌ COMMIT BLOCKED: Critical violations found!"
    echo "Fix the issues above before committing."
    exit 1
fi

echo "✅ All checks passed!"
exit 0
EOF

# Make it executable
chmod +x .git/hooks/pre-commit

echo "✅ Pre-commit hook installed!"
```

### Test the Pre-Commit Hook

```bash
# Try to commit the file with violations
git add sample-java-project/src/main/java/com/ibm/demo/TestPRFile.java
git commit -m "test: Should be blocked by pre-commit hook"

# Expected: Commit will be blocked due to critical violations
```

---

## Option 3: Manual PR Review Script

Create a script to manually review PRs and post results as comments.

### Create Manual Review Script

```bash
cd /Users/shubhampandey/Bobathon

# Create manual review script
cat > scripts/manual-pr-review.sh << 'EOF'
#!/bin/bash

# Manual PR Review Script
# Usage: ./scripts/manual-pr-review.sh <branch-name>

BRANCH=$1
BASE_BRANCH=${2:-main}

if [ -z "$BRANCH" ]; then
    echo "Usage: $0 <branch-name> [base-branch]"
    exit 1
fi

echo "🔍 Reviewing changes in branch: $BRANCH"
echo "📊 Comparing against: $BASE_BRANCH"
echo ""

# Get list of changed Java files
CHANGED_FILES=$(git diff --name-only $BASE_BRANCH...$BRANCH | grep '\.java$')

if [ -z "$CHANGED_FILES" ]; then
    echo "✅ No Java files changed"
    exit 0
fi

echo "📁 Changed Java files:"
echo "$CHANGED_FILES"
echo ""

# Analyze each changed file
TOTAL_VIOLATIONS=0
BLOCKING_VIOLATIONS=0

for file in $CHANGED_FILES; do
    if [ -f "$file" ]; then
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "📄 Analyzing: $file"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        python src/analyzer/main.py analyze-file "$file" --output "${file}.review.json"
        
        # Count violations (simplified - you can enhance this)
        if [ -f "${file}.review.json" ]; then
            # Parse JSON to count violations
            VIOLATIONS=$(python -c "import json; data=json.load(open('${file}.review.json')); print(len(data.get('violations', [])))")
            BLOCKING=$(python -c "import json; data=json.load(open('${file}.review.json')); print(sum(1 for v in data.get('violations', []) if v.get('blocking', False)))")
            
            TOTAL_VIOLATIONS=$((TOTAL_VIOLATIONS + VIOLATIONS))
            BLOCKING_VIOLATIONS=$((BLOCKING_VIOLATIONS + BLOCKING))
            
            rm "${file}.review.json"
        fi
        echo ""
    fi
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Review Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Total Violations: $TOTAL_VIOLATIONS"
echo "Blocking Issues: $BLOCKING_VIOLATIONS"
echo ""

if [ $BLOCKING_VIOLATIONS -gt 0 ]; then
    echo "❌ PR REVIEW FAILED"
    echo "Critical violations must be fixed before merge!"
    exit 1
else
    echo "✅ PR REVIEW PASSED"
    echo "No blocking violations found"
    exit 0
fi
EOF

# Make it executable
chmod +x scripts/manual-pr-review.sh

echo "✅ Manual PR review script created!"
```

### Use the Manual Review Script

```bash
# Review the test branch
./scripts/manual-pr-review.sh test-pr-with-violations main

# This will analyze all Java files changed in the branch
# and provide a summary of violations
```

---

## Option 4: Jenkins/GitLab CI Integration (If Available)

If your organization uses Jenkins or GitLab CI instead of GitHub Actions:

### Jenkins Pipeline Example

```groovy
pipeline {
    agent any
    
    stages {
        stage('Code Review') {
            steps {
                script {
                    // Get changed Java files
                    def changedFiles = sh(
                        script: "git diff --name-only origin/main...HEAD | grep '\\.java\$' || true",
                        returnStdout: true
                    ).trim()
                    
                    if (changedFiles) {
                        // Run analyzer
                        sh """
                            python src/analyzer/main.py analyze-project src/ --output review-results.json
                        """
                        
                        // Check for blocking violations
                        def hasBlocking = sh(
                            script: "python -c \"import json; data=json.load(open('review-results.json')); exit(1 if any(v.get('blocking') for v in data.get('violations', [])) else 0)\"",
                            returnStatus: true
                        )
                        
                        if (hasBlocking != 0) {
                            error("Critical code violations found!")
                        }
                    }
                }
            }
        }
    }
}
```

---

## Option 5: IDE Integration (Real-time Feedback)

### VSCode Extension (Future Enhancement)

Create a VSCode extension that runs the analyzer in real-time:
- Highlights violations as you type
- Shows inline warnings and errors
- Provides quick fixes

### IntelliJ IDEA Plugin (Future Enhancement)

Similar integration for IntelliJ IDEA users.

---

## Recommended Approach for Hackathon Demo

Since GitHub Actions is disabled, here's the best approach for your hackathon:

### 1. **Local Testing Demo** (Immediate)
```bash
# Run analyzer on test file
python src/analyzer/main.py analyze-file sample-java-project/src/main/java/com/ibm/demo/TestPRFile.java

# Show colorized output with violations
# Take screenshots for presentation
```

### 2. **Pre-Commit Hook Demo** (5 minutes setup)
```bash
# Install pre-commit hook
# Try to commit bad code
# Show it gets blocked
# Fix issues and commit successfully
```

### 3. **Manual PR Review Demo** (10 minutes setup)
```bash
# Run manual review script
./scripts/manual-pr-review.sh test-pr-with-violations main

# Show comprehensive analysis
# Demonstrate blocking vs. non-blocking
```

### 4. **Presentation Strategy**
- Explain GitHub Actions limitation
- Show local testing works perfectly
- Demonstrate pre-commit hook as alternative
- Highlight that the core analyzer is platform-agnostic
- Can be integrated with any CI/CD system (Jenkins, GitLab, etc.)

---

## Testing Checklist (Without GitHub Actions)

- [ ] Run analyzer locally on TestPRFile.java
- [ ] Verify all 20+ violations are detected
- [ ] Test blocking vs. non-blocking classification
- [ ] Install and test pre-commit hook
- [ ] Run manual PR review script
- [ ] Generate JSON report for analysis
- [ ] Take screenshots for demo
- [ ] Document results

---

## Benefits of This Approach

### ✅ Advantages:
1. **No dependency on GitHub Actions** - Works in any environment
2. **Faster feedback** - Pre-commit hooks catch issues immediately
3. **Offline capable** - Works without internet connection
4. **Flexible integration** - Can be used with any CI/CD system
5. **Developer-friendly** - Catches issues before push

### 🎯 For Hackathon:
- Shows adaptability and problem-solving
- Demonstrates platform-agnostic design
- Highlights multiple integration options
- Proves the core technology works regardless of CI/CD platform

---

## Next Steps

1. **Test locally** using the commands above
2. **Install pre-commit hook** for automatic checking
3. **Create manual review script** for PR analysis
4. **Document results** for hackathon presentation
5. **Prepare demo** showing local testing and pre-commit hook

---

## Need Help?

Run these commands to test everything:

```bash
# 1. Test analyzer
python src/analyzer/main.py analyze-file sample-java-project/src/main/java/com/ibm/demo/TestPRFile.java

# 2. Test on project
python src/analyzer/main.py analyze-project sample-java-project/src/main/java/

# 3. Generate report
python src/analyzer/main.py analyze-project sample-java-project/src/main/java/ --output demo-report.json

# 4. View report
cat demo-report.json | python -m json.tool
```

**The core analyzer works perfectly - we just need alternative integration methods!** 🚀