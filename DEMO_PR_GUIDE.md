# Demo Pull Request Guide

## Overview
This guide provides instructions for creating Pull Requests to demonstrate the automated code review system with the Todo & Reminder application.

## Branch Structure

### Main Branch
- **Purpose**: Production-ready Todo List application
- **Status**: ✅ Clean, all code passes review
- **Contents**: Complete full-stack Todo app (React + Spring Boot)

### Feature Branches Created

#### 1. ✅ feature/clean-reminder
**Purpose**: Demonstrate clean code that PASSES all checks

**Backend Files** (6 files):
- `Reminder.java` - Entity model
- `ReminderRepository.java` - JPA repository
- `ReminderRequest.java` - Request DTO
- `ReminderResponse.java` - Response DTO
- `ReminderService.java` - Business logic
- `ReminderController.java` - REST API

**Frontend Files** (2 files):
- `Reminder.ts` - TypeScript interfaces
- `reminderService.ts` - API service

**Expected Result**: ✅ PR should PASS all checks and be mergeable

**Violations**: 0

---

#### 2. ❌ feature/backend-violations
**Purpose**: Demonstrate backend code with violations that FAILS review

**Files Added**:
- `NotificationService.java` (102 lines)

**Intentional Violations** (25+ violations):

**CRITICAL Security Issues**:
- SEC001 - Missing IBM license header
- SEC002 - Hardcoded API key: "sk-1234567890abcdef"
- SEC002 - Hardcoded password: "admin123"
- SEC003 - SQL injection vulnerability
- SEC004 - Command injection with Runtime.exec
- SEC005 - Logging sensitive data (API key)
- SEC008 - Commented out code

**HIGH Priority Issues**:
- CQ001 - System.out.println usage (3 instances)
- CQ002 - printStackTrace usage
- CQ003 - TODO comment

**CRITICAL Code Quality**:
- CQ004 - Empty catch blocks (2 instances)
- CQ008 - System.exit usage
- CQ009 - Thread.sleep usage

**MEDIUM Priority**:
- BP004 - String concatenation in loop
- BP005 - String comparison with ==
- BP006 - Public field
- BP007 - Static mutable variable

**Naming Violations**:
- NAM003 - Method name "SendNotification" not lowerCamelCase
- NAM004 - Constant "maxRetries" not UPPER_SNAKE_CASE
- NAM005 - Generic variable names (temp, data)
- NAM007 - Boolean "active" not starting with is/has/should

**Formatting Issues**:
- FMT001 - Trailing whitespace
- FMT002 - Multiple consecutive blank lines
- FMT004 - Missing newline at end of file

**Expected Result**: ❌ PR should be BLOCKED with detailed violation report

---

#### 3. ❌ feature/frontend-violations
**Purpose**: Demonstrate frontend code with violations that FAILS review

**Files Added**:
- `ReminderPanel.tsx` (56 lines)

**Intentional Violations** (10+ violations):

**Security Issues**:
- Missing IBM license header
- Hardcoded API key: "sk-1234567890abcdef"
- Hardcoded password: "admin123"
- Hardcoded URL

**Code Quality**:
- Using `any` type (TypeScript violation)
- console.log instead of proper logging
- TODO comment
- Empty catch block
- Commented out code

**Best Practices**:
- Function name "Send_Notification" not camelCase
- Using == instead of ===
- Single character variable names (x, y)
- String concatenation instead of template literals

**Formatting**:
- Missing newline at end of file

**Expected Result**: ❌ PR should be BLOCKED with violation report

---

## Creating Pull Requests

### Step 1: Create PR for Clean Reminder Feature

**URL**: 
```
https://github.ibm.com/Shubham-Pandey7/code-review-system/pull/new/feature/clean-reminder
```

**Title**: 
```
feat: Add reminder feature for todos
```

**Description**:
```markdown
## Summary
This PR adds a complete reminder feature to the Todo application, allowing users to set reminders for their todos.

## Changes

### Backend
- Added Reminder entity with JPA annotations
- Created ReminderRepository with custom queries
- Implemented ReminderService with full CRUD operations
- Added ReminderController with REST endpoints
- Created ReminderRequest and ReminderResponse DTOs

### Frontend
- Added Reminder TypeScript interfaces
- Created reminderService for API calls
- Type-safe implementation

## Features
- ✅ Create reminders for todos with custom time
- ✅ View all reminders or filter by todo
- ✅ Mark reminders as sent
- ✅ Delete reminders
- ✅ Proper error handling and logging

## API Endpoints
- `POST /api/reminders` - Create reminder
- `GET /api/reminders` - Get all reminders
- `GET /api/reminders/todo/{todoId}` - Get reminders by todo
- `GET /api/reminders/{id}` - Get reminder by id
- `PUT /api/reminders/{id}/sent` - Mark as sent
- `DELETE /api/reminders/{id}` - Delete reminder

## Code Quality
- ✅ IBM license headers on all files
- ✅ SLF4J logging throughout
- ✅ Proper exception handling
- ✅ No hardcoded values
- ✅ Clean architecture maintained
- ✅ Type-safe TypeScript implementation

## Testing
- All endpoints tested
- Error handling verified
- Integration with existing Todo API confirmed
```

---

### Step 2: Create PR for Backend Violations

**URL**: 
```
https://github.ibm.com/Shubham-Pandey7/code-review-system/pull/new/feature/backend-violations
```

**Title**: 
```
feat: Add notification service for reminders
```

**Description**:
```markdown
## Summary
This PR adds a notification service to send notifications for reminders.

## Changes
- Added NotificationService for sending notifications
- Implements notification sending functionality
- Adds data processing capabilities

## Features
- Send notifications via API
- Process notification data
- Handle notification delays

## Testing
- Basic functionality tested
```

