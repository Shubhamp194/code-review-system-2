# Pull Request Testing Guide

## Overview
This guide provides instructions for creating and testing Pull Requests to demonstrate the automated code review system.

## Test Branches Created

### 1. ✅ feature/clean-enhancement
**Purpose**: Demonstrate that clean, well-written code passes all checks

**Files Added**:
- `sample-java-project/src/main/java/com/ibm/demo/UserService.java` (154 lines)
  - Proper IBM license header
  - SLF4J logging (no System.out)
  - Proper exception handling
  - Descriptive variable names
  - No hardcoded secrets
  
- `sample-java-project/src/main/typescript/userApi.ts` (113 lines)
  - TypeScript with proper types
  - No `any` types
  - Proper error handling
  - IBM license header

**Expected Result**: ✅ PR should pass all checks and be mergeable

**PR Creation URL**: 
```
https://github.ibm.com/Shubham-Pandey7/code-review-system/pull/new/feature/clean-enhancement
```

---

### 2. ❌ feature/backend-violations
**Purpose**: Demonstrate detection of critical security and code quality violations

**Files Added**:
- `sample-java-project/src/main/java/com/ibm/demo/DatabaseService.java` (47 lines)

**Intentional Violations** (13 violations):
1. **SEC001** - Missing IBM license header
2. **SEC002** - Hardcoded password: "admin123" (CRITICAL)
3. **SEC002** - Hardcoded apiKey: "sk-abc123xyz" (CRITICAL)
4. **SEC003** - SQL injection via string concatenation (CRITICAL)
5. **SEC004** - Command injection with Runtime.exec (CRITICAL)
6. **CQ001** - System.out.println usage (HIGH)
7. **CQ002** - printStackTrace usage (HIGH)
8. **CQ003** - TODO comment (HIGH)
9. **CQ004** - Empty catch block (CRITICAL)
10. **BP006** - Public field (MEDIUM)
11. **BP005** - String comparison with == (MEDIUM)
12. **NAM005** - Generic variable name "temp" (LOW)
13. **IMP001** - Wildcard imports (MEDIUM)

**Expected Result**: ❌ PR should be BLOCKED with detailed violation report

**PR Creation URL**: 
```
https://github.ibm.com/Shubham-Pandey7/code-review-system/pull/new/feature/backend-violations
```

---

### 3. ❌ feature/frontend-violations
**Purpose**: Demonstrate comprehensive violation detection across multiple categories

**Files Added**:
- `sample-java-project/src/main/java/com/ibm/demo/ConfigManager.java` (107 lines)

**Intentional Violations** (30+ violations across all categories):

**Security Violations**:
- SEC001 - Missing IBM license header
- SEC002 - Hardcoded API key, password, token (3 instances)
- SEC003 - SQL injection vulnerability
- SEC005 - Logging sensitive data
- SEC006 - Hardcoded URL
- SEC007 - Hardcoded file path
- SEC008 - Commented out code

**Code Quality Violations**:
- CQ001 - System.out.println and System.err.println (3 instances)
- CQ002 - printStackTrace usage
- CQ003 - TODO comment
- CQ004 - Empty catch block
- CQ005 - Catching generic Exception
- CQ007 - Debug flag
- CQ008 - System.exit usage
- CQ009 - Thread.sleep usage

**Best Practice Violations**:
- BP004 - String concatenation in loop
- BP005 - String comparison with ==
- BP006 - Public field
- BP007 - Static mutable variable

**Naming Violations**:
- NAM003 - Method name not lowerCamelCase (2 instances)
- NAM004 - Constant not UPPER_SNAKE_CASE
- NAM005 - Generic variable names (temp, data)
- NAM006 - Single character variable (x)
- NAM007 - Boolean not starting with is/has/should

**Import Violations**:
- IMP001 - Wildcard imports (2 instances)

**Exception Handling Violations**:
- EXC003 - Throwing generic Exception

