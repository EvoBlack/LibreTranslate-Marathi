#!/usr/bin/env python3
"""
Download AI4Bharat IndicTrans2 model for English ↔ Marathi translation.
This model provides high-quality translations for Indic languages.
"""

import os
import sys
from pathlib import Path

def download_model():
    """Download the IndicTrans2 English-Marathi model from HuggingFace."""
    
    # Using the distilled model for better performance
    model_id = 'ai4bharat/indictrans2-en-indic-dist-200M'
    local_dir = Path('./models/indictrans2-en-mr')
    
    print("=" * 60)
    print("Downloading IndicTrans2 Model for English ↔ Marathi")
    print("=" * 60)
    print(f"Model: {model_id}")
    print(f"Target: {local_dir.absolute()}")
    print()
    print("This is a distilled 200M parameter model optimized for:")
    print("  • Fast inference")
    print("  • High accuracy")
    print("  • All 22 Indic languages including Marathi")
    print()
    
    try:
        from huggingface_hub import snapshot_download
        
        # Create models directory if it doesn't exist
        local_dir.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if model already exists
        if local_dir.exists() and (local_dir / 'config.json').exists():
            print("Model directory already exists. Checking files...")
            required_files = ['config.json', 'pytorch_model.bin', 'tokenizer_config.json']
            existing_files = [f for f in required_files if (local_dir / f).exists()]
            
            if len(existing_files) >= 2:
                print(f"✓ Found {len(existing_files)} model files")
                print("Skipping download (model already present)")
                print()
                print("To force re-download, delete the models directory:")
                print(f"  rm -rf {local_dir}")
                return True
        
        # Download the model
        print("Downloading model files (this may take 5-10 minutes)...")
        print("Model size: ~800MB")
        print()
        
        downloaded_path = snapshot_download(
            repo_id=model_id,
            local_dir=str(local_dir),
            local_dir_use_symlinks=False,
            resume_download=True,
            ignore_patterns=["*.h5", "*.ot", "*.msgpack", "*.safetensors"]
        )
        
        print()
        print("=" * 60)
        print("✓ Model downloaded successfully!")
        print("=" * 60)
        print(f"Location: {local_dir.absolute()}")
        print()
        
        # Verify model files
        required_files = ['config.json', 'pytorch_model.bin']
        missing_files = [f for f in required_files if not (local_dir / f).exists()]
        
        if missing_files:
            print(f"✗ ERROR: Missing required files: {missing_files}")
            print("Download may have failed. Please try again.")
            return False
        
        # List all downloaded files
        all_files = list(local_dir.glob('*'))
        print(f"Downloaded {len(all_files)} files:")
        for f in sorted(all_files)[:10]:  # Show first 10 files
            if f.is_file():
                size_mb = f.stat().st_size / (1024 * 1024)
                print(f"  • {f.name} ({size_mb:.1f} MB)")
        
        if len(all_files) > 10:
            print(f"  ... and {len(all_files) - 10} more files")
        
        print()
        print("Supported translations:")
        print("  • English → Marathi (en → mr)")
        print("  • Marathi → English (mr → en)")
        print("  • Plus 21 other Indic languages")
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
        print("  2. Ensure you have enough disk space (~1GB)")
        print("  3. Try running again (download will resume)")
        return False

if __name__ == "__main__":
    success = download_model()
    sys.exit(0 if success else 1)
