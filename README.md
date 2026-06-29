# Reviewable Multimodal Prototype: Image Captioning with Stress Tests

## Overview

This is a **reviewable prototype** for exploring image captioning failure modes and limitations, built as part of an AI Safety Engineering assignment. It is **not a production system**.

**Track**: B - Image Captioning (image → caption)

**Model**: `nlpconnect/vit-gpt2-image-captioning` (Vision Transformer + GPT-2)

**Focus**: Stress testing with hallucination detection, boundary cases, and refusal behavior for uncertain/high-stakes scenarios.

## What This Prototype Does

1. Loads 10 public test images from picsum.photos (stable placeholder service)
2. Runs 10 curated test cases including:
   - Normal common objects
   - Multiple objects, small details, ambiguous scenes
   - Stress slices: blurry images, low-light, occlusion, text-heavy images
   - Refusal cases: identity inference, high-stakes medical/safety content
3. Generates captions using a pre-trained vision-language model
4. Applies uncertainty wrappers for refusal cases
5. Outputs results with evidence table showing failures
6. Documents at least 8 failure examples with failure type annotations

## How to Run

### Prerequisites
- Python 3.9+
- `uv` package manager ([install guide](https://github.com/astral-sh/uv))

### Setup and Execution

```bash
# Clone and navigate to repository
cd AISE-W17D4_AC-Assignment

# Install dependencies with uv
uv sync

# Run the full prototype
uv run python -m caption_prototype.run
```

The command will:
- Download the model (first run only, ~1GB)
- Download 10 test images from picsum.photos (~2MB total)
- Process all test cases
- Generate `outputs/results.csv` and `outputs/results.json`
- Print a summary to console

## Files to Review

| File | Purpose |
|------|---------|
| [README.md](README.md) | This file - project overview |
| [PIPELINE.md](PIPELINE.md) | System pipeline diagram and failure predictions |
| [TEST_PLAN.md](TEST_PLAN.md) | Test case descriptions and stress slices |
| [RESULTS.md](RESULTS.md) | Evidence table with all 10 test results |
| [LIMITATIONS.md](LIMITATIONS.md) | Known limitations (80-120 words) |
| [REPRO.md](REPRO.md) | Exact reproduction steps and troubleshooting |
| [outputs/failure_examples.md](outputs/failure_examples.md) | Detailed failure analysis (8+ examples) |
| [outputs/results.csv](outputs/results.csv) | Machine-readable test results |
| [src/caption_prototype/](src/caption_prototype/) | Source code |

## Key Design Decisions

- **No manual image collection**: Uses public images from picsum.photos (stable placeholder service)
- **Stress slice coverage**: Diverse images selected to cover stress categories including blur effects, grayscale, people, and various scenes
- **Refusal wrapper**: High-stakes cases return uncertainty messages instead of raw model output
- **Minimal design**: No web UI, no over-engineering, just reproducible code + evidence

## Expected Behavior

**This prototype is designed to fail**. The assignment requires documenting failure modes. You should see:
- Hallucinated objects
- Missed salient details
- Overcounting/undercounting
- Overconfident captions on ambiguous images
- Failed text recognition
- Ignored uncertainty boundaries

These failures are documented in [RESULTS.md](RESULTS.md) and [outputs/failure_examples.md](outputs/failure_examples.md).

## Notes

- First run downloads ~1GB of model weights and ~2MB of test images
- Outputs are deterministic (same images and fixed random seed)
- This is a **reviewable prototype**, not a production system
- Failures are features, not bugs—they demonstrate model limitations
