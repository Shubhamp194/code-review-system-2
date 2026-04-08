# Branch Protection Setup Guide

## 🛡️ How to Block PR Merging When Code Review Fails

This guide shows you how to configure GitHub branch protection rules to prevent merging PRs when the AI Code Review workflow fails (shows red X).

---

## 📋 Prerequisites

- Repository admin access
- GitHub Actions workflow running successfully
- At least one workflow run completed (so GitHub knows about the check)

---

## 🚀 Step-by-Step Setup

### Step 1: Go to Repository Settings

1. Navigate to your repository on GitHub
2. Click **Settings** tab (top right)
3. In the left sidebar, click **Branches**

### Step 2: Add Branch Protection Rule

1. Click **Add branch protection rule** (or **Add rule**)
2. In "Branch name pattern", enter: `main`
   - This protects your main branch
   - You can also use `master` or other branch names

### Step 3: Configure Required Status Checks

Enable these settings:

#### ✅ Require status checks to pass before merging
- **Check this box** - This is the key setting!
- This ensures PRs can only be merged if all checks pass

#### ✅ Require branches to be up to date before merging
- **Check this box** (recommended)
- Ensures the PR has the latest changes from main

#### ✅ Status checks that are required
- In the search box, type: **"Automated Code Review"**
- Click on it to add it to required checks
- You should see: `Automated Code Review` with a checkmark

**Note:** The status check name must match your workflow job name. In our case, it's "Automated Code Review" from the workflow file.

### Step 4: Additional Recommended Settings

#### ✅ Require a pull request before merging
- **Check this box** (recommended)
- Prevents direct pushes to main branch
- Forces all changes through PR process

#### ✅ Require approvals
- Set to **1** or more reviewers (optional)
- Combines automated + human review

#### ✅ Dismiss stale pull request approvals when new commits are pushed
- **Check this box** (recommended)
- Ensures re-review after code changes

#### ✅ Require review from Code Owners
- **Check this box** if you have a CODEOWNERS file (optional)

### Step 5: Save Changes

1. Scroll to the bottom
2. Click **Create** (or **Save changes**)
3. Branch protection is now active! 🎉

---

## 🎯 What Happens After Setup

### When PR Has Violations (Red X ❌)

**Before Branch Protection:**
- Workflow fails with red X
- Merge button is still green
- Anyone can merge despite failures

**After Branch Protection:**
- Workflow fails with red X ❌
- Merge button shows: **"Merging is blocked"**
- Message: "Required status check 'Automated Code Review' has not succeeded"
- PR cannot be merged until violations are fixed

### When PR Is Clean (Green Check ✅)

- Workflow passes with green checkmark
- Merge button is enabled
- PR can be merged normally

---

## 📸 Visual Guide

### Settings Location
```
Repository → Settings → Branches → Add branch protection rule
```

### Required Configuration
```
Branch name pattern: main

☑️ Require status checks to pass before merging
   ☑️ Require branches to be up to date before merging
   
   Status checks that are required:
   ✓ Automated Code Review  [This is your workflow]

☑️ Require a pull request before merging
   Number of required approvals: 1

☑️ Dismiss stale pull request approvals when new commits are pushed

[Create] or [Save changes]
```

---

## 🔍 Troubleshooting

### Issue: "Automated Code Review" doesn't appear in status checks

**Cause:** GitHub hasn't seen this check yet

**Solution:**
1. Make sure the workflow has run at least once
2. Wait a few minutes for GitHub to register the check
3. Refresh the branch protection settings page
4. The check should now appear in the search

**Alternative:** Type the exact name manually if it doesn't auto-complete

### Issue: Merge button still enabled despite failed check

**Cause:** Branch protection not configured correctly

**Solution:**
1. Verify "Require status checks to pass before merging" is checked
2. Verify "Automated Code Review" is in the required checks list
3. Save the settings again
4. Refresh the PR page

### Issue: Can't find "Automated Code Review" in the list

**Cause:** Workflow job name doesn't match

**Solution:**
1. Check your workflow file: `.github/workflows/code-review.yml`
2. Look for the `jobs:` section
3. Find the job name (should be `code-review`)
4. The display name is from `name:` field: "Automated Code Review"
5. Use this exact name in branch protection

### Issue: Branch protection not working for admins

**Cause:** Admins can bypass branch protection by default

**Solution:**
1. In branch protection settings
2. Scroll to bottom
3. Check: **"Do not allow bypassing the above settings"**
4. Or: **"Include administrators"**
5. Save changes

