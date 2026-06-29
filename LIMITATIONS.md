# Limitations

This prototype uses a frozen ViT-GPT2 model trained on COCO captions. It cannot adapt to new domains or correct its own errors. The model has no uncertainty quantification—it generates captions unconditionally even when visual input is ambiguous, degraded, or out-of-distribution. Test images are from picsum.photos placeholder service, selected for diversity but not representative of authentic high-stakes scenarios. Stress slices use available images (blur effects, people) rather than authentic medical or legal content. The refusal wrapper is rule-based, not learned, and may fail to catch all boundary cases. The system cannot explain reasoning, detect hallucinations autonomously, or refuse appropriately without explicit labels. This is a reviewable prototype demonstrating failure modes, not production-ready.

**Word count**: 110 words
