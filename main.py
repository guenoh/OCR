#!/usr/bin/env python3
"""
OCR Project - Main Entry Point
Captures screenshot via ADB → Extracts text with OCR → Visualizes with rectangles and text
"""

import os
import sys
import time
from src.adb_capture import capture_screenshot
from src.image_processor import process_image
from src.ocr_extractor import extract_text
from src.visualizer import draw_ocr_results, save_results, print_results
from src.text_corrector import correct_ocr_results, get_dictionary_stats


def main():
    """Main execution flow"""
    print("="*60)
    print("📱 ADB Screenshot OCR with Visualization")
    print("="*60 + "\n")

    # Start total timer
    total_start = time.time()

    # Configuration
    SCREENSHOT_PATH = "screenshot.png"
    PROCESSED_PATH = "screenshot_processed.png"
    VISUALIZED_PATH = "screenshot_with_ocr.png"
    RESULTS_PATH = "ocr_results.txt"

    CROP_LEFT = 850
    SCALE_FACTOR = 0.6  # 0.6x = 정확도 향상
    LANGUAGES = ['ko', 'en']  # 한글 + 영문

    # Performance optimization settings
    USE_GPU = True           # GPU 사용 (자동 감지)
    OPTIMIZE_PARAMS = False  # 파라미터 최적화 OFF (속도 우선)
    ENHANCE_IMAGE = False    # 이미지 전처리 OFF (속도 우선)
    TEXT_CORRECTION = True   # 텍스트 오타 보정
    CORRECTION_THRESHOLD = 0.8  # 신뢰도 80% 이하만 보정

    try:
        # Step 1: Capture screenshot via ADB
        print("STEP 1: Capture Screenshot")
        print("-" * 60)
        step1_start = time.time()
        screenshot_path = capture_screenshot(SCREENSHOT_PATH)
        step1_time = (time.time() - step1_start) * 1000
        print(f"⏱️  Time: {step1_time:.2f}ms")
        print()

        # Step 2: Process image (crop and scale)
        print("STEP 2: Process Image")
        print("-" * 60)
        step2_start = time.time()
        processed_image = process_image(
            screenshot_path,
            crop_left=CROP_LEFT,
            scale_factor=SCALE_FACTOR,
            enhance=ENHANCE_IMAGE
        )

        # Save processed image for reference
        processed_image.save(PROCESSED_PATH)
        print(f"💾 Processed image saved to {PROCESSED_PATH}")
        step2_time = (time.time() - step2_start) * 1000
        print(f"⏱️  Time: {step2_time:.2f}ms")
        print()

        # Step 3: Extract text with OCR
        print("STEP 3: Extract Text with OCR")
        print("-" * 60)
        step3_start = time.time()
        ocr_results = extract_text(
            processed_image,
            languages=LANGUAGES,
            use_gpu=USE_GPU,
            optimize_params=OPTIMIZE_PARAMS
        )
        step3_time = (time.time() - step3_start) * 1000
        print(f"⏱️  Time: {step3_time:.2f}ms")
        print()

        # Step 3.5: Text Correction (오타 보정)
        if TEXT_CORRECTION:
            print("STEP 3.5: Text Correction")
            print("-" * 60)
            step35_start = time.time()

            stats = get_dictionary_stats()
            print(f"📚 사전 로드: {stats['total']}개 단어")

            ocr_results, correction_count = correct_ocr_results(
                ocr_results,
                confidence_threshold=CORRECTION_THRESHOLD
            )

            step35_time = (time.time() - step35_start) * 1000
            print(f"✅ 보정 완료: {correction_count}개 단어 수정")
            print(f"⏱️  Time: {step35_time:.2f}ms")
            print()
        else:
            step35_time = 0

        # Step 4: Visualize results (draw rectangles and text)
        print("STEP 4: Visualize OCR Results")
        print("-" * 60)
        step4_start = time.time()
        visualized_image = draw_ocr_results(processed_image, ocr_results)
        visualized_image.save(VISUALIZED_PATH)
        print(f"💾 Visualization saved to {VISUALIZED_PATH}")
        step4_time = (time.time() - step4_start) * 1000
        print(f"⏱️  Time: {step4_time:.2f}ms")
        print()

        # Step 5: Save and display results
        print("STEP 5: Save Results")
        print("-" * 60)
        step5_start = time.time()
        save_results(ocr_results, RESULTS_PATH)
        print_results(ocr_results)
        step5_time = (time.time() - step5_start) * 1000
        print(f"⏱️  Time: {step5_time:.2f}ms")

        # Total time
        total_time = (time.time() - total_start) * 1000

        print("\n" + "="*60)
        print("⏱️  PERFORMANCE SUMMARY")
        print("="*60)
        print(f"Step 1 (ADB Capture):     {step1_time:>10.2f}ms")
        print(f"Step 2 (Image Process):   {step2_time:>10.2f}ms")
        print(f"Step 3 (OCR Extract):     {step3_time:>10.2f}ms")
        if TEXT_CORRECTION:
            print(f"Step 3.5 (Text Correct):  {step35_time:>10.2f}ms")
        print(f"Step 4 (Visualization):   {step4_time:>10.2f}ms")
        print(f"Step 5 (Save Results):    {step5_time:>10.2f}ms")
        print("-"*60)
        print(f"Total Time:               {total_time:>10.2f}ms ({total_time/1000:.2f}s)")
        print("="*60)

        print("\n✅ Complete! Check these files:")
        print(f"   - Original: {SCREENSHOT_PATH}")
        print(f"   - Processed: {PROCESSED_PATH}")
        print(f"   - Visualized: {VISUALIZED_PATH}")
        print(f"   - Text results: {RESULTS_PATH}")
        print("="*60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
