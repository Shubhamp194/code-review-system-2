# Create Test Pull Request - Step by Step Guide

## ✅ Current Status
- ✅ Test branch created: `test-pr-with-violations`
- ✅ Test file added: `TestPRFile.java` with 20+ intentional violations
- ✅ Changes committed and pushed to GitHub
- ✅ Branch available at: https://github.ibm.com/Shubham-Pandey7/code-review-system/tree/test-pr-with-violations

## 🎯 Next Steps: Create the Pull Request

### Step 1: Navigate to Create PR Page

**Option A: Use the Direct Link (Easiest)**
Click this link to create the PR directly:
```
https://github.ibm.com/Shubham-Pandey7/code-review-system/pull/new/test-pr-with-violations
```

**Option B: Through Repository Interface**
1. Go to: https://github.ibm.com/Shubham-Pandey7/code-review-system
2. You should see a yellow banner: "test-pr-with-violations had recent pushes"
3. Click the green **"Compare & pull request"** button

**Option C: Through Pull Requests Tab**
1. Go to: https://github.ibm.com/Shubham-Pandey7/code-review-system/pulls
2. Click **"New pull request"**
3. Select base: `main` and compare: `test-pr-with-violations`
4. Click **"Create pull request"**

### Step 2: Fill in PR Details

**Title:**
```
Test PR: Verify Automated Code Review System
```

**Description:**
```markdown
## 🧪 Test Pull Request

This PR tests the automated code review system with intentional code violations.

### Purpose
- Verify GitHub Actions workflow triggers correctly
- Test violation detection across all severity levels
- Validate PR comment generation
- Confirm merge blocking for critical issues

### Test File Added
- `sample-java-project/src/main/java/com/ibm/demo/TestPRFile.java`

### Expected Violations (20+)

#### Critical (3) - Should BLOCK merge ❌
1. Missing IBM license header
2. Hardcoded password: `password = "mySecretPassword123"`
3. Hardcoded API key: `apiKey = "sk-1234567890abcdef"`
4. SQL injection vulnerability: String concatenation in query

#### High Priority (8)
- System.out.println usage
- System.err.println usage
- Empty catch block
- Generic Exception catch
- printStackTrace() usage
- TODO comment
- Hardcoded URL
- Commented-out code

#### Medium Priority (6)
- Public field exposure
- Static mutable variable
- String concatenation in loop
- Using == for String comparison
- Debug flag
- Poor variable naming (temp, obj, x)

#### Low Priority (3)
- Magic number (12345)
- Empty method
- Method naming violation (Process_Data)

### What to Watch For

1. **GitHub Actions Workflow**
   - Should trigger automatically within 10 seconds
   - Check "Actions" tab for workflow run
   - Should complete in 30-60 seconds

2. **Status Check**
   - Should show ❌ (failed) due to blocking violations
   - Check "Checks" tab for detailed results

3. **PR Comment**
   - Bot should post a comment with violation details
   - Should list all violations by severity
   - Should indicate merge is blocked

4. **Merge Button**
   - Should be disabled or show warning
   - Message: "Merging is blocked" (if branch protection enabled)

### Success Criteria
- ✅ Workflow runs automatically
- ✅ All 20+ violations detected
- ✅ Critical violations flagged as blocking
- ✅ PR comment posted with results
- ✅ Status check fails (red X)
- ✅ Merge blocked for critical issues

---

**Note:** This is a test PR. Do NOT merge. Close after verification.
```

### Step 3: Create the Pull Request

1. Review the PR details
2. Click the green **"Create pull request"** button
3. Wait for the magic to happen! ✨

## 📊 What Happens Next (Timeline)

### Immediate (0-10 seconds)
- ✅ PR created successfully
- ✅ GitHub detects the PR event
- ✅ Workflow queued in Actions tab

### During Execution (30-60 seconds)
You can watch the workflow in real-time:
1. Go to **Actions** tab
2. Click on the running workflow: "Code Review"
3. Click on the job: "analyze"
4. Watch the logs as it:
   - Sets up Python
   - Installs dependencies
   - Analyzes the Java file
   - Detects violations
   - Posts results

### After Completion (60+ seconds)
1. **Status Check Updated**
   - Red X (❌) appears next to commit
   - Status: "Code Review — Failed"

2. **PR Comment Posted**
   - Bot posts detailed violation report
   - Lists all issues by severity
   - Provides line numbers and descriptions

3. **Checks Tab Updated**
   - Shows detailed results
   - Click "Details" to see full analysis

4. **Merge Status**
   - Merge button shows warning
   - "Merging is blocked" (if branch protection enabled)