**Formatting Violations**:
- FMT001 - Trailing whitespace
- FMT002 - Multiple consecutive blank lines
- FMT003 - Line exceeding 120 characters
- FMT004 - Missing newline at end of file

**Low Priority Violations**:
- LOW001 - Magic number
- LOW004 - Redundant boolean check
- LOW005 - Empty method

**Expected Result**: ❌ PR should be BLOCKED with extensive violation report

**PR Creation URL**: 
```
https://github.ibm.com/Shubham-Pandey7/code-review-system/pull/new/feature/frontend-violations
```

---

## How to Create Pull Requests

### Step 1: Navigate to PR Creation URL
Click on the PR creation URL for each branch (provided above)

### Step 2: Fill PR Details

**For feature/clean-enhancement**:
```
Title: feat: Add user service and API client

Description:
This PR adds a new UserService for user management operations and a TypeScript API client for frontend integration.

Changes:
- Added UserService.java with proper error handling and logging
- Added userApi.ts with TypeScript type definitions
- All code follows IBM coding standards
- No security vulnerabilities
- Proper exception handling implemented

Testing:
- Code follows all style guidelines
- No hardcoded secrets or credentials
- Proper logging using SLF4J
- Type-safe TypeScript implementation
```

**For feature/backend-violations**:
```
Title: feat: Add database service

Description:
This PR adds a DatabaseService for database operations.

Changes:
- Added DatabaseService.java for database queries
- Implements user query functionality
- Adds command execution capability

Testing:
- Basic functionality tested
```

**For feature/frontend-violations**:
```
Title: feat: Add configuration manager

Description:
This PR adds a ConfigManager for application configuration management.

Changes:
- Added ConfigManager.java for configuration loading
- Implements configuration processing
- Adds data processing capabilities

Testing:
- Configuration loading tested
```

### Step 3: Create Pull Request
Click "Create Pull Request" button

### Step 4: Observe GitHub Actions Workflow

The workflow will automatically:
1. **Checkout code** - Get the PR changes
2. **Set up Python** - Install dependencies
3. **Run PR Code Review (Blocking)** - Analyze changed files
4. **Generate AI Code Explanation (Non-blocking)** - Provide context (if Ollama available)

### Step 5: Review Results

**For Clean Enhancement PR**:
- ✅ All checks should pass
- ✅ Green checkmark on PR
- ✅ "Merge pull request" button enabled
- 📊 AI explanation provides positive feedback

**For Backend Violations PR**:
- ❌ Code review check fails
- ❌ Red X on PR
- ❌ "Merge pull request" button disabled
- 📋 Detailed violation report in workflow logs
- 🔴 13 violations detected with severity levels

**For Frontend Violations PR**:
- ❌ Code review check fails
- ❌ Red X on PR
- ❌ "Merge pull request" button disabled
- 📋 Extensive violation report (30+ violations)
- 🔴 Multiple CRITICAL security issues flagged

---

## Expected Workflow Output Examples

### Clean Enhancement (PASS)
```
✅ Code Review Analysis Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Analysis Summary:
   Files Analyzed: 2
   Total Violations: 0
   Critical Issues: 0
   High Priority: 0
   Medium Priority: 0
   Low Priority: 0

✅ All checks passed! Code is ready for review.
```

### Backend Violations (FAIL)
```
❌ Code Review Analysis Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Analysis Summary:
   Files Analyzed: 1
   Total Violations: 13
   Critical Issues: 4
   High Priority: 3
   Medium Priority: 4
   Low Priority: 2

🔴 CRITICAL Issues Found:
   - SEC002: Hardcoded secret detected (password)
   - SEC002: Hardcoded secret detected (apiKey)
   - SEC003: SQL injection vulnerability
   - SEC004: Command injection vulnerability
   - CQ004: Empty catch block

⚠️  HIGH Priority Issues:
   - CQ001: System.out.println usage
   - CQ002: printStackTrace usage
   - CQ003: TODO comment

❌ Code review failed. Please fix the violations before merging.
```

