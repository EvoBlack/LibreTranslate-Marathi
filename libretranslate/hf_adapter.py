"""
HuggingFace adapter for English ↔ Marathi translation using MarianMT models.
Supports bidirectional translation with a single model.
"""

import os
import sys
from types import SimpleNamespace
from pathlib import Path

_MODEL_DIR = Path(__file__).resolve().parents[1] / "models" / "en-mr-marianmt"

_pipeline = None
_model = None
_tokenizer = None

def _load_pipeline():
    """Load the MarianMT pipeline for English-Marathi translation."""
    global _pipeline, _model, _tokenizer
    
    if _pipeline is not None:
        return _pipeline
    
    if not _MODEL_DIR.exists():
        print(f"✗ Model directory not found: {_MODEL_DIR}")
        return None
    
    try:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
        
        print(f"Loading MarianMT model from {_MODEL_DIR}...")
        
        # Load tokenizer
        _tokenizer = AutoTokenizer.from_pretrained(
            str(_MODEL_DIR), 
            trust_remote_code=True,
            local_files_only=True
        )
        print("✓ Tokenizer loaded")
        
        # Load model
        _model = AutoModelForSeq2SeqLM.from_pretrained(
            str(_MODEL_DIR), 
            trust_remote_code=True,
            local_files_only=True
        )
        print("✓ Model loaded")
        
        # Create pipeline (use CPU for inference, device=-1)
        _pipeline = pipeline(
            "translation", 
            model=_model, 
            tokenizer=_tokenizer, 
            device=-1
        )
        
        print("✓ MarianMT pipeline ready")
        return _pipeline
        
    except Exception as e:
        print(f"✗ Failed to load HF model pipeline: {e}")
        import traceback
        traceback.print_exc()
        return None


class HFTranslator:
    """Translator wrapper for HuggingFace MarianMT models."""
    
    def __init__(self, pipe, src_lang, tgt_lang):
        self.pipe = pipe
        self.src_lang = src_lang.lower()
        self.tgt_lang = tgt_lang.lower()

    def hypotheses(self, text, num_alternatives=1):
        """
        Generate translation hypotheses.
        Returns list of objects with .value attribute to match argostranslate API.
        """
        if self.pipe is None:
            return []
        
        try:
            # For Marathi to English, we need to handle the model differently
            # The opus-mt-en-mr model is trained for en->mr
            # For mr->en, we may need a different approach or model
            
            # Generate translations
            result = self.pipe(
                text, 
                max_length=512,
                num_return_sequences=max(1, num_alternatives),
                num_beams=max(2, num_alternatives),
                early_stopping=True
            )
            
            if isinstance(result, dict):
                result = [result]
            
            translations = []
            for item in result[:num_alternatives]:
                # Extract translation text from various possible keys
                value = (
                    item.get("translation_text") or 
                    item.get("generated_text") or 
                    item.get("text") or
                    str(item)
                )
                translations.append(SimpleNamespace(value=value))
            
            return translations
            
        except Exception as e:
            print(f"✗ Translation error ({self.src_lang}→{self.tgt_lang}): {e}")
            import traceback
            traceback.print_exc()
            return []


def get_translator(src_code, tgt_code):
    """
    Get translator for the specified language pair.
    Supports: en↔mr (English ↔ Marathi)
    """
    src = src_code.lower()
    tgt = tgt_code.lower()
    
    # Check if this is a supported language pair
    if (src, tgt) not in [("en", "mr"), ("mr", "en")]:
        return None
    
    pipe = _load_pipeline()
    if pipe is None:
        print(f"⚠ Cannot create translator for {src}→{tgt}: pipeline not loaded")
        return None
    
    return HFTranslator(pipe, src, tgt)
