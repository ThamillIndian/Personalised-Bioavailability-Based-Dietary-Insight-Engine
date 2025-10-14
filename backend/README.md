# 🍳 Smart Recipe Generator API

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> An intelligent recipe suggestion system powered by AI that recognizes ingredients from images, matches recipes, and provides personalized cooking recommendations.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Project Structure](#-project-structure)
- [Evaluation Criteria Coverage](#-evaluation-criteria-coverage)

---

## ✨ Features

### Core Features

1. **🖼️ Ingredient Recognition from Images**
   - Upload images of ingredients
   - AI-powered recognition using Google Gemini Vision
   - Returns ingredients with confidence scores
   - Handles multiple ingredients in a single image

2. **🔍 Smart Recipe Matching**
   - Advanced matching algorithm with fuzzy search
   - Ranks recipes by ingredient match percentage
   - Considers critical vs. optional ingredients
   - Suggests recipes even with partial ingredient matches

3. **🔄 Ingredient Substitutions**
   - AI-powered substitution suggestions
   - Context-aware alternatives (baking, vegan, etc.)
   - Includes substitution ratios and notes
   - Fallback database for common substitutions

4. **🍽️ Dietary Restrictions**
   - Filter by vegetarian, vegan, gluten-free, etc.
   - 13+ dietary tags supported
   - 100% compliance filtering
   - Nutritional information for all recipes

5. **⭐ User Ratings & Favorites**
   - Rate recipes 1-5 stars
   - Save favorite recipes
   - Track cooking history
   - Personalized recommendations based on preferences

6. **📊 Advanced Filtering**
   - Filter by cuisine type (Italian, Chinese, Indian, etc.)
   - Filter by cooking time and difficulty
   - Filter by nutritional values (calories, protein, carbs)
   - Pagination support

### Additional Features

- **30 Diverse Recipes**: Pre-loaded database with cuisines from around the world
- **Comprehensive API**: RESTful endpoints with OpenAPI documentation
- **Error Handling**: Robust error handling with detailed error messages
- **Logging**: Structured logging with Loguru
- **Testing**: Full pytest test suite
- **Production Ready**: Clean code, type hints, async support

---

## 🛠️ Tech Stack

### Backend Framework
- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.11+**: Latest Python with async/await support
- **Uvicorn**: ASGI server for running FastAPI

### AI & External APIs
- **Google Gemini Flash 2.5**: For image recognition and AI suggestions
- **Spoonacular API**: For additional recipe data and nutritional info (optional)

### Database & Storage
- **Supabase**: PostgreSQL database with real-time capabilities
- **Pydantic**: Data validation and settings management

### Image Processing
- **Pillow (PIL)**: Image processing and optimization
- **Async I/O**: Non-blocking image operations

### Testing & Quality
- **pytest**: Testing framework
- **pytest-asyncio**: Async test support
- **Black**: Code formatting
- **Flake8**: Code linting

### Deployment
- **Railway/Render**: Recommended deployment platforms
- **Docker**: Containerization support (optional)

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────┐
│   Frontend      │
│  (React App)    │
└────────┬────────┘
         │ HTTP/JSON
         ▼
┌─────────────────────────────────────┐
│         FastAPI Backend             │
├─────────────────────────────────────┤
│  ┌──────────────────────────────┐  │
│  │   API Layer (Routes)         │  │
│  │  - Health Check              │  │
│  │  - Ingredients               │  │
│  │  - Recipes                   │  │
│  │  - Favorites                 │  │
│  └──────────┬───────────────────┘  │
│             │                       │
│  ┌──────────▼───────────────────┐  │
│  │   Services Layer             │  │
│  │  - Gemini Service            │  │
│  │  - Spoonacular Service       │  │
│  │  - Image Processor           │  │
│  │  - Recipe Matcher ⭐         │  │
│  │  - Substitution Service      │  │
│  └──────────┬───────────────────┘  │
│             │                       │
│  ┌──────────▼───────────────────┐  │
│  │   Data Layer                 │  │
│  │  - Pydantic Models           │  │
│  │  - Database Client           │  │
│  │  - Seed Data (30 recipes)    │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
         │               │
         ▼               ▼
   ┌─────────┐    ┌──────────┐
   │ Gemini  │    │ Supabase │
   │   AI    │    │   DB     │
   └─────────┘    └──────────┘
```

### Smart Recipe Matching Algorithm

The heart of our system - a sophisticated matching algorithm that:

```python
Match Score = (
    Exact Matches × 1.0 +
    Fuzzy Matches × 0.8 -
    Critical Missing × 20.0
) × Dietary Compliance
```

**Features:**
- Fuzzy matching for ingredient variations
- Critical ingredient detection
- Dietary restriction compliance
- User preference boosting
- Minimum 40% match threshold

---

## 📦 Installation

### Prerequisites

- Python 3.11 or higher
- pip or pipenv
- Git

### Step 1: Clone Repository

```bash
git clone <your-repo-url>
cd backend
```

### Step 2: Create Virtual Environment

```bash
# Using venv
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### Step 1: Create Environment File

Copy the example environment file:

```bash
cp env.example .env
```

### Step 2: Configure API Keys

Edit `.env` file with your credentials:

```env
# Required: Google Gemini API Key
GEMINI_API_KEY="your-gemini-api-key-here"

# Optional: Spoonacular API Key (for enhanced features)
SPOONACULAR_API_KEY="your-spoonacular-api-key"

# Optional: Supabase (for database persistence)
SUPABASE_URL="your-supabase-project-url"
SUPABASE_KEY="your-supabase-anon-key"
```

### Getting API Keys

#### Google Gemini API Key (Required)
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Click "Get API Key"
4. Copy the key to `.env`

#### Spoonacular API Key (Optional)
1. Visit [Spoonacular API](https://spoonacular.com/food-api)
2. Sign up for free account
3. Get API key from dashboard
4. Free tier: 150 requests/day

#### Supabase (Optional)
1. Visit [Supabase](https://supabase.com)
2. Create new project
3. Copy project URL and anon key
4. Run database schema: `data/supabase_schema.sql`

---

## 🚀 Running the Application

### Development Mode

```bash
# Start server with auto-reload
uvicorn app.main:app --reload

# Or using Python directly
python -m app.main
```

Server will start at: `http://localhost:8000`

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Access Points

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health

---

## 📚 API Documentation

### Base URL

```
http://localhost:8000/api/v1
```

### Endpoints

#### 1. Health Check

```http
GET /api/v1/health
```

Response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00Z",
  "database_connected": true,
  "services": {
    "database": true,
    "gemini_ai": true,
    "spoonacular": true
  }
}
```

#### 2. Recognize Ingredients from Image

```http
POST /api/v1/ingredients/recognize-image
Content-Type: multipart/form-data

file: <image file>
```

Response:
```json
{
  "success": true,
  "ingredients": [
    {
      "name": "tomato",
      "confidence": 0.95,
      "quantity_estimate": "3-4 pieces",
      "category": "vegetable"
    }
  ],
  "total_found": 5,
  "processing_time_ms": 2340
}
```

#### 3. Search Recipes by Ingredients

```http
POST /api/v1/recipes/search
Content-Type: application/json

{
  "ingredients": ["chicken", "tomato", "onion"],
  "dietary_restrictions": ["gluten-free"],
  "max_cook_time": 45,
  "difficulty": "easy",
  "limit": 10
}
```

Response:
```json
{
  "success": true,
  "recipes": [
    {
      "recipe": {
        "id": "uuid",
        "title": "Chicken Tikka Masala",
        "difficulty": "medium",
        "prep_time": 30,
        "cook_time": 40,
        "ingredients": [...],
        "instructions": [...],
        "nutrition": {...}
      },
      "match_percentage": 85.5,
      "matched_ingredients": ["chicken", "tomato", "onion"],
      "missing_ingredients": ["yogurt", "cream"],
      "can_make_with_substitutions": true
    }
  ],
  "total_found": 8
}
```

#### 4. Get Ingredient Substitutions

```http
POST /api/v1/ingredients/substitutions
Content-Type: application/json

{
  "ingredient": "butter",
  "context": "baking"
}
```

Response:
```json
{
  "success": true,
  "original_ingredient": "butter",
  "substitutions": [
    {
      "substitute": "coconut oil",
      "ratio": "1:1",
      "notes": "Best for baking, adds slight coconut flavor"
    }
  ]
}
```

#### 5. Rate Recipe

```http
POST /api/v1/favorites/ratings
Content-Type: application/json

{
  "recipe_id": "recipe-123",
  "user_id": "user-456",
  "rating": 5,
  "review": "Delicious!"
}
```

### Full API Documentation

Visit `/docs` for interactive Swagger UI with all endpoints.

---

## 🧪 Testing

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=app --cov-report=html
```

### Run Specific Test File

```bash
pytest tests/test_recipes.py -v
```

### Test Structure

```
tests/
├── conftest.py           # Test fixtures
├── test_health.py        # Health check tests
├── test_recipes.py       # Recipe search & filtering tests
├── test_ingredients.py   # Image recognition tests
└── test_favorites.py     # Ratings & favorites tests
```

---

## 🚢 Deployment

### Railway (Recommended)

1. Install Railway CLI:
```bash
npm install -g @railway/cli
```

2. Login and deploy:
```bash
railway login
railway init
railway up
```

3. Set environment variables in Railway dashboard

### Render

1. Create `render.yaml`:
```yaml
services:
  - type: web
    name: recipe-api
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
```

2. Connect GitHub repo to Render
3. Set environment variables

### Docker (Optional)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry
│   ├── config.py                  # Settings & configuration
│   ├── database.py                # Supabase connection
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── health.py          # Health check endpoints
│   │       ├── recipes.py         # Recipe endpoints
│   │       ├── ingredients.py     # Ingredient endpoints
│   │       └── favorites.py       # Favorites & ratings
│   │
│   ├── services/
│   │   ├── gemini_service.py      # Gemini AI integration
│   │   ├── spoonacular_service.py # Spoonacular API
│   │   ├── image_processor.py     # Image processing
│   │   ├── recipe_matcher.py      # ⭐ Smart matching algorithm
│   │   └── substitution_service.py# Substitution logic
│   │
│   ├── models/
│   │   ├── recipe.py              # Recipe models
│   │   └── user.py                # User models
│   │
│   ├── schemas/
│   │   ├── recipe_schema.py       # Recipe request/response
│   │   ├── ingredient_schema.py   # Ingredient schemas
│   │   └── response_schema.py     # Generic responses
│   │
│   └── utils/
│       ├── error_handlers.py      # Custom exceptions
│       ├── validators.py          # Input validation
│       ├── helpers.py             # Helper functions
│       └── logger.py              # Logging setup
│
├── data/
│   ├── seed_recipes.py            # 30 diverse recipes
│   └── supabase_schema.sql        # Database schema
│
├── tests/
│   ├── conftest.py                # Pytest fixtures
│   ├── test_recipes.py            # Recipe tests
│   ├── test_ingredients.py        # Ingredient tests
│   └── test_favorites.py          # Favorites tests
│
├── requirements.txt               # Python dependencies
├── env.example                    # Environment template
├── README.md                      # This file
└── runtime.txt                    # Python version
```

---

## ✅ Evaluation Criteria Coverage

### 1. Ingredient Classification Approach ✅

**Implementation:**
- Google Gemini Vision API for state-of-the-art image recognition
- Pillow for image preprocessing and optimization
- Confidence scores for each recognized ingredient
- Fallback text-based ingredient parsing

**Files:**
- `app/services/gemini_service.py`
- `app/services/image_processor.py`

---

### 2. Recipe Matching Logic ✅

**Implementation:**
- Advanced scoring algorithm with fuzzy matching
- Critical ingredient detection
- Match percentage calculation (0-100%)
- Dietary restriction filtering
- User preference boosting

**Algorithm Details:**
```python
# Fuzzy matching threshold: 70%
# Minimum match: 40%
# Exact match weight: 1.0
# Fuzzy match weight: 0.8
# Critical penalty: -20 points
```

**Files:**
- `app/services/recipe_matcher.py` (★ Core Algorithm)
- `app/utils/helpers.py`

---

### 3. Error Handling ✅

**Implementation:**
- Custom exception classes
- HTTP-friendly error responses
- Detailed error messages with context
- Graceful degradation
- Logging for debugging

**Error Types:**
- `ImageProcessingError`: Invalid images
- `IngredientRecognitionError`: AI failures
- `RecipeNotFoundError`: Missing recipes
- `ValidationError`: Invalid input
- `ExternalAPIError`: Third-party failures

**Files:**
- `app/utils/error_handlers.py`

---

### 4. User Experience Considerations ✅

**Implementation:**
- Fast response times (async/await)
- Loading states support
- Detailed API responses
- Pagination for large datasets
- Clear error messages
- Comprehensive documentation

**UX Features:**
- Match percentage shows how well user can make recipe
- Substitution suggestions for missing ingredients
- "Can make with substitutions" flag
- Nutritional info for informed decisions
- Multiple cuisine options

---

### 5. Production Quality Code ✅

**Implementation:**
- Type hints throughout
- Pydantic for validation
- Clean architecture (layers)
- DRY principles
- Comprehensive docstrings
- Consistent naming conventions

**Code Quality Tools:**
- Black (formatting)
- Flake8 (linting)
- pytest (testing)
- Loguru (logging)

---

## 🎯 Minimum Requirements Met

- ✅ **20+ Recipes**: 30 diverse recipes with complete data
- ✅ **Ingredient Recognition**: Gemini Vision + image processing
- ✅ **Recipe Matching**: Advanced algorithm with fuzzy search
- ✅ **Substitutions**: AI-powered + fallback database
- ✅ **Dietary Restrictions**: 13+ tags, perfect filtering
- ✅ **Error Handling**: Comprehensive exception handling
- ✅ **Loading States**: Async support, processing time tracking
- ✅ **Documentation**: This README + inline docs + OpenAPI

---

## 📝 License

MIT License - feel free to use this project!

---

## 👨‍💻 Author

Created with ❤️ for the Smart Recipe Generator assignment

---

## 🆘 Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# Make sure you're in the backend directory
cd backend
# Reinstall dependencies
pip install -r requirements.txt
```

**2. Gemini API Not Working**
- Check API key in `.env`
- Verify key is active on Google AI Studio
- Check rate limits (1500 requests/day)

**3. No Recipes Found**
- Seed data is loaded in-memory from `data/seed_recipes.py`
- Ensure file is not corrupted
- Check logs for errors

**4. Image Upload Fails**
- Max size: 10MB
- Supported formats: JPEG, PNG, WebP
- Check file MIME type

---

## 🚀 Future Enhancements

- [ ] Meal planning features
- [ ] Shopping list generation
- [ ] Recipe scaling (adjust servings)
- [ ] More cuisine types
- [ ] Recipe difficulty AI estimation
- [ ] Cooking time predictions
- [ ] Video tutorials integration
- [ ] Social sharing features

---

**Ready to cook? 🍳 Start the server and visit `/docs` to explore the API!**

