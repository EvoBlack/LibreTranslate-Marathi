#!/usr/bin/env python3
"""Quick API test script"""

import requests
import time

API_URL = "http://localhost:7860"

def test_health():
    """Test health endpoint"""
    print("1. Testing /health endpoint...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Health check passed")
            print(f"   Model: {data.get('model')}")
            print(f"   Device: {data.get('device')}")
            return True
        else:
            print(f"   ✗ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def test_languages():
    """Test languages endpoint"""
    print("\n2. Testing /languages endpoint...")
    try:
        response = requests.get(f"{API_URL}/languages", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Found {len(data)} languages")
            for lang in data:
                print(f"     - {lang['name']} ({lang['code']})")
            return True
        else:
            print(f"   ✗ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def test_translation(text, source, target, description):
    """Test translation"""
    print(f"\n3. Testing translation: {description}")
    print(f"   Input: '{text}' ({source} → {target})")
    try:
        start = time.time()
        response = requests.post(
            f"{API_URL}/translate",
            json={"q": text, "source": source, "target": target},
            timeout=30
        )
        elapsed = (time.time() - start) * 1000
        
        if response.status_code == 200:
            data = response.json()
            translated = data.get("translatedText", "")
            print(f"   Output: '{translated}'")
            print(f"   ✓ Translation successful ({elapsed:.0f}ms)")
            return True
        else:
            print(f"   ✗ Failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def test_batch_translation():
    """Test batch translation"""
    print("\n4. Testing batch translation...")
    texts = ["Hello", "Thank you", "Good morning"]
    print(f"   Input: {texts}")
    try:
        start = time.time()
        response = requests.post(
            f"{API_URL}/translate",
            json={"q": texts, "source": "en", "target": "mr"},
            timeout=30
        )
        elapsed = (time.time() - start) * 1000
        
        if response.status_code == 200:
            data = response.json()
            translated = data.get("translatedText", [])
            print(f"   Output: {translated}")
            print(f"   ✓ Batch translation successful ({elapsed:.0f}ms)")
            return True
        else:
            print(f"   ✗ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Quick API Test")
    print("=" * 60)
    
    results = []
    
    # Test health
    results.append(test_health())
    
    # Test languages
    results.append(test_languages())
    
    # Test English to Marathi
    results.append(test_translation(
        "Hello world", 
        "en", 
        "mr", 
        "English to Marathi (sentence)"
    ))
    
    # Test dictionary translation
    results.append(test_translation(
        "Home", 
        "en", 
        "mr", 
        "English to Marathi (dictionary word)"
    ))
    
    # Test Marathi to English
    results.append(test_translation(
        "नमस्कार", 
        "mr", 
        "en", 
        "Marathi to English"
    ))
    
    # Test batch
    results.append(test_batch_translation())
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ ALL TESTS PASSED! Ready to deploy! 🚀")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check errors above.")
    print("=" * 60)
