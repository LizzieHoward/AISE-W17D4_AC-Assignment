# Quick Start Guide

This is a quick reference for running the prototype.

## One Command to Rule Them All

```bash
uv run python -m caption_prototype.run
```

## What Happens on First Run

1. **Model Download** (~1 GB, 2-5 minutes)
   - Downloads `nlpconnect/vit-gpt2-image-captioning` from Hugging Face
   - Cached in `~/.cache/huggingface/transformers/`

2. **Dataset Download** (~500 MB, 1-3 minutes)
   - Downloads COCO validation set from Hugging Face
   - Cached in `~/.cache/huggingface/datasets/`

3. **Run Tests** (10-30 seconds)
   - Processes 10 test cases
   - Generates captions
   - Evaluates against expected behavior

4. **Generate Outputs**
   - `outputs/results.csv`
   - `outputs/results.json`
   - `outputs/failure_examples.md`

## Subsequent Runs

After the first run, everything is cached and execution takes <1 minute.

## Troubleshooting Quick Fixes

### Command not working?
```bash
# Ensure you're in the repo root
cd AISE-W17D4_AC-Assignment

# Re-sync dependencies
uv sync

# Try again
uv run python -m caption_prototype.run
```

### Downloads failing?
- Check internet connection
- Wait and retry (Hugging Face servers sometimes timeout)
- Check firewall settings

### Out of disk space?
- Need ~1.5 GB free for model and dataset caches

### Out of memory?
- Close other applications
- Minimum 2GB RAM recommended

## Expected Console Output

```
================================================================================
Image Captioning Prototype - Stress Test Runner
================================================================================

Loading model: nlpconnect/vit-gpt2-image-captioning...
Model loaded on cpu

Loading test cases...
Loading COCO dataset (validation split)...
Dataset loaded with XXXX images
Loaded 10 test cases

Running 10 test cases...

[1/10] TC-01 - Normal baseline... ✓
[2/10] TC-02 - Multiple objects... ✗ (Missed salient object)
[3/10] TC-03 - Small object / Background detail... ✗ (Missed salient object)
...

Results saved to outputs/results.csv
Results saved to outputs/results.json
Failure examples saved to outputs/failure_examples.md

================================================================================
SUMMARY
================================================================================

Total tests: 10
Passed: X
Failed: X

Failure breakdown:
  - Overconfident caption: X
  - Missed salient object: X
  ...

================================================================================

✓ Prototype execution completed successfully
```

## Files to Review After Running

1. **outputs/results.csv** - Structured test results
2. **outputs/failure_examples.md** - Detailed failure analysis
3. **RESULTS.md** - Evidence table (update with real results)