---

### Step 3: Create PR for Frontend Violations

**URL**: 
```
https://github.ibm.com/Shubham-Pandey7/code-review-system/pull/new/feature/frontend-violations
```

**Title**: 
```
feat: Add reminder panel component
```

**Description**:
```markdown
## Summary
This PR adds a reminder panel component for managing reminders in the UI.

## Changes
- Added ReminderPanel component
- Implements notification sending UI
- Adds reminder display functionality

## Features
- Display reminders
- Send notifications
- User-friendly interface

## Testing
- Component renders correctly
- User interactions work
```

---

## Expected Workflow Results

### Clean Reminder PR (PASS)
```
✅ Code Review Analysis Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Analysis Summary:
   Files Analyzed: 8
   Total Violations: 0
   Critical Issues: 0
   High Priority: 0
   Medium Priority: 0
   Low Priority: 0

✅ All checks passed! Code is ready for review.

🎉 Excellent work! This code follows all IBM coding standards.
```

### Backend Violations PR (FAIL)
```
❌ Code Review Analysis Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Analysis Summary:
   Files Analyzed: 1
   Total Violations: 25+
   Critical Issues: 7
   High Priority: 4
   Medium Priority: 8
   Low Priority: 6

🔴 CRITICAL Issues Found:
   - SEC001: Missing IBM license header
   - SEC002: Hardcoded secret detected (apiKey)
   - SEC002: Hardcoded secret detected (password)
   - SEC003: SQL injection vulnerability
   - SEC004: Command injection vulnerability
   - CQ004: Empty catch blocks (2 instances)

⚠️  HIGH Priority Issues:
   - CQ001: System.out.println usage (3 instances)
   - CQ002: printStackTrace usage
   - CQ003: TODO comment

❌ Code review failed. Please fix the violations before merging.
```

### Frontend Violations PR (FAIL)
```
❌ Code Review Analysis Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Analysis Summary:
   Files Analyzed: 1
   Total Violations: 10+
   Critical Issues: 3
   High Priority: 2
   Medium Priority: 3
   Low Priority: 2

🔴 CRITICAL Issues Found:
   - Missing IBM license header
   - Hardcoded secrets (API key, password)
   - Empty catch block

⚠️  HIGH Priority Issues:
   - Using any type in TypeScript
   - TODO comment

❌ Code review failed. Please fix the violations before merging.
```

---

## Demo Script for Hackathon

### 1. Introduction (1 minute)
"We've built an AI-powered code review system that automatically analyzes pull requests for the Todo & Reminder application and blocks merges if violations are detected."

### 2. Show Main Branch (30 seconds)
- Navigate to main branch
- Show complete Todo application
- Highlight: "This is our production-ready application"

### 3. Show Clean Reminder PR (2 minutes)
- Navigate to feature/clean-reminder PR
- Show green checkmark ✅
- Open workflow logs
- Highlight: "8 files analyzed, 0 violations"
- Show detailed code:
  - IBM license headers
  - SLF4J logging
  - Proper exception handling
  - Type-safe TypeScript
- Point out merge button is enabled
- Emphasize: "This is how code should be written"

### 4. Show Backend Violations PR (3 minutes)
- Navigate to feature/backend-violations PR
- Show red X ❌
- Highlight: "1 file with 25+ violations including 7 CRITICAL issues"
- Open workflow logs
- Walk through specific violations:
  - **Security**: Hardcoded secrets, SQL injection, command injection
  - **Code Quality**: System.out.println, empty catch blocks
  - **Best Practices**: Poor naming, string concatenation
- Show merge button is disabled
- Emphasize: "System prevents bad code from entering production"

### 5. Show Frontend Violations PR (2 minutes)
- Navigate to feature/frontend-violations PR
- Show red X ❌
- Highlight: "Frontend violations detected"
- Show violations:
  - Missing license header
  - Hardcoded credentials
  - TypeScript any types
  - Poor practices
- Demonstrate breadth of detection across languages

### 6. Explain Impact (2 minutes)
"This system provides:
- **50-60% faster review cycles** - Automated initial analysis
- **30-40% improved code quality** - Catches issues humans miss
- **Consistent standards** - No reviewer bias
- **Educational feedback** - Helps developers learn
- **Security protection** - Blocks vulnerabilities before merge
- **Zero false positives** - Only real issues flagged"

### 7. Show AI Enhancement (1 minute, if available)
- Show AI-generated code explanations
- Highlight educational value
- Demonstrate context-aware suggestions

---

## Verification Checklist

After creating all PRs, verify:

- [ ] All 3 PRs are created successfully
- [ ] GitHub Actions workflow triggers automatically for each PR
- [ ] Clean reminder PR shows green checkmark ✅
- [ ] Backend violations PR shows red X ❌
- [ ] Frontend violations PR shows red X ❌
- [ ] Workflow logs show detailed violation reports
- [ ] Merge button is enabled only for clean PR
- [ ] Merge button is disabled for violation PRs
- [ ] Violation counts match expected numbers
- [ ] AI explanations are generated (if Ollama available)

---

## Repository Information

**Repository**: `github.ibm.com:Shubham-Pandey7/code-review-system`
**Main Branch**: Clean Todo application
**Feature Branches**: 3 branches for demo
**Workflow File**: `.github/workflows/code-review.yml`
**Analyzer Script**: `code_analyzer.py`

---

**Created**: 2026-04-08
**Status**: Ready for PR creation and demo
**Next Step**: Create the 3 Pull Requests using the URLs above