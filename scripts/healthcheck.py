#!/usr/bin/env python3
"""
Health check for LibreTranslate Marathi service.
Tests English → Marathi translation.
"""

import requests
import os
import sys

def check_health():
    """Perform health check by testing translation."""
    port = os.environ.get('PORT', os.environ.get('LT_PORT', '5000'))
    url = f'http://localhost:{port}/translate'
    
    try:
        # Test English to Marathi translation
        response = requests.post(
            url=url,
            headers={'Content-Type': 'application/json'},
            json={
                'q': 'Hello',
                'source': 'en',
                'target': 'mr'
            },
            timeout=30
        )
        response.raise_for_status()
        
        # Verify response structure
        data = response.json()
        if 'translatedText' not in data:
            print("✗ Health check failed: No translatedText in response")
            return False
        
        print(f"✓ Health check passed: '{data['translatedText']}'")
        return True
        
    except requests.exceptions.Timeout:
        print("✗ Health check failed: Request timeout")
        return False
    except requests.exceptions.ConnectionError:
        print("✗ Health check failed: Cannot connect to service")
        return False
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False

if __name__ == "__main__":
    success = check_health()
    sys.exit(0 if success else 1)
