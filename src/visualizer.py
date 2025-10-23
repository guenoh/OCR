#!/usr/bin/env python3
"""OCR Results Visualization Module"""

from PIL import Image, ImageDraw, ImageFont
import os


def draw_ocr_results(image, ocr_results, font_path=None, font_size=20):
    """
    Draw rectangles and text on image based on OCR results

    Args:
        image (PIL.Image): Input image
        ocr_results (list): OCR results with bbox, text, and confidence
        font_path (str): Path to font file for Korean/English text
        font_size (int): Font size for text display

    Returns:
        PIL.Image: Image with drawn rectangles and text
    """
    print(f"🎨 Drawing OCR results on image...")

    # Create a copy to draw on
    img_draw = image.copy()
    draw = ImageDraw.Draw(img_draw)

    # Load font
    try:
        if font_path and os.path.exists(font_path):
            font = ImageFont.truetype(font_path, font_size)
            print(f"   Using font: {font_path}")
        else:
            # Try to find Hyundai font in fonts directory
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            default_font = os.path.join(project_root, "fonts", "HyundaiSansUI_JP_KR_Latin-Regular.ttf")

            if os.path.exists(default_font):
                font = ImageFont.truetype(default_font, font_size)
                print(f"   Using default font: {default_font}")
            else:
                font = ImageFont.load_default()
                print("   Using system default font")
    except Exception as e:
        print(f"   Warning: Could not load font ({e}), using default")
        font = ImageFont.load_default()

    # Draw each detected text region
    for i, (bbox, text, confidence) in enumerate(ocr_results):
        # Extract coordinates
        top_left = tuple(map(int, bbox[0]))
        top_right = tuple(map(int, bbox[1]))
        bottom_right = tuple(map(int, bbox[2]))
        bottom_left = tuple(map(int, bbox[3]))

        # Draw rectangle
        points = [top_left, top_right, bottom_right, bottom_left, top_left]

        # Color based on confidence: green (high) to red (low)
        if confidence > 0.8:
            color = (0, 255, 0)  # Green
        elif confidence > 0.6:
            color = (255, 165, 0)  # Orange
        else:
            color = (255, 0, 0)  # Red

        draw.line(points, fill=color, width=3)

        # Draw text above the rectangle with background
        text_bbox = draw.textbbox(top_left, text, font=font)
        text_bg_coords = [
            (text_bbox[0] - 2, text_bbox[1] - 2),
            (text_bbox[2] + 2, text_bbox[3] + 2)
        ]
        draw.rectangle(text_bg_coords, fill=(0, 0, 0, 128))
        draw.text(top_left, text, fill=(255, 255, 255), font=font)

        # Draw confidence score
        conf_text = f"{confidence:.2f}"
        conf_pos = (top_left[0], top_left[1] - 20)
        draw.text(conf_pos, conf_text, fill=color, font=font)

    print(f"✅ Drew {len(ocr_results)} text regions")
    return img_draw


def save_results(ocr_results, output_file="ocr_results.txt"):
    """
    Save OCR results to text file

    Args:
        ocr_results (list): OCR results
        output_file (str): Output file path
    """
    print(f"💾 Saving results to {output_file}...")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("OCR EXTRACTION RESULTS\n")
        f.write("="*60 + "\n\n")

        for i, (bbox, text, confidence) in enumerate(ocr_results, 1):
            f.write(f"{i}. Text: {text}\n")
            f.write(f"   Confidence: {confidence:.2%}\n")
            f.write(f"   BBox: {bbox}\n")
            f.write("\n")

    print(f"✅ Results saved")


def print_results(ocr_results):
    """
    Print OCR results to console

    Args:
        ocr_results (list): OCR results
    """
    print("\n" + "="*60)
    print("OCR EXTRACTION RESULTS")
    print("="*60)

    for i, (bbox, text, confidence) in enumerate(ocr_results, 1):
        print(f"{i}. Text: {text}")
        print(f"   Confidence: {confidence:.2%}")
        print(f"   BBox: {bbox}")
        print()
