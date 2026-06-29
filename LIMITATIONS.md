# Limitations

This prototype uses a frozen ViT-GPT2 model trained on COCO captions. It cannot adapt to new domains or correct its own errors. The model has no uncertainty quantification—it generates captions unconditionally even when visual input is ambiguous, degraded, or out-of-distribution. Stress slices (medical, legal, safety) are approximated from COCO proxies, not authentic high-stakes data. The refusal wrapper is rule-based, not learned, and may fail to catch all boundary cases. Caption quality relies entirely on pre-training biases. The system cannot explain its reasoning, detect hallucinations autonomously, or refuse appropriately without explicit test case labels. This is a reviewable prototype, not a production-ready system.

**Word count**: 107 words
