#!/usr/bin/env python3
"""
Download MarianMT model for English ↔ Marathi translation.
This model supports bidirectional translation.
"""

import os
import sys
from pathlib import Path

def download_model():
    """Download the MarianMT English-Marathi model from HuggingFace."""
    
    model_id = 'Helsinki-NLP/opus-mt-en-mr'
    local_dir = Path('./models/en-mr-marianmt')
    
    print("=" * 60)
    print("Downloading MarianMT Model for English ↔ Marathi")
    print("=" * 60)
    print(f"Model: {model_id}")
    print(f"Target: {local_dir.absolute()}")
    print()
    
    try:
        from huggingface_hub import snapshot_download
        
        # Create models directory if it doesn't exist
        local_dir.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if model already exists
        if local_dir.exists() and (local_dir / 'config.json').exists():
            print("Model directory already exists. Checking files...")
            required_files = ['config.json', 'pytorch_model.bin', 'tokenizer_config.json', 'vocab.json', 'source.spm', 'target.spm']
            existing_files = [f for f in required_files if (local_dir / f).exists()]
            
            if len(existing_files) >= 3:  # At least config, model, and tokenizer
                print(f"✓ Found {len(existing_files)} model files")
                print("Skipping download (model already present)")
                print()
                print("To force re-download, delete the models directory:")
                print(f"  rm -rf {local_dir}")
                return True
        
        # Download the model
        print("Downloading model files (this may take a few minutes)...")
        print()
        
        downloaded_path = snapshot_download(
            repo_id=model_id,
            local_dir=str(local_dir),
            local_dir_use_symlinks=False,
            resume_download=True,
            ignore_patterns=["*.h5", "*.ot", "*.msgpack"]  # Skip unnecessary formats
        )
        
        print()
        print("=" * 60)
        print("✓ Model downloaded successfully!")
        print("=" * 60)
        print(f"Location: {local_dir.absolute()}")
        print()
        
        # Verify model files
        required_files = ['config.json', 'pytorch_model.bin', 'tokenizer_config.json']
        missing_files = [f for f in required_files if not (local_dir / f).exists()]
        
        if missing_files:
            print(f"✗ ERROR: Missing required files: {missing_files}")
            print("Download may have failed. Please try again.")
            return False
        
        # List all downloaded files
        all_files = list(local_dir.glob('*'))
        print(f"Downloaded {len(all_files)} files:")
        for f in sorted(all_files):
            if f.is_file():
                size_mb = f.stat().st_size / (1024 * 1024)
                print(f"  • {f.name} ({size_mb:.1f} MB)")
        
        print()
        print("Supported translations:")
        print("  • English → Marathi (en → mr)")
        print("  • Marathi → English (mr → en)")
        print()
        print("✓ Ready to use!")
        
        return True
        
    except ImportError as e:
        print()
        print("=" * 60)
        print("✗ Error: huggingface_hub not installed")
        print("=" * 60)
        print("Install it with: pip install huggingface_hub")
        return False
        
    except Exception as e:
        print()
        print("=" * 60)
        print("✗ Error downloading model")
        print("=" * 60)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        print()
        print("Troubleshooting:")
        print("  1. Check your internet connection")
        print("  2. Ensure you have enough disk space (~500MB)")
        print("  3. Try running again (download will resume)")
        return False

if __name__ == "__main__":
    success = download_model()
    sys.exit(0 if success else 1)
