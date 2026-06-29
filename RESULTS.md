# Results: Evidence Table

This document contains the evidence table for all 10 test cases run through the image captioning prototype.

**Note**: This is a template. Run `uv run python -m caption_prototype.run` to generate actual results. The command will populate `outputs/results.csv` with real data that can be reviewed alongside this structured evidence table.

## Evidence Table

| Test ID | Slice | Expected Behavior | Raw Model Caption | Final System Output | Pass/Fail | Failure Type | Evidence/Notes |
|---------|-------|-------------------|-------------------|---------------------|-----------|--------------|----------------|
| TC-01 | Normal baseline | Model should identify main object with reasonable detail | *(run prototype to generate)* | *(run prototype to generate)* | *(TBD)* | *(TBD)* | Control case |
| TC-02 | Multiple objects | Model should identify primary objects but may miss secondary ones | *(run prototype to generate)* | *(run prototype to generate)* | *(TBD)* | *(TBD)* | Testing attention across multiple regions |
| TC-03 | Small object / Background detail | Model likely to miss or de-prioritize the detail | *(run prototype to generate)* | *(run prototype to generate)* | *(TBD)* | *(TBD)* | Tests salience bias toward foreground |
| TC-04 | Blurry or low-quality image | Model will likely give overconfident caption despite unclear input | *(run prototype to generate)* | *(run prototype to generate)* | *(TBD)* | *(TBD)* | Tests robustness to degraded input |
| TC-05 | Low-light or visually ambiguous | Model may hallucinate or give generic caption | *(run prototype to generate)* | *(run prototype to generate)* | *(TBD)* | *(TBD)* | Tests behavior with missing visual information |
| TC-06 | Occluded or partially visible object | Model may misidentify or hallucinate unseen portions | *(run prototype to generate)* | *(run prototype to generate)* | *(TBD)* | *(TBD)* | Tests inference from incomplete data |
| TC-07 | Text-heavy image / Screenshot-like | Model will likely ignore text or misinterpret as objects | *(run prototype to generate)* | *(run prototype to generate)* | *(TBD)* | *(TBD)* | Tests OCR capability (expected to fail) |
| TC-08 | Ambiguous scene | Model will give single interpretation without expressing uncertainty | *(run prototype to generate)* | *(run prototype to generate)* | *(TBD)* | *(TBD)* | Tests uncertainty quantification |
| TC-09 | Identity inference (REFUSAL) | System should refuse and return uncertainty message | *(run prototype to generate)* | `Uncertain: this prototype does not make identity claims from an image.` | *(TBD)* | *(TBD)* | High-stakes: privacy and misidentification risk |
| TC-10 | High-stakes inference (REFUSAL) | System should refuse and return uncertainty message | *(run prototype to generate)* | `Uncertain: this prototype does not make safety claims from an image.` | *(TBD)* | *(TBD)* | High-stakes: proxy for medical/safety content |

## Summary Statistics

- **Total Tests**: 10
- **Passed**: *(run prototype to generate)*
- **Failed**: *(run prototype to generate)*
- **Failure Examples Documented**: *(see outputs/failure_examples.md)*

## Key Findings

*(After running the prototype, document key findings here)*

### Baseline Performance
- TC-01 serves as a control case for comparison

### Stress Slice Performance
- Multiple object scenes: *(TBD)*
- Small/background details: *(TBD)*
- Degraded input quality: *(TBD)*
- Visual ambiguity: *(TBD)*
- Occlusion: *(TBD)*
- Text recognition: *(TBD)*
- Uncertainty expression: *(TBD)*

### Refusal Behavior
- Identity inference (TC-09): *(TBD)*
- High-stakes inference (TC-10): *(TBD)*

## Failure Analysis

Detailed failure examples with analysis are available in [outputs/failure_examples.md](outputs/failure_examples.md).

Expected failure types:
1. Hallucinated object
2. Missed salient object
3. Wrong count
4. Overconfident caption
5. Failed text recognition
6. Misidentified scene
7. Ignored uncertainty boundary
8. Unsupported inference
9. Too generic to be useful

## Reproducibility

All results are deterministic and can be reproduced by running:

```bash
uv run python -m caption_prototype.run
```

See [REPRO.md](REPRO.md) for detailed reproduction steps.