---

## 🎨 Customization Options

### Protect Multiple Branches

Create separate rules for:
- `main` - Production branch
- `develop` - Development branch
- `release/*` - Release branches

### Different Rules for Different Branches

**Main branch (strict):**
- Require status checks
- Require 2 approvals
- Require code owner review

**Development branch (relaxed):**
- Require status checks
- Require 1 approval
- No code owner review

### Allow Specific People to Bypass

1. In branch protection settings
2. Under "Restrict who can push to matching branches"
3. Add specific users or teams
4. They can merge despite failed checks (not recommended)

---

## 📊 Testing Your Setup

### Test 1: PR with Violations

1. Create a PR with code that has violations
2. Wait for workflow to complete
3. Check PR status - should show red X
4. Try to merge - should see "Merging is blocked"
5. ✅ Success if merge is blocked

### Test 2: PR without Violations

1. Create a PR with clean code
2. Wait for workflow to complete
3. Check PR status - should show green checkmark
4. Try to merge - should be allowed
5. ✅ Success if merge is enabled

### Test 3: Fix Violations

1. Use the PR from Test 1
2. Fix the violations in the code
3. Push the changes
4. Wait for workflow to re-run
5. Check if merge button becomes enabled
6. ✅ Success if merge is now allowed

---

## 🔐 Security Best Practices

### ✅ Do's

- ✅ Always require status checks on main/master
- ✅ Require branches to be up to date
- ✅ Include administrators in restrictions
- ✅ Require at least 1 approval for important branches
- ✅ Dismiss stale approvals on new commits
- ✅ Use CODEOWNERS for critical files

### ❌ Don'ts

- ❌ Don't allow bypassing for admins (unless necessary)
- ❌ Don't disable branch protection temporarily
- ❌ Don't add too many required checks (slows down development)
- ❌ Don't forget to test the setup
- ❌ Don't allow force pushes to protected branches

---

## 📝 Example Configuration

### Minimal Setup (Quick Start)
```
Branch: main
☑️ Require status checks to pass before merging
   Required checks: Automated Code Review
```

### Recommended Setup (Balanced)
```
Branch: main
☑️ Require status checks to pass before merging
   ☑️ Require branches to be up to date
   Required checks: Automated Code Review
☑️ Require a pull request before merging
   Required approvals: 1
☑️ Dismiss stale approvals when new commits are pushed
```

### Strict Setup (Maximum Protection)
```
Branch: main
☑️ Require status checks to pass before merging
   ☑️ Require branches to be up to date
   Required checks: Automated Code Review
☑️ Require a pull request before merging
   Required approvals: 2
   ☑️ Require review from Code Owners
☑️ Dismiss stale approvals when new commits are pushed
☑️ Require signed commits
☑️ Include administrators
☑️ Restrict who can push to matching branches
☐ Allow force pushes (keep unchecked)
☐ Allow deletions (keep unchecked)
```

---

## 🎯 Quick Reference

### To Block Merging on Failed Checks:

1. **Settings** → **Branches** → **Add rule**
2. Branch pattern: `main`
3. ☑️ **Require status checks to pass before merging**
4. Add check: **Automated Code Review**
5. **Create** / **Save**

### To Test:

1. Create PR with violations
2. Wait for red X
3. Try to merge → Should be blocked ✅

---

## 📞 Need Help?

### Common Questions

**Q: How long does it take for branch protection to activate?**  
A: Immediately after saving, but the status check must have run at least once.

**Q: Can I temporarily disable branch protection?**  
A: Yes, but not recommended. Edit the rule and uncheck settings, or delete the rule.

**Q: What if I need to merge urgently despite failures?**  
A: Admins can bypass if "Include administrators" is unchecked, or temporarily disable the rule.

**Q: Can I have different rules for different teams?**  
A: Yes, use "Restrict who can push" and "Require review from Code Owners" settings.

---

## ✅ Verification Checklist

After setup, verify:

- [ ] Branch protection rule created for `main`
- [ ] "Require status checks" is enabled
- [ ] "Automated Code Review" is in required checks
- [ ] Workflow has run at least once
- [ ] Test PR with violations shows "Merging is blocked"
- [ ] Test PR without violations allows merging
- [ ] Team members are aware of the new policy

---

**Your repository is now protected! PRs with code violations cannot be merged.** 🛡️

For more information, see: [GitHub Branch Protection Documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)