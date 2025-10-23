#!/usr/bin/env python3
"""
ADB Screenshot OCR Script
- Captures screenshot via adb
- Crops top 850px
- Scales to 0.5x
- Extracts text using EasyOCR
"""

import subprocess
import os
from PIL import Image
import easyocr
import numpy as np


def capture_adb_screenshot(output_path="screenshot.png"):
    """Capture screenshot from Android device using adb"""
    print("Capturing screenshot via adb...")

    # Capture screenshot on device
    subprocess.run(["adb", "shell", "screencap", "-p", "/sdcard/screenshot.png"], check=True)

    # Pull screenshot from device
    subprocess.run(["adb", "pull", "/sdcard/screenshot.png", output_path], check=True)

    # Clean up device
    subprocess.run(["adb", "shell", "rm", "/sdcard/screenshot.png"], check=True)

    print(f"Screenshot saved to {output_path}")
    return output_path


def process_image(input_path, crop_top=850, scale_factor=0.5):
    """Crop top pixels and scale image"""
    print(f"Processing image: crop_top={crop_top}px, scale={scale_factor}x")

    # Open image
    img = Image.open(input_path)
    print(f"Original size: {img.size}")

    # Crop: remove top 850px
    width, height = img.size
    img_cropped = img.crop((0, crop_top, width, height))
    print(f"After crop: {img_cropped.size}")

    # Scale to 0.5x
    new_width = int(img_cropped.width * scale_factor)
    new_height = int(img_cropped.height * scale_factor)
    img_scaled = img_cropped.resize((new_width, new_height), Image.LANCZOS)
    print(f"After scaling: {img_scaled.size}")

    return img_scaled


def extract_text_with_easyocr(image, languages=['ko', 'en']):
    """Extract text from image using EasyOCR"""
    print(f"Initializing EasyOCR with languages: {languages}")
    reader = easyocr.Reader(languages)

    print("Extracting text...")
    # Convert PIL Image to numpy array
    img_array = np.array(image)

    # Perform OCR
    results = reader.readtext(img_array)

    return results


def main():
    # Step 1: Capture screenshot
    screenshot_path = capture_adb_screenshot("screenshot.png")

    # Step 2: Process image (crop and scale)
    processed_image = process_image(screenshot_path, crop_top=850, scale_factor=0.5)

    # Save processed image for reference
    processed_path = "screenshot_processed.png"
    processed_image.save(processed_path)
    print(f"Processed image saved to {processed_path}")

    # Step 3: Extract text with EasyOCR
    results = extract_text_with_easyocr(processed_image)

    # Step 4: Display results
    print("\n" + "="*50)
    print("OCR RESULTS")
    print("="*50)

    for i, (bbox, text, confidence) in enumerate(results, 1):
        print(f"{i}. Text: {text}")
        print(f"   Confidence: {confidence:.2f}")
        print(f"   BBox: {bbox}")
        print()

    # Save results to file
    output_file = "ocr_results.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        for bbox, text, confidence in results:
            f.write(f"{text}\n")

    print(f"Results saved to {output_file}")


if __name__ == "__main__":
    main()
