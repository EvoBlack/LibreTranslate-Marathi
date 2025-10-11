#!/usr/bin/env python3
"""
Test script for Marathi Translation API
"""

import requests
import json

def test_api(base_url="http://localhost:5000"):
    """Test the translation API"""
    
    print("=" * 60)
    print("Testing Marathi Translation API")
    print("=" * 60)
    print(f"Base URL: {base_url}\n")
    
    tests = [
        {
            "name": "Health Check",
            "method": "GET",
            "endpoint": "/health",
            "expected": 200
        },
        {
            "name": "Get Languages",
            "method": "GET",
            "endpoint": "/languages",
            "expected": 200
        },
        {
            "name": "English to Marathi",
            "method": "POST",
            "endpoint": "/translate",
            "data": {
                "q": "Hello, how are you?",
                "source": "en",
                "target": "mr"
            },
            "expected": 200
        },
        {
            "name": "Marathi to English",
            "method": "POST",
            "endpoint": "/translate",
            "data": {
                "q": "नमस्कार",
                "source": "mr",
                "target": "en"
            },
            "expected": 200
        },
        {
            "name": "Batch Translation",
            "method": "POST",
            "endpoint": "/translate",
            "data": {
                "q": ["Hello", "Thank you", "Good morning"],
                "source": "en",
                "target": "mr"
            },
            "expected": 200
        }
    ]
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(tests, 1):
        print(f"[{i}/{len(tests)}] {test['name']}")
        
        try:
            url = base_url + test['endpoint']
            
            if test['method'] == 'GET':
                response = requests.get(url, timeout=30)
            else:
                response = requests.post(url, json=test['data'], timeout=30)
            
            if response.status_code == test['expected']:
                data = response.json()
                print(f"  ✓ PASSED")
                if 'translatedText' in data:
                    print(f"  Translation: {data['translatedText']}")
                elif 'status' in data:
                    print(f"  Status: {data['status']}")
                passed += 1
            else:
                print(f"  ✗ FAILED: Expected {test['expected']}, got {response.status_code}")
                print(f"  Response: {response.text}")
                failed += 1
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            failed += 1
        
        print()
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0

if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:5000", help="API base URL")
    args = parser.parse_args()
    
    success = test_api(args.url)
    sys.exit(0 if success else 1)
