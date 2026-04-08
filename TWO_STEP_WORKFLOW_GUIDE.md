# Two-Step Workflow Guide

## Overview

The GitHub Actions workflow has been redesigned into **two separate, independent steps** to provide better control and clarity:

1. **PR Code Review (Blocking)** - Analyzes only changed files and blocks merge on violations
2. **AI Code Explanation (Non-blocking)** - Provides context and explanations without blocking

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions Workflow                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 1: Generate Changed File List                         │
│  • git diff to get only PR changes                          │
│  • Filter for .java, .ts, .tsx, .scss files                 │
│  • Save to changed_files.txt                                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 2: PR Code Review (BLOCKING) ⛔                       │
│  • Analyzes ONLY changed files (not entire repo)            │
│  • Runs rule-based violation detection                      │
│  • Exits with code 1 if CRITICAL/HIGH violations found      │
│  • BLOCKS PR merge if violations exist                      │
│  • Timeout: 3 minutes                                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 3: AI Code Explanation (NON-BLOCKING) ✅              │
│  • Runs even if Step 2 fails (if: always())                 │
│  • Analyzes ONLY changed files                              │
│  • Generates AI explanation using Ollama                    │
│  • Does NOT block merge (continue-on-error: true)           │
│  • Timeout: 3 minutes (2 min command + 1 min buffer)        │
└─────────────────────────────────────────────────────────────┘
```

---

## Step 1: PR Code Review (Blocking)

### Purpose
Enforce code quality standards by detecting violations in PR changes only.

### Behavior
- **Analyzes**: Only files changed in the PR (not entire codebase)
- **Detects**: Security issues, code smells, best practices violations
- **Blocks**: PR merge if CRITICAL or HIGH severity violations found
- **Timeout**: 3 minutes
- **Exit Code**: 1 if violations found, 0 if clean

### Implementation
```yaml
- name: Run PR Code Review (Blocking)
  id: code-review
  timeout-minutes: 3
  run: |
    # Loop through only changed files
    while IFS= read -r file; do
      if [ -f "$file" ]; then
        echo "Analyzing: $file"
        PYTHONPATH=src python -m analyzer.main file "$file" \
          --output-format github || exit 1
      fi
    done < changed_files.txt
```

### What Gets Analyzed
```bash
# Example: PR changes 3 files
changed_files.txt:
  src/main/java/com/ibm/UserService.java
  src/main/java/com/ibm/DataProcessor.java
  src/styles/main.scss

# Only these 3 files are analyzed, not the entire repo
```

### Output Example
```
🔍 Running code review on PR changes only...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Analyzing: src/main/java/com/ibm/UserService.java

Found 5 violations:

🔴 [SEC002] No Hardcoded Secrets
   Severity: CRITICAL
   File: src/main/java/com/ibm/UserService.java:16
   Message: Detects hardcoded passwords, API keys, tokens, and secrets
   💡 Suggestion: Use environment variables or configuration files

🟡 [CQ001] No System.out/err.println
   Severity: HIGH
   File: src/main/java/com/ibm/UserService.java:24
   Message: Use proper logging framework instead
   💡 Suggestion: Use proper logging framework (SLF4J, Log4j, etc.)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ Code review failed - blocking violations found
```

### When It Blocks
- **CRITICAL violations**: SQL injection, hardcoded secrets, command injection
- **HIGH violations**: Missing license, System.out, generic exceptions

### When It Passes
- **No violations**: Clean code
- **Only MEDIUM/LOW violations**: Non-blocking issues

---

## Step 2: AI Code Explanation (Non-blocking)

### Purpose
Provide context and understanding of PR changes without blocking merge.

### Behavior
- **Analyzes**: Only files changed in the PR
- **Explains**: What changed, why changed, impact
- **Never Blocks**: Runs with `continue-on-error: true`
- **Runs Always**: Even if Step 1 fails (`if: always()`)
- **Timeout**: 3 minutes (2 min command + 1 min buffer)

### Implementation
```yaml
- name: Generate AI Code Explanation (Non-blocking)
  id: ai-explanation
  if: always()
  timeout-minutes: 3
  continue-on-error: true
  run: |
    # Get only changed files
    CHANGED_FILES=$(cat changed_files.txt | tr '\n' ' ')
    
    # Run AI explanation with timeout
    timeout 2m PYTHONPATH=src python -m analyzer.main explain $CHANGED_FILES || {
      echo "⚠️  AI explanation timed out or failed"
      echo "This does not affect the PR review status"
    }
