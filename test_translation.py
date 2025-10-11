#!/usr/bin/env python3
"""
Test script for LibreTranslate Marathi service.
Tests both English → Marathi and Marathi → English translation.
"""

import requests
import json
import sys

def test_translation(base_url="http://localhost:5000"):
    """Test the translation service."""
    
    print("=" * 60)
    print("LibreTranslate Marathi - Translation Test")
    print("=" * 60)
    print(f"Testing service at: {base_url}\n")
    
    tests = [
        {
            "name": "English → Marathi",
            "text": "Hello, how are you?",
            "source": "en",
            "target": "mr"
        },
        {
            "name": "Marathi → English",
            "text": "नमस्कार, तुम्ही कसे आहात?",
            "source": "mr",
            "target": "en"
        },
        {
            "name": "English → Marathi (Long)",
            "text": "Machine translation is the task of automatically converting text from one language to another.",
            "source": "en",
            "target": "mr"
        },
        {
            "name": "Batch Translation",
            "text": ["Hello", "Good morning", "Thank you"],
            "source": "en",
            "target": "mr"
        }
    ]
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(tests, 1):
        print(f"[Test {i}/{len(tests)}] {test['name']}")
        print(f"  Input: {test['text']}")
        
        try:
            response = requests.post(
                f"{base_url}/translate",
                headers={"Content-Type": "application/json"},
                json={
                    "q": test["text"],
                    "source": test["source"],
                    "target": test["target"]
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                translated = data.get("translatedText", "")
                print(f"  Output: {translated}")
                print(f"  ✓ PASSED\n")
                passed += 1
            else:
                print(f"  ✗ FAILED: HTTP {response.status_code}")
                print(f"  Error: {response.text}\n")
                failed += 1
                
        except Exception as e:
            print(f"  ✗ FAILED: {e}\n")
            failed += 1
    
    # Test language list
    print(f"[Test {len(tests)+1}/{len(tests)+1}] Get Languages")
    try:
        response = requests.get(f"{base_url}/languages", timeout=10)
        if response.status_code == 200:
            langs = response.json()
            print(f"  Languages: {[l['code'] for l in langs]}")
            print(f"  ✓ PASSED\n")
            passed += 1
        else:
            print(f"  ✗ FAILED: HTTP {response.status_code}\n")
            failed += 1
    except Exception as e:
        print(f"  ✗ FAILED: {e}\n")
        failed += 1
    
    # Summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Total: {passed + failed}")
    print(f"Passed: {passed} ✓")
    print(f"Failed: {failed} ✗")
    print("=" * 60)
    
    return failed == 0

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test LibreTranslate Marathi service")
    parser.add_argument(
        "--url",
        default="http://localhost:5000",
        help="Base URL of the service (default: http://localhost:5000)"
    )
    
    args = parser.parse_args()
    
    success = test_translation(args.url)
    sys.exit(0 if success else 1)
