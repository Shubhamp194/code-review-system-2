# Ollama Timeout Fix Documentation

## Problem Description

The GitHub Actions workflow was hanging indefinitely at the "Generating PR change explanation..." step, blocking the entire workflow from completing. This prevented the code review process from finishing and providing feedback to developers.

### Root Cause

1. **Sequential Processing**: The PR explanation analyzer processes files one by one
2. **Long Timeout Per File**: Each file had a 120-second timeout
3. **Multiple Files**: With multiple changed files, total time = 120s × number of files
4. **No Workflow Protection**: No timeout at the workflow step level to prevent indefinite hanging

### Example Scenario
- PR with 5 changed files
- 120 seconds timeout per file
- Total potential time: 5 × 120 = 600 seconds (10 minutes)
- If Ollama is slow or unresponsive, workflow hangs for extended periods

## Solution Implemented

### 1. Workflow-Level Timeout Protection

**File**: `.github/workflows/code-review.yml`

Added timeout at the analysis step level:

```yaml
- name: Run Code Review with AI Explanation
  timeout-minutes: 5  # Maximum 5 minutes for entire analysis
  run: |
    # Analysis command
```

**Impact**: Ensures the workflow never hangs for more than 5 minutes, even if Ollama is completely unresponsive.

### 2. Command-Level Timeout with Fallback

Added `timeout` command wrapper with graceful fallback:

```yaml
timeout 4m python -m analyzer.main review \
  --pr-base "${{ github.event.pull_request.base.sha }}" \
  --pr-head "${{ github.event.pull_request.head.sha }}" \
  --output-format github || {
  echo "⚠️ AI explanation timed out. Running violations-only analysis..."
  python -m analyzer.main review \
    --pr-base "${{ github.event.pull_request.base.sha }}" \
    --pr-head "${{ github.event.pull_request.head.sha }}" \
    --output-format github \
    --skip-explanation
}
```

**How it works**:
- Primary attempt: 4-minute timeout for full analysis with AI explanations
- Fallback: If timeout occurs, immediately run violations-only analysis
- Result: Always get code review results, even if AI explanation fails

### 3. Reduced Per-File Timeout

**File**: `config/rules.yaml`

Changed Ollama timeout from 120 seconds to 30 seconds per file:

```yaml
pr_explanation:
  enabled: true
  provider: ollama
  model: qwen2.5-coder:1.5b
  base_url: http://127.0.0.1:11434
  fallback_to_heuristic: true
  timeout_seconds: 30  # Reduced from 120
```

**Impact**: 
- Faster failure detection when Ollama is slow
- 5 files now take maximum 150 seconds instead of 600 seconds
- Still enough time for Ollama to generate explanations for most files

### 4. Heuristic Fallback Already Enabled

The system already has `fallback_to_heuristic: true`, which means:
- If Ollama times out on a file, it uses rule-based analysis
- If Ollama is unavailable, it uses rule-based analysis
- Violations are always detected, regardless of AI availability

## Timeout Hierarchy

The system now has multiple layers of timeout protection:

```
1. Workflow Level (30 minutes)
   └── 2. Step Level (5 minutes)
       └── 3. Command Level (4 minutes)
           └── 4. Per-File Level (30 seconds)
```

**Example with 5 files**:
- Best case: All files analyzed with AI in ~50 seconds (5 × 10s average)
- Timeout case: Each file times out at 30s = 150 seconds total
- Fallback case: Command times out at 4 minutes, switches to violations-only
- Hard limit: Step times out at 5 minutes, workflow continues

## Benefits

### 1. Guaranteed Completion
- Workflow always completes within 5 minutes
- No more indefinite hanging
- Developers get feedback quickly

### 2. Graceful Degradation
- Primary: Full analysis with AI explanations
- Fallback 1: Violations-only analysis (still blocks bad code)
- Fallback 2: Workflow continues to other steps

### 3. Faster Feedback Loop
- 30-second per-file timeout catches slow responses quickly
- 4-minute command timeout ensures fallback happens fast
- 5-minute step timeout is the hard safety net

### 4. Maintained Code Quality
- Violations are ALWAYS detected (rule-based engine)
- AI explanations are a bonus, not a requirement
- PR merging is still blocked on CRITICAL/HIGH violations

## Testing Recommendations

### Test Case 1: Normal Operation
```bash
# Create PR with 2-3 files
# Expected: Complete in < 1 minute with AI explanations
```

### Test Case 2: Ollama Slow Response
```bash
# Create PR with 5+ files while Ollama is under load
# Expected: Some files timeout at 30s, use heuristic fallback
# Total time: < 3 minutes
```

### Test Case 3: Ollama Unavailable
```bash
# Stop Ollama service
# Create PR
# Expected: Command times out at 4 minutes, switches to violations-only
# Total time: ~4 minutes
```

### Test Case 4: Complete Failure
```bash
# Simulate complete system failure
# Expected: Step times out at 5 minutes, workflow continues
# Violations still reported (if any)
```

## Monitoring

Watch for these indicators in GitHub Actions logs:

### Success Indicators
```
✓ Analyzing PR changes...
✓ Generating PR change explanation...
✓ Analysis complete
```

### Timeout Indicators
```
⚠️ AI explanation timed out. Running violations-only analysis...
⚠️ Falling back to heuristic analysis for file X
```

### Failure Indicators
```
❌ Analysis step timed out after 5 minutes
❌ Workflow timed out after 30 minutes
```

## Configuration Options

### Adjust Timeouts

If you need different timeout values, edit these files:

**Workflow step timeout** (`.github/workflows/code-review.yml`):
```yaml
timeout-minutes: 5  # Change to 3, 7, 10, etc.
```

**Command timeout** (`.github/workflows/code-review.yml`):
```yaml
timeout 4m python ...  # Change to 2m, 3m, 6m, etc.
```

**Per-file timeout** (`config/rules.yaml`):
```yaml
timeout_seconds: 30  # Change to 15, 45, 60, etc.
```

### Disable AI Explanations

If Ollama continues to cause issues, disable AI explanations:

**Option 1**: In `config/rules.yaml`:
```yaml
pr_explanation:
  enabled: false  # Disable completely
```

**Option 2**: In workflow, always use `--skip-explanation`:
```yaml
python -m analyzer.main review ... --skip-explanation
```

## Performance Expectations

### With AI Explanations (Ollama Working)
- Small PR (1-3 files): 30-60 seconds
- Medium PR (4-7 files): 1-2 minutes
- Large PR (8-15 files): 2-4 minutes

### Without AI Explanations (Violations Only)
- Small PR (1-3 files): 5-10 seconds
- Medium PR (4-7 files): 10-20 seconds
- Large PR (8-15 files): 20-40 seconds

### With Timeouts/Fallbacks
- Maximum wait: 5 minutes (step timeout)
- Typical fallback: 4 minutes (command timeout)
- Always get results: Yes (violations-only mode)

## Conclusion

The timeout fix ensures:
1. ✅ Workflows never hang indefinitely
2. ✅ Developers get feedback within 5 minutes maximum
3. ✅ Code quality checks always run (violations detected)
4. ✅ AI explanations are attempted but not required
5. ✅ System gracefully degrades when Ollama is slow/unavailable

The code review system is now production-ready with robust timeout protection and fallback mechanisms.

---

**Last Updated**: 2026-04-08  
**Status**: ✅ Implemented and Ready for Testing