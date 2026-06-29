"""
Dataset loading and test case management for image captioning prototype.
"""

import csv
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from PIL import Image
from datasets import load_dataset


class TestCase:
    """Represents a single test case with metadata."""
    
    def __init__(
        self,
        test_id: str,
        slice_name: str,
        description: str,
        expected_behavior: str,
        requires_refusal: bool,
        refusal_category: Optional[str] = None,
        image_id: Optional[int] = None,
        notes: Optional[str] = None
    ):
        self.test_id = test_id
        self.slice_name = slice_name
        self.description = description
        self.expected_behavior = expected_behavior
        self.requires_refusal = requires_refusal
        self.refusal_category = refusal_category
        self.image_id = image_id
        self.notes = notes
        self.image: Optional[Image.Image] = None
    
    def to_dict(self) -> Dict:
        """Convert test case to dictionary."""
        return {
            'test_id': self.test_id,
            'slice_name': self.slice_name,
            'description': self.description,
            'expected_behavior': self.expected_behavior,
            'requires_refusal': self.requires_refusal,
            'refusal_category': self.refusal_category or '',
            'image_id': self.image_id,
            'notes': self.notes or ''
        }


def load_manifest(manifest_path: Path) -> List[TestCase]:
    """
    Load test cases from manifest CSV.
    
    Args:
        manifest_path: Path to manifest.csv
        
    Returns:
        List of TestCase objects
    """
    test_cases = []
    
    with open(manifest_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            test_case = TestCase(
                test_id=row['test_id'],
                slice_name=row['slice_name'],
                description=row['description'],
                expected_behavior=row['expected_behavior'],
                requires_refusal=row['requires_refusal'].lower() == 'true',
                refusal_category=row.get('refusal_category') or None,
                image_id=int(row['image_id']) if row.get('image_id') else None,
                notes=row.get('notes') or None
            )
            test_cases.append(test_case)
    
    return test_cases


def load_coco_images(test_cases: List[TestCase], cache_dir: Optional[str] = None) -> List[TestCase]:
    """
    Load images from COCO dataset for each test case.
    
    Args:
        test_cases: List of test cases with image_id specified
        cache_dir: Optional cache directory for dataset
        
    Returns:
        Test cases with images loaded
    """
    print("Loading COCO dataset (validation split)...")
    
    dataset = None
    
    # Try multiple dataset sources
    dataset_sources = [
        ("HuggingFaceM4/COCO", "validation[:1000]"),
        ("detection-datasets/coco", "val[:1000]"),
        ("yerevann/coco-karpathy", "val[:1000]"),
    ]
    
    for dataset_name, split in dataset_sources:
        try:
            print(f"Attempting to load {dataset_name}...")
            dataset = load_dataset(
                dataset_name,
                split=split,
                cache_dir=cache_dir,
                trust_remote_code=True
            )
            print(f"✓ Successfully loaded {dataset_name}")
            break
        except Exception as e:
            print(f"✗ Could not load {dataset_name}: {str(e)[:100]}")
            continue
    
    if dataset is None:
        print("⚠️  Warning: Could not load any COCO dataset. Using placeholder images.")
        print("    This is acceptable for demonstrating the pipeline structure.")
        # Create placeholder images for all test cases
        for test_case in test_cases:
            test_case.image = Image.new('RGB', (224, 224), color=(128, 128, 128))
        return test_cases
    
    # Create a mapping of image IDs to images
    # For this prototype, we'll use indices as proxies for image IDs
    print(f"Dataset loaded with {len(dataset)} images")
    
    for test_case in test_cases:
        if test_case.image_id is not None and test_case.image_id < len(dataset):
            # Get image from dataset
            item = dataset[test_case.image_id]
            
            # Handle different dataset formats
            if 'image' in item:
                test_case.image = item['image']
            elif 'img' in item:
                test_case.image = item['img']
            elif 'file_name' in item and 'coco_url' in item:
                # Some datasets only have URLs, use placeholder
                print(f"Note: {test_case.test_id} requires manual download, using placeholder")
                test_case.image = Image.new('RGB', (224, 224), color='gray')
            else:
                print(f"Warning: Could not find image field for {test_case.test_id}")
                # Create a placeholder image
                test_case.image = Image.new('RGB', (224, 224), color='gray')
            
            # Convert to RGB if needed
            if hasattr(test_case.image, 'mode') and test_case.image.mode != 'RGB':
                test_case.image = test_case.image.convert('RGB')
        else:
            print(f"Warning: Invalid image_id for {test_case.test_id}, using placeholder")
            test_case.image = Image.new('RGB', (224, 224), color='gray')
    
    return test_cases


def get_test_cases(manifest_path: Path, cache_dir: Optional[str] = None) -> List[TestCase]:
    """
    Main entry point: load test cases and their images.
    
    Args:
        manifest_path: Path to manifest CSV
        cache_dir: Optional cache directory for dataset
        
    Returns:
        List of TestCase objects with images loaded
    """
    test_cases = load_manifest(manifest_path)
    test_cases = load_coco_images(test_cases, cache_dir=cache_dir)
    return test_cases
