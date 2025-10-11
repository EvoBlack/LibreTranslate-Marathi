# LibreTranslate Marathi

A specialized, optimized LibreTranslate service for **English ↔ Marathi** translation using HuggingFace MarianMT models.

## ✨ Features

- **🔄 Bidirectional Translation**: English ↔ Marathi with a single model
- **🚀 High Performance**: Optimized for production deployment
- **🎯 Focused**: Only Marathi translation - no unnecessary dependencies
- **🐳 Docker Ready**: Containerized and ready to deploy
- **☁️ Cloud Compatible**: Works on Render, Railway, Fly.io, etc.
- **📦 Minimal Dependencies**: Stripped down to essentials

## 🌐 Supported Languages

| Language | Code | Direction |
|----------|------|-----------|
| English  | `en` | Source & Target |
| Marathi  | `mr` | Source & Target |

## 🤖 Model Information

Uses **Helsinki-NLP MarianMT** (`opus-mt-en-mr`) from HuggingFace:

- ✅ High-quality neural machine translation
- ✅ Fast CPU inference
- ✅ Production-ready
- ✅ Regularly updated by the community

## 🚀 Quick Start

### Local Development

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Download the model
python scripts/download_marianmt.py

# 3. Run the service
python main.py --host 0.0.0.0 --port 5000
```

The service will be available at `http://localhost:5000`

### Docker

```bash
# Build the image
docker build -t libretranslate-marathi .

# Run the container
docker run -p 5000:5000 libretranslate-marathi
```

### Docker Compose

```yaml
version: '3.8'
services:
  translator:
    build: .
    ports:
      - "5000:5000"
    environment:
      - PORT=5000
      - LT_LOAD_ONLY=en,mr
    restart: unless-stopped
```

## 📡 API Usage

### Basic Translation

```bash
# English → Marathi
curl -X POST "http://localhost:5000/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "q": "Hello, how are you?",
    "source": "en",
    "target": "mr"
  }'

# Response:
# {
#   "translatedText": "नमस्कार, तुम्ही कसे आहात?",
#   "detectedLanguage": {
#     "confidence": 100,
#     "language": "en"
#   }
# }
```

```bash
# Marathi → English
curl -X POST "http://localhost:5000/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "q": "नमस्कार जग",
    "source": "mr",
    "target": "en"
  }'

# Response:
# {
#   "translatedText": "Hello world",
#   "detectedLanguage": {
#     "confidence": 100,
#     "language": "mr"
#   }
# }
```

### Batch Translation

```bash
curl -X POST "http://localhost:5000/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "q": ["Hello", "Good morning", "Thank you"],
    "source": "en",
    "target": "mr"
  }'
```

### Get Supported Languages

```bash
curl "http://localhost:5000/languages"

# Response:
# [
#   {
#     "code": "en",
#     "name": "English",
#     "targets": ["mr"]
#   },
#   {
#     "code": "mr",
#     "name": "Marathi",
#     "targets": ["en"]
#   }
# ]
```

## 🏗️ Architecture

### What's Included

- ✅ Flask web framework
- ✅ HuggingFace Transformers
- ✅ PyTorch (CPU)
- ✅ MarianMT model
- ✅ Language detection
- ✅ API documentation (Swagger)

### What's Removed

- ❌ Argos Translate (not needed)
- ❌ File translation support
- ❌ Redis (using in-memory storage)
- ❌ Prometheus metrics
- ❌ Suggestions database
- ❌ Multiple language models
- ❌ Unnecessary locales

## ⚡ Performance

| Metric | Value |
|--------|-------|
| **Build Time** | ~5-8 minutes |
| **Startup Time** | ~20-30 seconds |
| **Translation Speed** | ~100-500 words/sec |
| **Memory Usage** | ~2-3 GB RAM |
| **Docker Image Size** | ~3-4 GB |

## 🔧 Configuration

### Environment Variables

```bash
# Port configuration
PORT=5000

# Language restriction
LT_LOAD_ONLY=en,mr

# Disable features
LT_DISABLE_FILES_TRANSLATION=true
LT_DISABLE_WEB_UI=false

# Performance
LT_THREADS=4
```

### Command Line Options

```bash
python main.py \
  --host 0.0.0.0 \
  --port 5000 \
  --load-only en,mr \
  --threads 4 \
  --disable-files-translation
```

## 🐛 Troubleshooting

### Model Not Found

```bash
# Download the model manually
python scripts/download_marianmt.py
```

### Out of Memory

```bash
# Reduce threads
python main.py --threads 2

# Or use Docker with memory limit
docker run -m 4g -p 5000:5000 libretranslate-marathi
```

### Slow Translations

- Ensure you're using CPU-optimized PyTorch
- Reduce batch size
- Increase thread count (if you have CPU cores available)

## 📝 License

AGPL v3 - Same as LibreTranslate

## 🙏 Credits

- [LibreTranslate](https://github.com/LibreTranslate/LibreTranslate) - Original project
- [Helsinki-NLP](https://huggingface.co/Helsinki-NLP) - MarianMT models
- [HuggingFace](https://huggingface.co/) - Model hosting and transformers library

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions
