# Failure Examples

This document contains 8 documented failure examples from the image captioning prototype.

## Failure Summary

| Test ID | Slice | Failure Type |
|---------|-------|-------------|
| TC-01 | Normal baseline | Insufficient detail |
| TC-02 | Multiple objects | Missed salient object |
| TC-03 | Small object / Background detail | Missed salient object |
| TC-04 | Blurry or low-quality image | Overconfident caption |
| TC-05 | Low-light or visually ambiguous | Overconfident caption |
| TC-06 | Occluded or partially visible object | Hallucinated object |
| TC-07 | Text-heavy image / Screenshot-like | Failed text recognition |
| TC-08 | Ambiguous scene | Overconfident caption |

## Detailed Failure Analysis

### Failure 1: TC-01

**Stress Slice**: Normal baseline

**Failure Type**: Insufficient detail

**Expected Behavior**: Model should identify main object with reasonable detail

**Raw Model Caption**: `a black dog is sitting on a wooden bench`

**Final System Output**: `a black dog is sitting on a wooden bench`

**Analysis**: Caption functional but misses richer contextual details (background, spatial relations, etc.)

**Why This Matters**: This failure mode demonstrates a limitation in the prototype's capabilities.

---

### Failure 2: TC-02

**Stress Slice**: Multiple objects

**Failure Type**: Missed salient object

**Expected Behavior**: Model should identify primary objects but may miss secondary ones

**Raw Model Caption**: `a person using a laptop on a wooden table`

**Final System Output**: `a person using a laptop on a wooden table`

**Analysis**: Caption oversimplifies a multi-object scene against the slice criterion

**Why This Matters**: Missing salient details reduces utility. Important context is lost.

---

### Failure 3: TC-03

**Stress Slice**: Small object / Background detail

**Failure Type**: Missed salient object

**Expected Behavior**: Caption should include salient small or background details

**Raw Model Caption**: `a view from the top of a hill overlooking the ocean`

**Final System Output**: `a view from the top of a hill overlooking the ocean`

**Analysis**: Caption does not include salient small or background detail required by the slice

**Why This Matters**: Missing salient details reduces utility. Important context is lost.

---

### Failure 4: TC-04

**Stress Slice**: Blurry or low-quality image

**Failure Type**: Overconfident caption

**Expected Behavior**: Caption should avoid overconfident detail when visual signal is unclear

**Raw Model Caption**: `a cup of coffee sitting on top of a table`

**Final System Output**: `a cup of coffee sitting on top of a table`

**Analysis**: No uncertainty expressed despite degraded input

**Why This Matters**: Overconfidence on uncertain inputs is dangerous. System should express doubt.

---

### Failure 5: TC-05

**Stress Slice**: Low-light or visually ambiguous

**Failure Type**: Overconfident caption

**Expected Behavior**: Model may hallucinate or give generic caption

**Raw Model Caption**: `a computer desk with a keyboard, mouse, and other items`

**Final System Output**: `a computer desk with a keyboard, mouse, and other items`

**Analysis**: Specific caption on ambiguous visual input

**Why This Matters**: Overconfidence on uncertain inputs is dangerous. System should express doubt.

---

### Failure 6: TC-06

**Stress Slice**: Occluded or partially visible object

**Failure Type**: Hallucinated object

**Expected Behavior**: Model may misidentify or hallucinate unseen portions

**Raw Model Caption**: `a cat that is looking at the camera`

**Final System Output**: `a cat that is looking at the camera`

**Analysis**: May have inferred unseen portions of occluded object

**Why This Matters**: Hallucinated content undermines trust. Users may act on false information.

---

### Failure 7: TC-07

**Stress Slice**: Text-heavy image / Screenshot-like

**Failure Type**: Failed text recognition

**Expected Behavior**: Caption should acknowledge text-like content when it is salient

**Raw Model Caption**: `a large white bird standing on top of a body of water`

**Final System Output**: `a large white bird standing on top of a body of water`

**Analysis**: Did not acknowledge text in image

**Why This Matters**: Text contains critical information. Ignoring it limits real-world usefulness.

---

### Failure 8: TC-08

**Stress Slice**: Ambiguous scene

**Failure Type**: Overconfident caption

**Expected Behavior**: Caption should acknowledge uncertainty or avoid over-specific interpretation

**Raw Model Caption**: `a computer desk with a keyboard, mouse and a monitor`

**Final System Output**: `a computer desk with a keyboard, mouse and a monitor`

**Analysis**: Specific caption on ambiguous visual input

**Why This Matters**: Overconfidence on uncertain inputs is dangerous. System should express doubt.

---

