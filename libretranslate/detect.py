"""
Simplified language detection for English and Marathi.
Uses langdetect for basic language identification.
"""

from langdetect import DetectorFactory, detect_langs, LangDetectException
from langdetect.lang_detect_exception import ErrorCode

# Set seed for reproducible results
DetectorFactory.seed = 0


class Language:
    """Represents a detected language with confidence score."""
    
    def __init__(self, code, confidence):
        self.code = code
        self.confidence = float(confidence)
        self.text_length = 0

    def __str__(self):
        return f"code: {self.code:<9} confidence: {self.confidence:>5.1f}"


def check_lang(langcodes, lang):
    """Check if detected language is in supported language codes."""
    if not langcodes:
        return True
    return normalized_lang_code(lang) in langcodes


def normalized_lang_code(lang):
    """Normalize language code from langdetect format."""
    code = lang.lang
    # Map Marathi variants
    if code in ["mr", "mar"]:
        code = "mr"
    return code


class Detector:
    """Language detector for English and Marathi."""
    
    def __init__(self, langcodes=()):
        self.langcodes = langcodes

    def detect(self, text):
        """
        Detect language of the given text.
        Returns list of Language objects with confidence scores.
        """
        if not text or not text.strip():
            return [Language("en", 0)]
        
        try:
            # Detect languages
            detected = detect_langs(text)
            
            # Filter by supported languages if specified
            if self.langcodes:
                top_choices = [
                    lang for lang in detected 
                    if check_lang(self.langcodes, lang)
                ][:3]
            else:
                top_choices = detected[:3]
            
            # Return default if no matches
            if not top_choices or top_choices[0].prob == 0:
                return [Language("en", 0)]
            
            # Convert to Language objects
            return [
                Language(normalized_lang_code(lang), round(lang.prob * 100)) 
                for lang in top_choices
            ]
            
        except LangDetectException as e:
            if e.code == ErrorCode.CantDetectError:
                return [Language("en", 0)]
            else:
                raise e