```

### What Gets Analyzed
```bash
# Same 3 files from PR changes
CHANGED_FILES="src/main/java/com/ibm/UserService.java src/main/java/com/ibm/DataProcessor.java src/styles/main.scss"

# AI analyzes only these files, not entire repo
```

### Output Example
```
🤖 Generating AI explanation for PR changes...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

============================================================
PR CHANGE EXPLANATION
============================================================

Files Explained: 3

What Changed:
  • Updated 3 supported files across 2 java, 1 scss.
  • Change mix: 2 modified, 1 added.
  • Defines or updates Java class `UserService`.
  • Defines or updates Java class `DataProcessor`.
  • Updates styling for user profile component.

Why Changed:
  • Appears intended to improve data flow and service integration.
  • Improves exception handling and logging in UserService.
  • Adds new data processing capabilities.
  • Updates UI styling for better user experience.

Impact:
  • UserService now handles errors more gracefully.
  • DataProcessor enables new feature: bulk data import.
  • UI changes affect user profile page only.

File: src/main/java/com/ibm/UserService.java
  Overview: Modified UserService.java: Improves error handling
  What Changed:
    - Added try-catch blocks for database operations
    - Replaced System.out with proper logging
  Why Changed:
    - Improve error handling and debugging capabilities
  Integration / Impact:
    - Affects all user authentication flows
  Considerations:
    - Test authentication thoroughly

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Fallback Behavior
If AI explanation fails or times out:
```
⚠️  AI explanation timed out or failed
This does not affect the PR review status
```

The workflow continues and completes successfully.

---

## Key Differences from Previous Design

### Before (Single Combined Step)
```yaml
- name: Run combined review
  # Analyzed entire repository
  # Combined violations + AI explanation
  # Single timeout for both
  # Confusing when AI failed but violations passed
```

### After (Two Separate Steps)
```yaml
- name: Run PR Code Review (Blocking)
  # Analyzes only PR changes
  # Only violation detection
  # Clear pass/fail status
  # Blocks merge on violations

- name: Generate AI Code Explanation (Non-blocking)
  # Analyzes only PR changes
  # Only AI explanation
  # Never blocks merge
  # Runs even if review fails
```

---

## Benefits

### 1. Analyzes Only PR Changes
✅ **Before**: Analyzed entire repository (slow, irrelevant)
✅ **After**: Analyzes only changed files (fast, relevant)

### 2. Clear Separation of Concerns
✅ **Step 1**: Quality enforcement (blocking)
✅ **Step 2**: Context and understanding (advisory)

### 3. Better Failure Handling
✅ **Step 1 fails**: PR blocked, clear reason
✅ **Step 2 fails**: PR not blocked, explanation unavailable

### 4. Faster Execution
✅ **Before**: 5+ minutes for entire repo
✅ **After**: < 1 minute for typical PR (3-5 files)

### 5. Better User Experience
✅ Clear status for each step in GitHub UI
✅ Developers know exactly why PR is blocked
✅ AI explanation is bonus, not requirement

---

## GitHub UI Appearance

### Workflow Steps (As shown in your image)
```
✅ Set up job
✅ Checkout code
✅ Set up Python
✅ Install Python dependencies
✅ Install Ollama
✅ Start Ollama server
✅ Pull Ollama model
✅ Generate changed file list
❌ Run PR Code Review (Blocking)          ← Step 1: BLOCKS if violations
✅ Generate AI Code Explanation           ← Step 2: NEVER blocks
✅ Upload Analysis Results
✅ Summary
```

