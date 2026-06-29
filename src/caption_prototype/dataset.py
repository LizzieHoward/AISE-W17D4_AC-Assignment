"""
Dataset loading and test case management for image captioning prototype.
"""

import csv
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from PIL import Image
import requests
from io import BytesIO


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
        image_id: Optional[str] = None,  # Now stores URL as string
        notes: Optional[str] = None
    ):
        self.test_id = test_id
        self.slice_name = slice_name
        self.description = description
        self.expected_behavior = expected_behavior
        self.requires_refusal = requires_refusal
        self.refusal_category = refusal_category
        self.image_id = image_id  # URL string
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
                image_id=row.get('image_id') or None,  # Keep as string (URL)
                notes=row.get('notes') or None
            )
            test_cases.append(test_case)
    
    return test_cases


def load_images_from_urls(test_cases: List[TestCase], cache_dir: Optional[Path] = None) -> List[TestCase]:
    """
    Load images from URLs for each test case.
    
    Args:
        test_cases: List of test cases with image_url specified
        cache_dir: Optional cache directory for downloaded images
        
    Returns:
        Test cases with images loaded
    """
    print("Loading images from URLs...")
    
    # Create cache directory if specified
    if cache_dir:
        cache_dir = Path(cache_dir)
        cache_dir.mkdir(parents=True, exist_ok=True)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"  [{i}/{len(test_cases)}] Loading {test_case.test_id}...", end=" ")
        
        if not test_case.image_id:  # Using image_id field to store URL
            print("WARNING: No URL provided, using placeholder")
            test_case.image = Image.new('RGB', (224, 224), color=(128, 128, 128))
            continue
        
        image_url = test_case.image_id  # Reusing image_id field for URL
        
        # Check cache first
        if cache_dir:
            cache_filename = f"{test_case.test_id}.jpg"
            cache_path = cache_dir / cache_filename
            
            if cache_path.exists():
                try:
                    test_case.image = Image.open(cache_path).convert('RGB')
                    print("OK (cached)")
                    continue
                except Exception as e:
                    print(f"WARNING: Cache read failed: {e}")
        
        # Download image
        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            test_case.image = Image.open(BytesIO(response.content)).convert('RGB')
            
            # Save to cache
            if cache_dir:
                cache_path = cache_dir / f"{test_case.test_id}.jpg"
                test_case.image.save(cache_path, 'JPEG')
            
            print("OK")
        except Exception as e:
            print(f"FAILED to load: {str(e)[:50]}")
            # Use placeholder on error
            test_case.image = Image.new('RGB', (224, 224), color=(128, 128, 128))
    
    return test_cases


def get_test_cases(manifest_path: Path, cache_dir: Optional[str] = None) -> List[TestCase]:
    """
    Main entry point: load test cases and their images.
    
    Args:
        manifest_path: Path to manifest CSV
        cache_dir: Optional cache directory for images
        
    Returns:
        List of TestCase objects with images loaded
    """
    test_cases = load_manifest(manifest_path)
    cache_path = Path(cache_dir) / "images" if cache_dir else None
    test_cases = load_images_from_urls(test_cases, cache_dir=cache_path)
    return test_cases
