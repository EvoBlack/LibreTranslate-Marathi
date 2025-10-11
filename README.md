# Marathi Translation API

A lightweight, production-ready translation API for English ↔ Marathi using MarianMT models.

## Features

- ✅ Simple REST API
- ✅ English ↔ Marathi translation
- ✅ Batch translation support
- ✅ CORS enabled
- ✅ Health check endpoint
- ✅ Docker ready
- ✅ Production optimized

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements-simple.txt

# Download model
python scripts/download_marianmt.py

# Run server
python app.py
```

Server will start at `http://localhost:5000`

### Docker

```bash
# Build
docker build -f Dockerfile-simple -t marathi-api .

# Run
docker run -p 5000:5000 marathi-api
```

### Deploy to Render

1. Push code to GitHub
2. Connect repository to Render
3. Use `render-simple.yaml` configuration
4. Deploy!

## API Endpoints

### 1. Health Check

```bash
GET /health
```

Response:
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### 2. Get Languages

```bash
GET /languages
```

Response:
```json
[
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
]
```

### 3. Translate

```bash
POST /translate
Content-Type: application/json

{
  "q": "Hello world",
  "source": "en",
  "target": "mr"
}
```

Response:
```json
{
  "translatedText": "नमस्कार जग",
  "detectedLanguage": {
    "confidence": 100,
    "language": "en"
  }
}
```

### Batch Translation

```bash
POST /translate
Content-Type: application/json

{
  "q": ["Hello", "Thank you", "Good morning"],
  "source": "en",
  "target": "mr"
}
```

Response:
```json
{
  "translatedText": ["नमस्कार", "धन्यवाद", "सुप्रभात"],
  "detectedLanguage": {
    "confidence": 100,
    "language": "en"
  }
}
```

## Usage Examples

### cURL

```bash
curl -X POST http://localhost:5000/translate \
  -H "Content-Type: application/json" \
  -d '{"q":"Hello","source":"en","target":"mr"}'
```

### Python

```python
import requests

response = requests.post(
    "http://localhost:5000/translate",
    json={
        "q": "Hello world",
        "source": "en",
        "target": "mr"
    }
)

print(response.json()["translatedText"])
```

### JavaScript

```javascript
fetch('http://localhost:5000/translate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    q: 'Hello world',
    source: 'en',
    target: 'mr'
  })
})
.then(res => res.json())
.then(data => console.log(data.translatedText));
```

### PHP

```php
$data = [
    'q' => 'Hello world',
    'source' => 'en',
    'target' => 'mr'
];

$ch = curl_init('http://localhost:5000/translate');
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type:application/json']);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$result = curl_exec($ch);
curl_close($ch);

$response = json_decode($result, true);
echo $response['translatedText'];
```

## Testing

```bash
# Test locally
python test_api.py

# Test deployed service
python test_api.py --url https://your-service.onrender.com
```

## Performance

- **First request**: 2-3 seconds (model warmup)
- **Subsequent requests**: <500ms
- **Batch translation**: ~100ms per text
- **Memory usage**: ~2GB RAM

## Error Handling

All errors return JSON:

```json
{
  "error": "Error message"
}
```

Status codes:
- `200`: Success
- `400`: Bad request (missing parameters)
- `500`: Server error
- `503`: Service unavailable (model not loaded)

## Environment Variables

- `PORT`: Server port (default: 5000)
- `HOST`: Server host (default: 0.0.0.0)

## License

AGPL v3