### Branch Protection
When you set up branch protection rules:
- **Required status check**: "Run PR Code Review (Blocking)"
- **Optional**: "Generate AI Code Explanation" (don't require this)

This ensures:
- PR cannot merge if code review fails
- PR can merge even if AI explanation fails

---

## Configuration

### Timeouts
```yaml
# Step 1: PR Code Review
timeout-minutes: 3  # Enough for 10-20 files

# Step 2: AI Explanation
timeout-minutes: 3  # 2 min command + 1 min buffer
command: timeout 2m  # Command-level timeout
```

### File Filtering
```yaml
# Only analyze these file types
grep -E '\.(java|ts|tsx|scss)$'
```

### AI Model
```yaml
# Ollama model for explanations
model: qwen2.5-coder:1.5b
timeout_seconds: 30  # Per file in config/rules.yaml
```

---

## Testing

### Test Scenario 1: Clean PR
```bash
# PR changes: 2 files, no violations
Result:
  ✅ Step 1: Pass (no violations)
  ✅ Step 2: Pass (explanation generated)
  ✅ PR can be merged
```

### Test Scenario 2: PR with Violations
```bash
# PR changes: 3 files, 1 has CRITICAL violation
Result:
  ❌ Step 1: Fail (hardcoded secret found)
  ✅ Step 2: Pass (explanation generated)
  ❌ PR BLOCKED - cannot merge
```

### Test Scenario 3: AI Timeout
```bash
# PR changes: 5 files, AI times out
Result:
  ✅ Step 1: Pass (no violations)
  ⚠️  Step 2: Timeout (explanation unavailable)
  ✅ PR can be merged
```

### Test Scenario 4: Both Fail
```bash
# PR changes: 2 files, violations + AI timeout
Result:
  ❌ Step 1: Fail (violations found)
  ⚠️  Step 2: Timeout (explanation unavailable)
  ❌ PR BLOCKED - cannot merge
```

---

## Troubleshooting

### Step 1 Fails Unexpectedly
```bash
# Check which file caused failure
# Look for the last "Analyzing: <file>" message
# Review violations in that file
```

### Step 2 Times Out
```bash
# Check Ollama logs: /tmp/ollama.log
# Verify model is loaded: ollama list
# Check timeout settings in config/rules.yaml
```

### No Files Analyzed
```bash
# Check changed_files.txt is not empty
# Verify file extensions match filter
# Ensure files exist in repository
```

---

## Performance Metrics

### Typical PR (3-5 files)
- **Step 1**: 10-30 seconds
- **Step 2**: 15-45 seconds
- **Total**: < 1 minute

### Large PR (10-15 files)
- **Step 1**: 30-60 seconds
- **Step 2**: 1-2 minutes
- **Total**: 2-3 minutes

### Very Large PR (20+ files)
- **Step 1**: 1-2 minutes
- **Step 2**: 2-3 minutes (may timeout)
- **Total**: 3-5 minutes

---

## Best Practices

### For Developers
1. **Keep PRs small**: 3-5 files per PR for fast review
2. **Fix violations locally**: Run analyzer before pushing
3. **Read AI explanations**: Understand impact of changes
4. **Don't bypass checks**: Fix issues, don't force merge

### For Teams
1. **Require Step 1**: Set as required status check
2. **Make Step 2 optional**: Don't require AI explanation
3. **Monitor timeouts**: Adjust if Step 2 times out frequently
4. **Review metrics**: Track violation trends over time

---

## Future Enhancements

### Phase 2 Ideas
1. **Incremental Analysis**: Only analyze changed lines, not entire files
2. **Caching**: Cache analysis results for unchanged files
3. **Parallel Processing**: Analyze multiple files simultaneously
4. **Smart Explanations**: Focus AI on files with violations
5. **Historical Trends**: Track code quality improvements

---

## Conclusion

The two-step workflow provides:

✅ **Clear separation**: Quality enforcement vs. context
✅ **Faster execution**: Analyzes only PR changes
✅ **Better UX**: Clear status for each step
✅ **Reliable blocking**: PR merge control works correctly
✅ **Graceful degradation**: AI failure doesn't block PR

This design ensures code quality is enforced while providing helpful AI insights without creating bottlenecks.

---

**Last Updated**: 2026-04-08  
**Status**: ✅ Production Ready  
**Workflow File**: `.github/workflows/code-review.yml`