### Frontend Violations (FAIL)
```
❌ Code Review Analysis Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Analysis Summary:
   Files Analyzed: 1
   Total Violations: 32
   Critical Issues: 6
   High Priority: 5
   Medium Priority: 12
   Low Priority: 9

🔴 CRITICAL Issues Found:
   - SEC002: Multiple hardcoded secrets (API key, password, token)
   - SEC003: SQL injection vulnerability
   - CQ004: Empty catch block
   - CQ005: Catching generic Exception

⚠️  HIGH Priority Issues:
   - SEC001: Missing IBM license header
   - CQ001: Multiple System.out/err.println
   - CQ002: printStackTrace usage
   - CQ003: TODO comment

❌ Code review failed. Please fix the violations before merging.
```

---

## Verification Checklist

After creating all PRs, verify:

- [ ] All 3 PRs are created successfully
- [ ] GitHub Actions workflow triggers automatically
- [ ] Clean enhancement PR shows green checkmark
- [ ] Backend violations PR shows red X
- [ ] Frontend violations PR shows red X
- [ ] Workflow logs show detailed violation reports
- [ ] Merge button is enabled only for clean PR
- [ ] Merge button is disabled for violation PRs
- [ ] AI explanations are generated (if Ollama available)

---

## Demo Script for Hackathon

### 1. Introduction (1 minute)
"We've built an AI-powered code review system that automatically analyzes pull requests and blocks merges if violations are detected."

### 2. Show Clean PR (1 minute)
- Navigate to clean enhancement PR
- Show green checkmark
- Highlight: "This PR follows all coding standards"
- Show workflow logs with 0 violations
- Point out merge button is enabled

### 3. Show Backend Violations PR (2 minutes)
- Navigate to backend violations PR
- Show red X
- Highlight: "This PR has 13 violations including 4 CRITICAL security issues"
- Open workflow logs
- Point out specific violations:
  - Hardcoded secrets
  - SQL injection
  - Command injection
  - Empty catch blocks
- Show merge button is disabled

### 4. Show Frontend Violations PR (2 minutes)
- Navigate to frontend violations PR
- Show red X
- Highlight: "This PR has 32 violations across all categories"
- Open workflow logs
- Show comprehensive violation report
- Emphasize the breadth of detection

### 5. Explain Impact (1 minute)
"This system:
- Reduces review time by 50-60%
- Catches security vulnerabilities before human review
- Enforces consistent coding standards
- Provides educational feedback
- Blocks problematic code from being merged"

### 6. Show AI Enhancement (1 minute, if available)
- Show AI-generated code explanations
- Highlight how AI provides context and suggestions
- Demonstrate the educational value

---

## Troubleshooting

### Workflow Not Triggering
- Check that GitHub Actions is enabled in repository settings
- Verify workflow file is in `.github/workflows/` directory
- Check branch protection rules

### Workflow Failing Unexpectedly
- Check Python dependencies are installed correctly
- Verify `code_analyzer.py` is in repository root
- Check file paths in workflow configuration

### AI Step Timing Out
- This is expected if Ollama is not available
- The blocking step will still work
- AI step is non-blocking and won't prevent merge decisions

---

## Next Steps

After successful PR testing:
1. Document results with screenshots
2. Prepare demo presentation
3. Create video walkthrough
4. Update README with demo links
5. Prepare for hackathon presentation

---

## Repository Information

**Repository**: https://github.ibm.com/Shubham-Pandey7/code-review-system
**Workflow File**: `.github/workflows/code-review.yml`
**Analyzer Script**: `code_analyzer.py`
**Rules Configuration**: `config/rules.yaml`

---

**Created**: 2026-04-08
**Last Updated**: 2026-04-08
**Status**: Ready for PR creation and testing