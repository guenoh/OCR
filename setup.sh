#!/bin/bash

# Setup script for OCR project

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing required packages..."
pip install --upgrade pip
pip install easyocr pillow

echo "Setup complete!"
echo "To run the OCR script, use:"
echo "  source venv/bin/activate"
echo "  python ocr_adb_screenshot.py"
