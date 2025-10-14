# 🚀 Deployment Guide

Complete guide for deploying Smart Recipe Generator API to production.

---

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Railway Deployment](#railway-deployment)
3. [Render Deployment](#render-deployment)
4. [Vercel (Serverless)](#vercel-serverless)
5. [Docker Deployment](#docker-deployment)
6. [Environment Variables](#environment-variables)
7. [Database Setup](#database-setup)
8. [Post-Deployment](#post-deployment)

---

## Pre-Deployment Checklist

Before deploying, ensure you have:

- [x] Python 3.11+ compatible code
- [x] `requirements.txt` with all dependencies
- [x] `runtime.txt` specifying Python version
- [x] Environment variables documented
- [x] Database schema ready (if using Supabase)
- [x] API keys for Gemini and Spoonacular
- [x] Tests passing locally

---

## Railway Deployment

Railway is the recommended platform for easy deployment.

### Step 1: Install Railway CLI

```bash
npm install -g @railway/cli
```

### Step 2: Login to Railway

```bash
railway login
```

### Step 3: Initialize Project

```bash
cd backend
railway init
```

Select "Create new project" and choose a name.

### Step 4: Deploy

```bash
railway up
```

### Step 5: Set Environment Variables

In Railway Dashboard:
1. Go to your project
2. Click "Variables"
3. Add all environment variables from `.env`:

```
GEMINI_API_KEY=your_key_here
SPOONACULAR_API_KEY=your_key_here
SUPABASE_URL=your_url_here
SUPABASE_KEY=your_key_here
ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### Step 6: Configure Start Command

In Railway settings, set start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Step 7: Get Domain

Railway automatically provides a domain:
- `https://your-app.railway.app`
- Or add custom domain in settings

---

## Render Deployment

### Step 1: Create `render.yaml`

Already created in project root. Verify it exists:

```yaml
services:
  - type: web
    name: smart-recipe-api
    env: python
    region: oregon
    plan: free
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.7
```

### Step 2: Connect GitHub

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Render auto-detects `render.yaml`

### Step 3: Set Environment Variables

In Render dashboard, add:
- `GEMINI_API_KEY`
- `SPOONACULAR_API_KEY`
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `ALLOWED_ORIGINS`

### Step 4: Deploy

Click "Create Web Service" - deployment starts automatically!

---

## Vercel (Serverless)

For serverless deployment (experimental).

### Step 1: Create `vercel.json`

```json
{
  "builds": [
    {
      "src": "app/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app/main.py"
    }
  ]
}
```

### Step 2: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 3: Deploy

```bash
vercel
```

**Note**: Vercel has limitations for long-running processes. Railway or Render recommended.

---

## Docker Deployment

### Step 1: Create Dockerfile

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Step 2: Create `.dockerignore`

```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
.git
.gitignore
README.md
tests/
.pytest_cache/
```

### Step 3: Build Image

```bash
docker build -t recipe-api .
```

### Step 4: Run Container

```bash
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  -e SPOONACULAR_API_KEY=your_key \
  recipe-api
```

### Step 5: Deploy to Cloud

**AWS ECS:**
```bash
# Push to ECR
docker tag recipe-api:latest aws_account_id.dkr.ecr.region.amazonaws.com/recipe-api:latest
docker push aws_account_id.dkr.ecr.region.amazonaws.com/recipe-api:latest
```

**Google Cloud Run:**
```bash
gcloud run deploy recipe-api --image recipe-api --platform managed
```

---

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | `AIza...` |
| `ALLOWED_ORIGINS` | CORS allowed origins | `https://myapp.com` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SPOONACULAR_API_KEY` | Spoonacular API key | None |
| `SUPABASE_URL` | Supabase project URL | None |
| `SUPABASE_KEY` | Supabase anon key | None |
| `PORT` | Server port | 8000 |
| `LOG_LEVEL` | Logging level | INFO |
| `DEBUG` | Debug mode | False |

### Setting Variables

**Railway:**
```bash
railway variables set GEMINI_API_KEY=your_key
```

**Render:**
- Dashboard → Environment → Add Variable

**Vercel:**
```bash
vercel env add GEMINI_API_KEY
```

**Docker:**
```bash
docker run -e GEMINI_API_KEY=your_key ...
```

---

## Database Setup

### Using Supabase (Recommended)

1. **Create Project**
   - Go to [Supabase](https://supabase.com)
   - Click "New Project"
   - Set name and password

2. **Run Schema**
   - Go to SQL Editor
   - Copy contents of `data/supabase_schema.sql`
   - Execute

3. **Get Credentials**
   - Go to Settings → API
   - Copy Project URL and anon key
   - Add to environment variables

4. **Optional: Seed Data**
   - Create Python script to insert recipes from `data/seed_recipes.py`
   - Or use app's in-memory data (current setup)

### Without Database

The app works without a database by using in-memory storage:
- Recipes: Loaded from `data/seed_recipes.py`
- Favorites/Ratings: Stored in-memory (resets on restart)

For production, Supabase is recommended.

---

## Post-Deployment

### 1. Verify Health

```bash
curl https://your-app.railway.app/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "services": {
    "gemini_ai": true,
    "spoonacular": true
  }
}
```

### 2. Test Endpoints

Visit: `https://your-app.railway.app/docs`

Test each endpoint in Swagger UI.

### 3. Monitor Logs

**Railway:**
```bash
railway logs
```

**Render:**
- Dashboard → Logs tab

**Docker:**
```bash
docker logs container_id
```

### 4. Set Up Monitoring

**Recommended Tools:**
- [Better Stack](https://betterstack.com/) - Logging
- [Sentry](https://sentry.io/) - Error tracking
- [Uptime Robot](https://uptimerobot.com/) - Uptime monitoring

### 5. Configure CORS

Update `ALLOWED_ORIGINS` to include your frontend domain:

```bash
ALLOWED_ORIGINS=https://myapp.com,https://www.myapp.com
```

### 6. Add Custom Domain (Optional)

**Railway:**
1. Settings → Domains
2. Add custom domain
3. Update DNS records

**Render:**
1. Settings → Custom Domain
2. Follow DNS setup instructions

---

## Performance Optimization

### 1. Enable Caching

Add Redis for caching:

```python
# Future enhancement
from redis import Redis
cache = Redis(host='localhost', port=6379)
```

### 2. Rate Limiting

Already implemented with `slowapi`.

Configure in `.env`:
```
RATE_LIMIT_PER_MINUTE=60
```

### 3. CDN for Images

Use Cloudinary or AWS S3 for recipe images.

### 4. Database Indexing

Ensure all indexes from `supabase_schema.sql` are created.

---

## Troubleshooting

### Issue: 502 Bad Gateway

**Solution:**
- Check logs for startup errors
- Verify all environment variables are set
- Ensure port binding is correct (`$PORT`)

### Issue: CORS Errors

**Solution:**
- Add frontend domain to `ALLOWED_ORIGINS`
- Ensure CORS middleware is enabled

### Issue: API Key Not Working

**Solution:**
- Verify key is active in provider dashboard
- Check for extra whitespace in environment variable
- Test key locally first

### Issue: Slow Response Times

**Solution:**
- Enable caching
- Optimize database queries
- Use faster API regions
- Upgrade to paid tier

---

## Security Best Practices

1. **Never commit `.env` file**
2. **Use HTTPS only** (Railway/Render provide this)
3. **Rotate API keys regularly**
4. **Enable rate limiting**
5. **Validate all inputs** (already implemented)
6. **Monitor for unusual activity**
7. **Keep dependencies updated**

---

## Maintenance

### Update Dependencies

```bash
pip install --upgrade -r requirements.txt
```

### Database Migrations

When schema changes:
1. Update `supabase_schema.sql`
2. Run migration in Supabase SQL Editor
3. Update models in `app/models/`

### Monitoring

Set up alerts for:
- API downtime
- Error rate > 1%
- Response time > 3s
- High memory usage

---

## Support

For issues:
1. Check logs first
2. Review this guide
3. Check platform-specific docs
4. Open GitHub issue

---

**Your API is ready to serve millions of recipe requests! 🚀**

