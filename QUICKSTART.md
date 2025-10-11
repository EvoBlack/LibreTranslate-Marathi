# Quick Start Guide - LibreTranslate Marathi

Get up and running with English ↔ Marathi translation in minutes!

## 🚀 Option 1: Local Development (Fastest)

### Prerequisites
- Python 3.8 or higher
- pip

### Steps

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd libretranslate-marathi

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download the MarianMT model (~300MB)
python scripts/download_marianmt.py

# 4. Start the service
python main.py

# 5. Test it!
# Open http://localhost:5000 in your browser
# Or use the API:
curl -X POST "http://localhost:5000/translate" \
  -H "Content-Type: application/json" \
  -d '{"q": "Hello world", "source": "en", "target": "mr"}'
```

**Expected output:**
```json
{
  "translatedText": "नमस्कार जग",
  "detectedLanguage": {
    "confidence": 100,
    "language": "en"
  }
}
```

---

## 🐳 Option 2: Docker (Recommended for Production)

### Prerequisites
- Docker installed

### Steps

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd libretranslate-marathi

# 2. Build the Docker image
docker build -t libretranslate-marathi .

# 3. Run the container
docker run -p 5000:5000 libretranslate-marathi

# 4. Test it!
curl -X POST "http://localhost:5000/translate" \
  -H "Content-Type: application/json" \
  -d '{"q": "Thank you", "source": "en", "target": "mr"}'
```

---

## ☁️ Option 3: Deploy to Render (Free Tier Available)

### Prerequisites
- GitHub account
- Render account (free)

### Steps

1. **Fork this repository** to your GitHub account

2. **Go to Render Dashboard**
   - Visit https://render.com
   - Click "New +" → "Web Service"

3. **Connect your repository**
   - Select your forked repository
   - Render will auto-detect the `render.yaml` configuration

4. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for build and deployment
   - Your service will be live at `https://your-service.onrender.com`

5. **Test your deployed service**
   ```bash
   curl -X POST "https://your-service.onrender.com/translate" \
     -H "Content-Type: application/json" \
     -d '{"q": "Good morning", "source": "en", "target": "mr"}'
   ```

---

## 🧪 Testing Your Installation

### Run the test script

```bash
python test_translation.py
```

This will test:
- ✅ English → Marathi translation
- ✅ Marathi → English translation
- ✅ Long text translation
- ✅ Batch translation
- ✅ Language list API

### Manual API Tests

```bash
# Test 1: Simple translation
curl -X POST "http://localhost:5000/translate" \
  -H "Content-Type: application/json" \
  -d '{"q": "Hello", "source": "en", "target": "mr"}'

# Test 2: Reverse translation
curl -X POST "http://localhost:5000/translate" \
  -H "Content-Type: application/json" \
  -d '{"q": "नमस्कार", "source": "mr", "target": "en"}'

# Test 3: Get supported languages
curl "http://localhost:5000/languages"

# Test 4: Health check
curl "http://localhost:5000/health"
```

---

## 📊 Performance Tips

### For Better Performance

1. **Increase threads** (if you have multiple CPU cores):
   ```bash
   python main.py --threads 8
   ```

2. **Use Docker with resource limits**:
   ```bash
   docker run -m 4g --cpus 4 -p 5000:5000 libretranslate-marathi
   ```

3. **Enable caching** (for repeated translations):
   - The service automatically caches recent translations in memory

---

## 🐛 Troubleshooting

### Problem: "Model not found"
**Solution:**
```bash
python scripts/download_marianmt.py
```

### Problem: "Out of memory"
**Solution:**
- Reduce threads: `python main.py --threads 2`
- Close other applications
- Use a machine with at least 4GB RAM

### Problem: "Port 5000 already in use"
**Solution:**
```bash
# Use a different port
python main.py --port 8080

# Or find and kill the process using port 5000
# On Linux/Mac:
lsof -ti:5000 | xargs kill -9
# On Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Problem: "Slow translations"
**Solution:**
- First translation is always slower (model loading)
- Subsequent translations are much faster
- Consider using batch translation for multiple texts

---

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out the [API documentation](http://localhost:5000/docs) (when service is running)
- Explore configuration options in `libretranslate/default_values.py`

---

## 💡 Quick Examples

### Python Client

```python
import requests

def translate(text, source="en", target="mr"):
    response = requests.post(
        "http://localhost:5000/translate",
        json={"q": text, "source": source, "target": target}
    )
    return response.json()["translatedText"]

# Use it
print(translate("Hello world"))  # नमस्कार जग
print(translate("नमस्कार", "mr", "en"))  # Hello
```

### JavaScript Client

```javascript
async function translate(text, source = "en", target = "mr") {
  const response = await fetch("http://localhost:5000/translate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ q: text, source, target })
  });
  const data = await response.json();
  return data.translatedText;
}

// Use it
translate("Hello world").then(console.log);  // नमस्कार जग
```

---

## 🎉 You're All Set!

Your Marathi translation service is now running. Happy translating! 🌐
