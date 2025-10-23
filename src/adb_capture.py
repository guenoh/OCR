#!/usr/bin/env python3
"""ADB Screenshot Capture Module"""

import subprocess
import os


def capture_screenshot(output_path="screenshot.png"):
    """
    Capture screenshot from Android device using adb

    Args:
        output_path (str): Path to save the screenshot

    Returns:
        str: Path to the saved screenshot
    """
    print("📱 Capturing screenshot via adb...")

    try:
        # Capture screenshot on device
        subprocess.run(
            ["adb", "shell", "screencap", "-p", "/sdcard/screenshot.png"],
            check=True
        )

        # Pull screenshot from device
        subprocess.run(
            ["adb", "pull", "/sdcard/screenshot.png", output_path],
            check=True
        )

        # Clean up device
        subprocess.run(
            ["adb", "shell", "rm", "/sdcard/screenshot.png"],
            check=True
        )

        print(f"✅ Screenshot saved to {output_path}")
        return output_path

    except subprocess.CalledProcessError as e:
        print(f"❌ Error capturing screenshot: {e}")
        raise
