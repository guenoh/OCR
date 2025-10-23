#!/usr/bin/env python3
"""OCR Text Extraction Module"""

import easyocr
import numpy as np
import torch

# Global reader cache to avoid reloading model
_reader_cache = {}


def extract_text(image, languages=['ko', 'en'], use_gpu=True, optimize_params=True):
    """
    Extract text from image using EasyOCR with performance optimizations

    Args:
        image (PIL.Image): Input image
        languages (list): List of language codes
        use_gpu (bool): Use GPU if available
        optimize_params (bool): Use optimized parameters for better accuracy

    Returns:
        list: OCR results with bbox, text, and confidence
    """
    global _reader_cache

    # Check GPU availability
    gpu_available = torch.cuda.is_available() or torch.backends.mps.is_available()
    use_gpu = use_gpu and gpu_available

    if use_gpu:
        print(f"🔍 Initializing EasyOCR with GPU ({languages})")
    else:
        print(f"🔍 Initializing EasyOCR with CPU ({languages})")

    # Cache reader to avoid reloading model
    cache_key = f"{','.join(languages)}_{use_gpu}"
    if cache_key not in _reader_cache:
        reader = easyocr.Reader(languages, gpu=use_gpu)
        _reader_cache[cache_key] = reader
        print("   ✓ Model loaded and cached")
    else:
        reader = _reader_cache[cache_key]
        print("   ✓ Using cached model")

    print("📝 Extracting text...")
    # Convert PIL Image to numpy array
    img_array = np.array(image)

    # Perform OCR with optimized parameters
    if optimize_params:
        # Optimized parameters for better small text detection
        results = reader.readtext(
            img_array,
            contrast_ths=0.1,      # Lower threshold for better contrast detection
            text_threshold=0.6,    # Lower threshold to detect more text
            low_text=0.3,          # Lower threshold for weak text
            link_threshold=0.3,    # Lower threshold for linking text regions
            width_ths=0.5,         # Minimum width threshold
            height_ths=0.5,        # Minimum height threshold
            paragraph=False        # Don't group into paragraphs
        )
    else:
        results = reader.readtext(img_array)

    print(f"✅ Found {len(results)} text regions")
    return results
