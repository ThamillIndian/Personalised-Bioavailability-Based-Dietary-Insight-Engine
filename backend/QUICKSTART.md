# ⚡ Quick Start Guide

Get the Smart Recipe Generator API running in 5 minutes!

---

## Prerequisites

- Python 3.11+
- Git
- Text editor

---

## Step 1: Clone & Navigate (30 seconds)

```bash
cd backend
```

---

## Step 2: Install Dependencies (2 minutes)

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

---

## Step 3: Configure API Keys (1 minute)

1. Copy environment template:
```bash
cp env.example .env
```

2. Edit `.env` and add your Gemini API key:
```env
GEMINI_API_KEY="your-actual-key-here"
```

**Get Gemini key:** https://makersuite.google.com/app/apikey (free, instant)

---

## Step 4: Run the Server (30 seconds)

```bash
uvicorn app.main:app --reload
```

✅ Server running at: **http://localhost:8000**

---

## Step 5: Test It! (1 minute)

### Option A: Browser

Visit: http://localhost:8000/docs

Click "Try it out" on any endpoint!

### Option B: cURL

```bash
# Health check
curl http://localhost:8000/api/v1/health

# List recipes
curl http://localhost:8000/api/v1/recipes/
```

### Option C: Python

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/recipes/search",
    json={"ingredients": ["chicken", "tomato"], "limit": 5}
)

print(response.json())
```

---

## Common Issues

### ❌ "Module not found"
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### ❌ "GEMINI_API_KEY not configured"
- Check `.env` file exists
- Verify key is correct
- No extra spaces or quotes

### ❌ "Address already in use"
```bash
# Use different port
uvicorn app.main:app --port 8001
```

---

## Next Steps

✅ API running? Great! Now:

1. **Read the docs**: http://localhost:8000/docs
2. **Test endpoints**: Try image upload, recipe search
3. **Deploy**: See `DEPLOYMENT.md`
4. **Build frontend**: Connect your React app

---

## Project Structure

```
backend/
├── app/              # Main application
│   ├── api/         # API endpoints
│   ├── services/    # Business logic
│   ├── models/      # Data models
│   └── utils/       # Utilities
├── data/            # Seed recipes & schema
├── tests/           # Test suite
└── .env             # Your config (not in Git!)
```

---

## Key Files

- `app/main.py` - FastAPI app entry point
- `app/services/recipe_matcher.py` - Smart matching algorithm ⭐
- `data/seed_recipes.py` - 30 diverse recipes
- `requirements.txt` - Dependencies

---

## Running Tests

```bash
pytest
```

---

## Documentation

- **README.md** - Full documentation
- **API_DOCUMENTATION.md** - API reference
- **DEPLOYMENT.md** - Deployment guide

---

## Features You Can Test

1. **Recipe Search** (POST /recipes/search)
   ```json
   {
     "ingredients": ["chicken", "tomato", "onion"],
     "dietary_restrictions": ["gluten-free"],
     "limit": 10
   }
   ```

2. **Image Recognition** (POST /ingredients/recognize-image)
   - Upload any food image
   - Get AI-recognized ingredients

3. **Substitutions** (POST /ingredients/substitutions)
   ```json
   {
     "ingredient": "butter",
     "context": "baking"
   }
   ```

4. **Nutrition Filtering** (GET /recipes/filter/by-nutrition)
   ```
   ?max_calories=500&min_protein=20
   ```

---

## Production Deployment

**Quick deploy to Railway:**

```bash
# Install CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up
```

**Set environment variable:**
```bash
railway variables set GEMINI_API_KEY=your_key
```

Done! API live in 2 minutes. 🚀

---

## Support

- Issues? Check logs: Look for errors in terminal
- Questions? Read `README.md`
- Bugs? File GitHub issue

---

**You're all set! Happy cooking! 🍳**

