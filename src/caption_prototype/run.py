"""
Main execution script for image captioning prototype.

Usage:
    uv run python -m caption_prototype.run
"""

import json
import sys
from pathlib import Path
from typing import List, Optional
import warnings

# Suppress warning messages for cleaner output
warnings.filterwarnings('ignore')

from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch
from PIL import Image

from caption_prototype.dataset import get_test_cases, TestCase
from caption_prototype.evaluation import (
    apply_refusal_wrapper,
    evaluate_caption,
    generate_failure_examples,
    EvaluationResult
)


def load_model(model_name: str = "nlpconnect/vit-gpt2-image-captioning"):
    """
    Load pre-trained vision-language model.
    
    Args:
        model_name: Hugging Face model identifier
        
    Returns:
        Tuple of (model, processor, tokenizer)
    """
    print(f"Loading model: {model_name}...")
    
    model = VisionEncoderDecoderModel.from_pretrained(model_name)
    processor = ViTImageProcessor.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Set to evaluation mode
    model.eval()
    
    # Use GPU if available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    
    print(f"Model loaded on {device}")
    return model, processor, tokenizer, device


def generate_caption(
    image: Image.Image,
    model,
    processor,
    tokenizer,
    device: str,
    max_length: int = 16,
    num_beams: int = 4
) -> str:
    """
    Generate caption for a single image.
    
    Args:
        image: PIL Image
        model: Vision-language model
        processor: Image processor
        tokenizer: Text tokenizer
        device: Device to run on
        max_length: Maximum caption length
        num_beams: Beam search width
        
    Returns:
        Generated caption string
    """
    try:
        # Preprocess image
        pixel_values = processor(images=image, return_tensors="pt").pixel_values
        pixel_values = pixel_values.to(device)
        
        # Generate caption
        with torch.no_grad():
            output_ids = model.generate(
                pixel_values,
                max_length=max_length,
                num_beams=num_beams,
                early_stopping=True
            )
        
        # Decode caption
        caption = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return caption.strip()
    
    except Exception as e:
        return f"Error: caption generation failed - {str(e)}"


def run_prototype(
    manifest_path: Path,
    output_dir: Path,
    cache_dir: Optional[Path] = None
) -> List[EvaluationResult]:
    """
    Run the full prototype pipeline.
    
    Args:
        manifest_path: Path to test case manifest
        output_dir: Directory for output files
        cache_dir: Optional cache directory for model/data
        
    Returns:
        List of evaluation results
    """
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load model
    model, processor, tokenizer, device = load_model()
    
    # Load test cases
    print("\nLoading test cases...")
    test_cases = get_test_cases(manifest_path, cache_dir=str(cache_dir) if cache_dir else None)
    print(f"Loaded {len(test_cases)} test cases\n")
    
    # Run inference on each test case
    results: List[EvaluationResult] = []
    
    print(f"Running {len(test_cases)} test cases...\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"[{i}/{len(test_cases)}] {test_case.test_id} - {test_case.slice_name}...", end=" ")
        
        # Generate raw caption
        raw_caption = generate_caption(
            test_case.image,
            model,
            processor,
            tokenizer,
            device
        )
        
        # Apply refusal wrapper if needed
        final_output = apply_refusal_wrapper(
            raw_caption,
            test_case.requires_refusal,
            test_case.refusal_category
        )
        
        # Evaluate
        result = evaluate_caption(
            test_id=test_case.test_id,
            slice_name=test_case.slice_name,
            expected_behavior=test_case.expected_behavior,
            raw_caption=raw_caption,
            final_output=final_output,
            requires_refusal=test_case.requires_refusal
        )
        
        results.append(result)
        
        # Print result
        if result.passed:
            print("✓")
        else:
            print(f"✗ ({result.failure_type})")
    
    return results


def save_results(
    results: List[EvaluationResult],
    output_dir: Path
):
    """
    Save results to CSV and JSON files.
    
    Args:
        results: List of evaluation results
        output_dir: Directory for output files
    """
    # Save CSV
    csv_path = output_dir / "results.csv"
    with open(csv_path, 'w', encoding='utf-8') as f:
        # Header
        f.write("test_id,slice_name,expected_behavior,raw_caption,final_output,passed,failure_type,notes\n")
        
        # Rows
        for r in results:
            # Escape quotes in fields
            def escape(s):
                if s is None:
                    return ""
                s = str(s).replace('"', '""')
                return f'"{s}"'
            
            f.write(f"{escape(r.test_id)},{escape(r.slice_name)},{escape(r.expected_behavior)},")
            f.write(f"{escape(r.raw_caption)},{escape(r.final_output)},{r.passed},")
            f.write(f"{escape(r.failure_type)},{escape(r.notes)}\n")
    
    print(f"\nResults saved to {csv_path}")
    
    # Save JSON
    json_path = output_dir / "results.json"
    json_data = {
        "test_count": len(results),
        "passed_count": sum(1 for r in results if r.passed),
        "failed_count": sum(1 for r in results if not r.passed),
        "results": [
            {
                "test_id": r.test_id,
                "slice_name": r.slice_name,
                "expected_behavior": r.expected_behavior,
                "raw_caption": r.raw_caption,
                "final_output": r.final_output,
                "passed": r.passed,
                "failure_type": r.failure_type,
                "notes": r.notes
            }
            for r in results
        ]
    }
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    print(f"Results saved to {json_path}")
    
    # Generate failure examples
    failure_md = generate_failure_examples(results, min_failures=8)
    failure_path = output_dir / "failure_examples.md"
    with open(failure_path, 'w', encoding='utf-8') as f:
        f.write(failure_md)
    
    print(f"Failure examples saved to {failure_path}")


def print_summary(results: List[EvaluationResult]):
    """Print summary table to console."""
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    passed = sum(1 for r in results if r.passed)
    failed = sum(1 for r in results if not r.passed)
    
    print(f"\nTotal tests: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    print("\nFailure breakdown:")
    failure_types = {}
    for r in results:
        if not r.passed and r.failure_type:
            failure_types[r.failure_type] = failure_types.get(r.failure_type, 0) + 1
    
    for failure_type, count in sorted(failure_types.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {failure_type}: {count}")
    
    print("\n" + "="*80)


def main():
    """Main entry point."""
    # Set paths relative to repository root
    repo_root = Path(__file__).parent.parent.parent
    manifest_path = repo_root / "data" / "manifest.csv"
    output_dir = repo_root / "outputs"
    cache_dir = repo_root / ".cache"
    
    print("="*80)
    print("Image Captioning Prototype - Stress Test Runner")
    print("="*80)
    print()
    
    # Check if manifest exists
    if not manifest_path.exists():
        print(f"Error: Manifest file not found at {manifest_path}")
        print("Please ensure data/manifest.csv exists.")
        sys.exit(1)
    
    # Run prototype
    try:
        results = run_prototype(manifest_path, output_dir, cache_dir)
        
        # Save results
        save_results(results, output_dir)
        
        # Print summary
        print_summary(results)
        
        print("\n✓ Prototype execution completed successfully")
        
    except Exception as e:
        print(f"\n✗ Error during execution: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
