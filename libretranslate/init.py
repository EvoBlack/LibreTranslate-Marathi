import os
import sys

def boot(load_only=None, update_models=False, install_models=False):
    """
    Simplified boot for Marathi-only translation using HuggingFace models.
    No Argos model installation needed.
    """
    print("Marathi translation service - using HuggingFace MarianMT models")
    print("Skipping Argos model installation (not needed for HF-based translation)")
    
    # Verify HF model is available
    from pathlib import Path
    model_dir = Path(__file__).resolve().parents[1] / "models" / "en-mr-marianmt"
    
    if not model_dir.exists():
        print(f"✗ ERROR: MarianMT model not found at {model_dir}")
        print("  The model must be downloaded before starting the service.")
        print("  Run: python scripts/download_marianmt.py")
        raise FileNotFoundError(f"Model directory not found: {model_dir}")
    
    # Check for required model files
    required_files = ['config.json', 'pytorch_model.bin', 'tokenizer_config.json']
    missing_files = [f for f in required_files if not (model_dir / f).exists()]
    
    if missing_files:
        print(f"✗ ERROR: Missing model files: {missing_files}")
        print(f"  Model directory: {model_dir}")
        print("  Re-download the model: python scripts/download_marianmt.py")
        raise FileNotFoundError(f"Missing model files: {missing_files}")
    
    print(f"✓ MarianMT model verified at {model_dir}")
    return
