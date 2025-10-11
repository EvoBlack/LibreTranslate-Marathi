#!/usr/bin/env python3
"""
LibreTranslate Marathi - English ↔ Marathi Translation Service
Uses HuggingFace MarianMT models for high-quality translation
"""

import sys
import os

print("=" * 60)
print("LibreTranslate Marathi - English ↔ Marathi Translation")
print("=" * 60)

# Pre-initialize everything before starting Flask
print("\n[1/4] Initializing translation service...")
try:
    from libretranslate.init import boot
    boot(load_only=['en', 'mr'], install_models=False)
    print("✓ Service initialized")
except Exception as e:
    print(f"⚠ Initialization warning: {e}")

# Pre-load languages
print("\n[2/4] Loading language definitions...")
try:
    from libretranslate.language import load_languages
    langs = load_languages()
    print(f"✓ Loaded {len(langs)} languages: {[l.code for l in langs]}")
except Exception as e:
    print(f"✗ Failed to load languages: {e}")
    sys.exit(1)

# Pre-load HF model
print("\n[3/4] Loading MarianMT model...")
try:
    from libretranslate import hf_adapter
    pipe = hf_adapter._load_pipeline()
    if pipe:
        print("✓ MarianMT model loaded successfully")
        # Test translation to ensure it works
        test_result = pipe("Hello", max_length=50)
        print(f"✓ Model test successful: {test_result}")
    else:
        print("✗ MarianMT model not found!")
        print("  Run: python scripts/download_marianmt.py")
        sys.exit(1)
except Exception as e:
    print(f"✗ Model loading failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Start the service
print("\n[4/4] Starting Flask application...")
print("=" * 60)
from libretranslate import main

if __name__ == "__main__":
    main()
