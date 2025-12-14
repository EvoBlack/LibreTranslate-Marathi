"""
Marathi Translation API with AI4Bharat IndicTrans2
High-quality translation service for English <-> Marathi
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from pathlib import Path
import os
import json
import torch

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variables
model = None
tokenizer = None
MODEL_DIR = Path("models/indictrans2-en-mr")
translations_dict = None
device = "cuda" if torch.cuda.is_available() else "cpu"

# Language codes for IndicTrans2
LANG_CODE_MAP = {
    "en": "eng_Latn",
    "mr": "mar_Deva"
}

def load_translations_dict():
    """Load the custom translations dictionary"""
    global translations_dict
    
    if translations_dict is not None:
        return translations_dict
    
    dict_path = Path("translations_dict.json")
    if dict_path.exists():
        with open(dict_path, 'r', encoding='utf-8') as f:
            translations_dict = json.load(f)
        print("✓ Translations dictionary loaded")
    else:
        translations_dict = {"en_to_mr": {}, "mr_to_en": {}}
        print("⚠ Translations dictionary not found, using model only")
    
    return translations_dict

def load_model():
    """Load the IndicTrans2 translation model"""
    global model, tokenizer
    
    if model is not None and tokenizer is not None:
        return model, tokenizer
    
    print("Loading IndicTrans2 model...")
    print(f"Device: {device}")
    
    if not MODEL_DIR.exists():
        raise FileNotFoundError(f"Model not found at {MODEL_DIR}. Run: python scripts/download_indictrans2.py")
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(
            str(MODEL_DIR),
            local_files_only=True,
            trust_remote_code=True
        )
        
        model = AutoModelForSeq2SeqLM.from_pretrained(
            str(MODEL_DIR),
            local_files_only=True,
            trust_remote_code=True
        ).to(device)
        
        model.eval()  # Set to evaluation mode
        
        print("✓ IndicTrans2 model loaded successfully")
        return model, tokenizer
    except Exception as e:
        print(f"✗ Failed to load model: {e}")
        raise

def translate_with_indictrans2(text, source_lang, target_lang):
    """
    Translate using IndicTrans2 model
    IndicTrans2 requires input format: "<src_lang> <tgt_lang> <text>"
    """
    if model is None or tokenizer is None:
        load_model()
    
    # Convert language codes
    src_code = LANG_CODE_MAP.get(source_lang, source_lang)
    tgt_code = LANG_CODE_MAP.get(target_lang, target_lang)
    
    # IndicTrans2 expects format: "<src_lang> <tgt_lang> <text>"
    input_text = f"{src_code} {tgt_code} {text}"
    
    # Tokenize
    inputs = tokenizer(
        input_text,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=256
    ).to(device)
    
    # Generate translation
    with torch.no_grad():
        generated_tokens = model.generate(
            **inputs,
            max_length=256,
            num_beams=4,
            num_return_sequences=1,
            early_stopping=True
        )
    
    # Decode
    translation = tokenizer.batch_decode(
        generated_tokens,
        skip_special_tokens=True
    )[0]
    
    # Clean up output
    translation = translation.strip()
    
    return translation

def translate_with_dict(text, source, target):
    """
    Translate using dictionary first, fallback to IndicTrans2
    Returns (translation, used_dict)
    """
    dict_data = load_translations_dict()
    
    # Normalize text for dictionary lookup
    text_lower = text.lower().strip()
    
    # Check dictionary first
    if source == "en" and target == "mr":
        if text_lower in dict_data["en_to_mr"]:
            return dict_data["en_to_mr"][text_lower], True
    elif source == "mr" and target == "en":
        if text in dict_data["mr_to_en"]:
            return dict_data["mr_to_en"][text], True
    
    # Fallback to IndicTrans2 model
    try:
        translated = translate_with_indictrans2(text, source, target)
        return translated, False
    except Exception as e:
        print(f"Translation error: {e}")
        return text, False

@app.route('/')
def home():
    """Home endpoint with API information"""
    return jsonify({
        "service": "Marathi Translation API (IndicTrans2)",
        "version": "2.0.0",
        "model": "AI4Bharat IndicTrans2",
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
        if model is None or tokenizer is None:
            load_model()
        return jsonify({
            "status": "healthy",
            "model": "IndicTrans2",
            "model_loaded": model is not None,
            "device": device
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
        
        # Load model and dictionary if not loaded
        if model is None or tokenizer is None:
            load_model()
        load_translations_dict()
        
        # Handle batch translation
        is_batch = isinstance(text, list)
        texts = text if is_batch else [text]
        
        # Translate
        translations = []
        for t in texts:
            if not t or not t.strip():
                translations.append("")
                continue
            
            translated, from_dict = translate_with_dict(t, source, target)
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
        print(f"Error in translate endpoint: {e}")
        import traceback
        traceback.print_exc()
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
    print("Marathi Translation API (IndicTrans2)")
    print("=" * 60)
    
    try:
        load_translations_dict()
        load_model()
        print("\nStarting server...")
        
        # Get port from environment or use default (7860 for HF Spaces)
        port = int(os.environ.get('PORT', 7860))
        host = os.environ.get('HOST', '0.0.0.0')
        
        app.run(host=host, port=port, debug=False)
    except Exception as e:
        print(f"\n✗ Failed to start server: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