## 🔍 How to Verify Everything Works

### Check 1: Workflow Triggered
```
✅ Go to: Actions tab
✅ See: "Code Review" workflow running
✅ Status: Yellow dot → Green check or Red X
```

### Check 2: Violations Detected
```
✅ Go to: PR → Checks tab
✅ Click: "Code Review" → "Details"
✅ See: List of all violations with line numbers
```

### Check 3: PR Comment Posted
```
✅ Go to: PR → Conversation tab
✅ See: Bot comment with violation summary
✅ Contains: Critical, High, Medium, Low violations
```

### Check 4: Status Check Failed
```
✅ Go to: PR → Conversation tab
✅ See: Red X next to commit
✅ Status: "Some checks were not successful"
```

### Check 5: Merge Blocked (if branch protection enabled)
```
✅ Go to: PR → Conversation tab
✅ See: "Merging is blocked"
✅ Reason: "Required status check 'code-review' has not succeeded"
```

## 🐛 Troubleshooting

### Workflow Not Triggering?

**Symptom:** No workflow appears in Actions tab after 30 seconds

**Solutions:**
1. Check GitHub Actions is enabled:
   - Settings → Actions → General
   - Ensure "Allow all actions" is selected

2. Verify workflow file exists:
   - Check `.github/workflows/code-review.yml` in repository

3. Check workflow permissions:
   - Settings → Actions → General → Workflow permissions
   - Select "Read and write permissions"

4. Manually trigger workflow:
   - Actions tab → "Code Review" → "Run workflow"

### Workflow Failing with Errors?

**Symptom:** Workflow runs but fails with error

**Common Issues:**

1. **Python Import Error**
   ```
   Error: ModuleNotFoundError: No module named 'colorama'
   ```
   **Fix:** Check `requirements.txt` exists and contains all dependencies

2. **Permission Error**
   ```
   Error: Resource not accessible by integration
   ```
   **Fix:** Enable write permissions in Settings → Actions → General

3. **File Not Found**
   ```
   Error: No such file or directory: 'config/rules.yaml'
   ```
   **Fix:** Verify all files are committed and pushed to repository

### No PR Comment Posted?

**Symptom:** Workflow succeeds but no comment appears

**Solutions:**
1. Check workflow logs for errors in "Post results" step
2. Verify GITHUB_TOKEN has write permissions
3. Check if Java files were actually changed in the PR
4. Look for comment in "Checks" tab instead

### Status Check Not Appearing?

**Symptom:** No status check shown on PR

**Solutions:**
1. Wait 1-2 minutes for first run to complete
2. Check Actions tab for workflow status
3. Verify workflow completed successfully
4. Refresh the PR page

## 📋 Before Creating PR - Configuration Checklist

Make sure you've completed these configurations (see GITHUB_CONFIGURATION_GUIDE.md):

- [ ] GitHub Actions enabled
- [ ] Workflow permissions set to "Read and write"
- [ ] Workflow file exists at `.github/workflows/code-review.yml`
- [ ] Python analyzer code exists in `src/analyzer/`
- [ ] Rule configuration exists at `config/rules.yaml`
- [ ] `requirements.txt` exists in repository root

## 🎬 After PR Creation - What to Do

### 1. Monitor the Workflow (First 2 minutes)
- Watch Actions tab for workflow execution
- Check for any errors in logs
- Verify it completes successfully

### 2. Review the Results (After completion)
- Read the PR comment with violations
- Check the Checks tab for details
- Verify all expected violations are detected

### 3. Test Merge Blocking (Optional)
- Try to click "Merge pull request"
- Should see warning or disabled button
- Confirms critical violations block merge

### 4. Document Findings
- Take screenshots of:
  - Workflow execution
  - PR comment with violations
  - Status check results
  - Merge blocking message
- Use for hackathon presentation!

### 5. Clean Up (After testing)
- Close the PR (don't merge)
- Optionally delete the test branch
- Keep for demo purposes if needed

## 🚀 Ready to Create the PR?

**Quick Start:**
1. Click: https://github.ibm.com/Shubham-Pandey7/code-review-system/pull/new/test-pr-with-violations
2. Copy the title and description from Step 2 above
3. Click "Create pull request"
4. Watch the automation work! 🎉

## 📞 Need Help?

If something doesn't work:
1. Check the troubleshooting section above
2. Review workflow logs in Actions tab
3. Verify all configuration steps completed
4. Check GITHUB_CONFIGURATION_GUIDE.md for detailed setup

---

**Good luck with your test PR!** 🎯

The automated code review system should detect all 20+ violations and demonstrate the power of AI-assisted code quality enforcement.