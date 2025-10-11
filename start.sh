#!/bin/bash
set -e

echo "============================================================"
echo "LibreTranslate Marathi - Startup Script"
echo "============================================================"

# Check if model exists
if [ ! -d "models/en-mr-marianmt" ]; then
    echo "ERROR: Model directory not found!"
    echo "Downloading model..."
    python scripts/download_marianmt.py
fi

# Verify model files
if [ ! -f "models/en-mr-marianmt/config.json" ]; then
    echo "ERROR: Model files incomplete!"
    echo "Re-downloading model..."
    python scripts/download_marianmt.py
fi

echo ""
echo "✓ Model verified"
echo ""

# Start the application
echo "Starting LibreTranslate Marathi service..."
echo "============================================================"
exec python main.py "$@"
