"""
Marathi Translation API
A lightweight translation service for English <-> Marathi
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from pathlib import Path
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variables for model
translator = None
MODEL_DIR = Path("models/en-mr-marianmt")

def load_model():
    """Load the MarianMT translation model"""
    global translator
    
    if translator is not None:
        return translator
    
    print("Loading MarianMT model...")
    
    if not MODEL_DIR.exists():
        raise FileNotFoundError(f"Model not found at {MODEL_DIR}. Run: python scripts/download_marianmt.py")
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(str(MODEL_DIR), local_files_only=True)
        model = AutoModelForSeq2SeqLM.from_pretrained(str(MODEL_DIR), local_files_only=True)
        translator = pipeline("translation", model=model, tokenizer=tokenizer, device=-1)
        print("✓ Model loaded successfully")
        return translator
    except Exception as e:
        print(f"✗ Failed to load model: {e}")
        raise

@app.route('/')
def home():
    """Home endpoint with API information"""
    return jsonify({
        "service": "Marathi Translation API",
        "version": "1.0.0",
        "languages": ["en", "mr"],
        "endpoints": {
            "translate": "/translate (POST)",
            "health": "/health (GET)",
            "languages": "/languages (GET)"
        }
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    try:
        if translator is None:
            load_model()
        return jsonify({
            "status": "healthy",
            "model_loaded": translator is not None
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 503

@app.route('/languages', methods=['GET'])
def languages():
    """Get supported languages"""
    return jsonify([
        {
            "code": "en",
            "name": "English",
            "targets": ["mr"]
        },
        {
            "code": "mr",
            "name": "Marathi",
            "targets": ["en"]
        }
    ])

@app.route('/translate', methods=['POST'])
def translate():
    """
    Translate text between English and Marathi
    
    Request body:
    {
        "q": "text to translate" or ["text1", "text2"],
        "source": "en" or "mr",
        "target": "mr" or "en"
    }
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Extract parameters
        text = data.get('q')
        source = data.get('source', '').lower()
        target = data.get('target', '').lower()
        
        # Validate parameters
        if not text:
            return jsonify({"error": "Missing 'q' parameter"}), 400
        
        if not source or not target:
            return jsonify({"error": "Missing 'source' or 'target' parameter"}), 400
        
        if source not in ['en', 'mr'] or target not in ['en', 'mr']:
            return jsonify({"error": "Supported languages: 'en', 'mr'"}), 400
        
        if source == target:
            return jsonify({"error": "Source and target languages must be different"}), 400
        
        # Load model if not loaded
        if translator is None:
            load_model()
        
        # Handle batch translation
        is_batch = isinstance(text, list)
        texts = text if is_batch else [text]
        
        # Translate
        translations = []
        for t in texts:
            if not t or not t.strip():
                translations.append("")
                continue
            
            result = translator(t, max_length=512)
            translated = result[0]['translation_text'] if result else t
            translations.append(translated)
        
        # Return response
        response = {
            "translatedText": translations if is_batch else translations[0],
            "detectedLanguage": {
                "confidence": 100,
                "language": source
            }
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Pre-load model
    print("=" * 60)
    print("Marathi Translation API")
    print("=" * 60)
    
    try:
        load_model()
        print("\nStarting server...")
        
        # Get port from environment or use default
        port = int(os.environ.get('PORT', 5000))
        host = os.environ.get('HOST', '0.0.0.0')
        
        app.run(host=host, port=port, debug=False)
    except Exception as e:
        print(f"\n✗ Failed to start server: {e}")
        exit(1)
