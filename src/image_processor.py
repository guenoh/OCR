#!/usr/bin/env python3
"""Image Processing Module"""

from PIL import Image, ImageEnhance, ImageFilter


def process_image(input_path, crop_left=850, scale_factor=0.5, enhance=True):
    """
    Process image: crop left pixels, scale, and enhance for OCR

    Args:
        input_path (str): Path to input image
        crop_left (int): Number of pixels to crop from left
        scale_factor (float): Scaling factor
        enhance (bool): Apply image enhancement for better OCR

    Returns:
        PIL.Image: Processed image
    """
    print(f"🖼️  Processing image: crop_left={crop_left}px, scale={scale_factor}x")

    # Open image
    img = Image.open(input_path)
    print(f"   Original size: {img.size}")

    # Crop: remove left pixels
    width, height = img.size
    img_cropped = img.crop((crop_left, 0, width, height))
    print(f"   After crop: {img_cropped.size}")

    # Scale
    new_width = int(img_cropped.width * scale_factor)
    new_height = int(img_cropped.height * scale_factor)
    img_scaled = img_cropped.resize((new_width, new_height), Image.LANCZOS)
    print(f"   After scaling: {img_scaled.size}")

    # Enhance image for better OCR
    if enhance:
        print(f"   Applying enhancements...")

        # Increase contrast
        enhancer = ImageEnhance.Contrast(img_scaled)
        img_scaled = enhancer.enhance(1.3)  # 30% more contrast

        # Increase sharpness
        enhancer = ImageEnhance.Sharpness(img_scaled)
        img_scaled = enhancer.enhance(1.5)  # 50% more sharpness

        # Apply slight unsharp mask for better edge detection
        img_scaled = img_scaled.filter(ImageFilter.UnsharpMask(radius=1, percent=100, threshold=3))

        print(f"   ✓ Enhancements applied")

    return img_scaled
