# Deploy to Hugging Face Spaces (FREE)

Hugging Face Spaces offers **FREE hosting** with 16GB RAM - perfect for this translation API!

## Setup Steps

### 1. Create Hugging Face Account
- Go to https://huggingface.co
- Sign up (free)

### 2. Create a New Space
- Click "New Space"
- Name: `marathi-translation-api`
- License: Choose any
- SDK: **Docker**
- Click "Create Space"

### 3. Push Your Code

```bash
# Add HF remote
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/marathi-translation-api

# Push
git push hf main
```

### 4. Wait for Build
- HF will build your Docker image
- Takes 5-10 minutes
- Watch the build logs

### 5. Your API is Live!
- URL: `https://YOUR_USERNAME-marathi-translation-api.hf.space`

## Test Your API

```bash
curl -X POST https://YOUR_USERNAME-marathi-translation-api.hf.space/translate \
  -H "Content-Type: application/json" \
  -d '{"q":"Hello","source":"en","target":"mr"}'
```

## Advantages

✅ **FREE** - No credit card required
✅ **16GB RAM** - More than enough
✅ **Always on** - No sleep mode
✅ **Fast** - Good performance
✅ **Easy** - Just push to git

## Alternative: Railway.app

If you prefer Railway:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Create project
railway init

# Deploy
railway up
```

Railway gives $5 free credit monthly which is enough for light usage.

## Comparison

| Platform | Free RAM | Free Tier | Best For |
|----------|----------|-----------|----------|
| **Hugging Face** | 16GB | Unlimited | ML models (Best!) |
| **Railway** | 8GB | $5 credit/month | General apps |
| **Render** | 512MB | Limited | Not enough for this |
| **Fly.io** | 256MB | 3 VMs | Not enough for this |

## Recommendation

**Use Hugging Face Spaces** - it's designed for ML models and offers the best free tier for your use case!
