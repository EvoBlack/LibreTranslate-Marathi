#!/usr/bin/env python3
"""
Test script for IndicTrans2-powered Marathi Translation API
Tests both dictionary and model translations
"""

import requests
import json
import time

API_URL = "https://evoblack-libretranslate-marathi.hf.space/translate"
HEALTH_URL = "https://evoblack-libretranslate-marathi.hf.space/health"

# Test cases for dictionary (should be instant and 100% accurate)
dictionary_tests = [
    {"input": "Home", "expected": "घर", "source": "en", "target": "mr"},
    {"input": "Profile", "expected": "प्रोफाइल", "source": "en", "target": "mr"},
    {"input": "Settings", "expected": "सेटिंग्स", "source": "en", "target": "mr"},
    {"input": "Driver", "expected": "चालक", "source": "en", "target": "mr"},
    {"input": "Host", "expected": "यजमान", "source": "en", "target": "mr"},
    {"input": "Events", "expected": "कार्यक्रम", "source": "en", "target": "mr"},
    {"input": "Login", "expected": "लॉगिन", "source": "en", "target": "mr"},
    {"input": "Logout", "expected": "लॉगआउट", "source": "en", "target": "mr"},
    {"input": "Welcome", "expected": "स्वागत", "source": "en", "target": "mr"},
    {"input": "Search", "expected": "शोधा", "source": "en", "target": "mr"},
]

# Test cases for model (sentences - quality check)
model_tests = [
    {"input": "Hello, how are you?", "source": "en", "target": "mr", "description": "Simple greeting"},
    {"input": "I love programming", "source": "en", "target": "mr", "description": "Simple sentence"},
    {"input": "Thank you very much", "source": "en", "target": "mr", "description": "Gratitude expression"},
    {"input": "Good morning", "source": "en", "target": "mr", "description": "Time greeting"},
    {"input": "Please help me", "source": "en", "target": "mr", "description": "Request"},
]

def test_translation(text, source, target, expected=None):
    """Test a single translation"""
    try:
        start_time = time.time()
        response = requests.post(
            API_URL,
            json={"q": text, "source": source, "target": target},
            timeout=30
        )
        elapsed = (time.time() - start_time) * 1000  # Convert to ms
        
        if response.status_code == 200:
            data = response.json()
            translated = data.get("translatedText", "")
            
            if expected:
                # Check if translation matches expected
                is_correct = translated == expected
                status = "✅ PASS" if is_correct else "❌ FAIL"
                print(f"{status} | {text:20} → {translated:25} ({elapsed:.0f}ms)")
                return is_correct
            else:
                # Just show the translation (no expected value)
                print(f"✓ | {text:30} → {translated:30} ({elapsed:.0f}ms)")
                return True
        else:
            print(f"❌ ERROR | {text:20} → HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR | {text:20} → {str(e)}")
        return False

def check_health():
    """Check API health and model info"""
    try:
        response = requests.get(HEALTH_URL, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ API is healthy")
            print(f"   Model: {data.get('model', 'Unknown')}")
            print(f"   Device: {data.get('device', 'Unknown')}")
            print(f"   Model Loaded: {data.get('model_loaded', False)}")
            return True
        else:
            print(f"⚠️  API returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Could not reach API: {e}")
        print("\n⏳ The Space might still be building.")
        print("   Wait 10-15 minutes and try again.")
        print("   Check status: https://huggingface.co/spaces/Evoblack/LibreTranslate-Marathi")
        return False

def main():
    print("=" * 80)
    print("Testing IndicTrans2-Powered Marathi Translation API")
    print("=" * 80)
    print(f"API URL: {API_URL}")
    print()
    
    # Check health
    print("Checking API health...")
    if not check_health():
        return
    
    print()
    
    # Test dictionary translations
    print("=" * 80)
    print("Testing Dictionary Translations (UI Terms)")
    print("=" * 80)
    print("These should be instant (<10ms) and 100% accurate")
    print("-" * 80)
    
    dict_passed = 0
    dict_failed = 0
    
    for test in dictionary_tests:
        result = test_translation(
            test["input"],
            test["source"],
            test["target"],
            test["expected"]
        )
        if result:
            dict_passed += 1
        else:
            dict_failed += 1
        time.sleep(0.3)
    
    print("-" * 80)
    print(f"Dictionary Results: {dict_passed}/{len(dictionary_tests)} passed")
    print()
    
    # Test model translations
    print("=" * 80)
    print("Testing Model Translations (Sentences)")
    print("=" * 80)
    print("These use IndicTrans2 model for high-quality translation")
    print("-" * 80)
    
    model_passed = 0
    
    for test in model_tests:
        print(f"\n{test['description']}:")
        result = test_translation(
            test["input"],
            test["source"],
            test["target"]
        )
        if result:
            model_passed += 1
        time.sleep(0.5)
    
    print("-" * 80)
    print(f"Model Results: {model_passed}/{len(model_tests)} completed")
    print()
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    if dict_failed == 0:
        print("✅ Dictionary translations: PERFECT (100% accuracy)")
    else:
        print(f"⚠️  Dictionary translations: {dict_passed}/{len(dictionary_tests)} passed")
    
    print(f"✅ Model translations: {model_passed}/{len(model_tests)} completed")
    
    if dict_failed == 0 and model_passed == len(model_tests):
        print("\n🎉 All tests passed! IndicTrans2 is working perfectly!")
    elif dict_failed > 0:
        print(f"\n⚠️  {dict_failed} dictionary test(s) failed.")
        print("   This might mean the dictionary file wasn't loaded.")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
