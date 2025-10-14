# 🍳 Smart Recipe Generator - Full Stack Application

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-15.2.4-black.svg)](https://nextjs.org)
[![React](https://img.shields.io/badge/React-19-blue.svg)](https://react.dev)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> An intelligent, full-stack recipe discovery platform powered by AI that recognizes ingredients from images, matches recipes, provides personalized recommendations, and offers interactive cooking tools.

---

## 🌊 Overview

**Smart Recipe Generator** be a complete recipe discovery application that combines AI-powered ingredient recognition, smart recipe matching, and an intuitive user interface to help ye find the perfect recipes based on what ye have in yer galley!

### Key Features at a Glance
- 🖼️ **AI Image Recognition** - Upload photos of ingredients and let AI identify them
- 🔍 **Smart Recipe Matching** - Advanced algorithm with fuzzy search and scoring
- 🤖 **AI Chatbot Assistant** - Context-aware cooking help across all pages
- 📱 **Mobile-First Design** - Optimized for all devices with touch gestures
- ⏱️ **Cooking Tools** - Built-in timers and shopping lists
- 🎨 **Beautiful UI** - Dark/light themes with smooth animations
- 📊 **Smart Recommendations** - Learn from yer preferences
- 🥗 **Dietary Filters** - 13+ dietary restrictions supported
- ⭐ **Favorites & Ratings** - Save and rate yer favorite recipes

---

## 📋 Table of Contents

- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Deployment](#-deployment)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

---

## 🏗️ Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────┐
│                  FRONTEND (Next.js)                     │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Pages: Home, Search, Recipe Detail, Collection  │  │
│  │  Components: Chat, Timer, Shopping, Filters      │  │
│  │  State: Local Storage, SWR, React Context        │  │
│  └──────────────┬───────────────────────────────────┘  │
└─────────────────┼───────────────────────────────────────┘
                  │ REST API (JSON)
                  │ HTTP/HTTPS
                  ▼
┌─────────────────────────────────────────────────────────┐
│              BACKEND (FastAPI)                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  API Layer: Health, Recipes, Ingredients, Chat  │  │
│  │  Services: Gemini AI, Recipe Matcher, LangChain │  │
│  │  Models: Recipe, User, Ratings                   │  │
│  └──────────┬──────────────┬────────────────────────┘  │
└─────────────┼──────────────┼───────────────────────────┘
              │              │
              ▼              ▼
    ┌──────────────┐  ┌──────────────┐
    │  Gemini AI   │  │   Supabase   │
    │  Vision API  │  │  PostgreSQL  │
    │  LangChain   │  │   Database   │
    └──────────────┘  └──────────────┘
```

### Frontend Architecture (Next.js)
- **App Router** - Modern Next.js 15 with server components
- **Components** - Reusable UI components with shadcn/ui
- **State Management** - React hooks, SWR for data fetching
- **Styling** - Tailwind CSS with custom theme
- **Optimization** - Image lazy loading, API caching, debounced search

### Backend Architecture (FastAPI)
- **3-Layer Architecture** - API → Services → Data
- **Async/Await** - Non-blocking operations throughout
- **Type Safety** - Pydantic models with validation
- **AI Integration** - Gemini Vision, LangChain for chat
- **Error Handling** - Comprehensive exception hierarchy

---

## 🛠️ Tech Stack

### Frontend Technologies
| Category | Technology | Purpose |
|----------|-----------|---------|
| Framework | **Next.js 15.2.4** | React framework with SSR |
| UI Library | **React 19** | Component-based UI |
| Language | **TypeScript 5** | Type-safe JavaScript |
| Styling | **Tailwind CSS 4** | Utility-first CSS |
| Components | **shadcn/ui + Radix UI** | Accessible components |
| Icons | **Lucide React** | Beautiful icons |
| Forms | **React Hook Form + Zod** | Form validation |
| State | **SWR** | Data fetching & caching |
| Theme | **next-themes** | Dark/light mode |

### Backend Technologies
| Category | Technology | Purpose |
|----------|-----------|---------|
| Framework | **FastAPI 0.109** | Modern Python web framework |
| Language | **Python 3.11+** | Backend language |
| AI/ML | **Google Gemini Flash 2.5** | Image recognition & chat |
| AI Framework | **LangChain** | Conversational AI |
| Database | **Supabase (PostgreSQL)** | Data persistence |
| Validation | **Pydantic v2** | Data validation |
| Image Processing | **Pillow 10.2** | Image manipulation |
| Testing | **pytest** | Test framework |
| Logging | **Loguru** | Structured logging |

### External APIs
- **Google Gemini API** - AI-powered ingredient recognition and chat
- **Spoonacular API** (Optional) - Enhanced recipe data

---

## 🎯 Prerequisites

### Required Software
- **Node.js** 18+ and npm/pnpm
- **Python** 3.11 or higher
- **Git** for version control

### API Keys (Required)
- **Google Gemini API Key** - Get from [Google AI Studio](https://makersuite.google.com/app/apikey)

### API Keys (Optional)
- **Spoonacular API Key** - Get from [Spoonacular](https://spoonacular.com/food-api)
- **Supabase Credentials** - Get from [Supabase](https://supabase.com)

---

## 📦 Installation

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd project
```

### Step 2: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install
# or
pnpm install
```

---

## ⚙️ Configuration

### Backend Configuration

1. **Create `.env` file** in `backend/` directory:

```bash
cd backend
cp env.example .env
```

2. **Edit `.env` with yer credentials**:

```env
# Required: Google Gemini API Key
GEMINI_API_KEY="your-gemini-api-key-here"

# Optional: Spoonacular API Key (for enhanced features)
SPOONACULAR_API_KEY="your-spoonacular-api-key"

# Optional: Supabase (for database persistence)
SUPABASE_URL="your-supabase-project-url"
SUPABASE_KEY="your-supabase-anon-key"

# Optional: Configuration flags
PARAPHRASE_ENABLED=true
GEMINI_REQUEST_DELAY=1.2

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

### Frontend Configuration

1. **Create `.env.local` file** in `frontend/` directory:

```bash
cd frontend
touch .env.local
```

2. **Add backend URL**:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Optional: Analytics
NEXT_PUBLIC_ANALYTICS_ID=your-analytics-id
```

---

## 🚀 Running the Application

### Start Backend Server

```bash
# From backend directory
cd backend

# Activate virtual environment if not already active
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Start server
uvicorn app.main:app --reload

# Server will start at http://localhost:8000
```

### Start Frontend Development Server

```bash
# From frontend directory (in a new terminal)
cd frontend

# Start development server
npm run dev
# or
pnpm dev

# Frontend will start at http://localhost:3000
```

### Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

---

## ✨ Features

### 1. 🖼️ AI-Powered Ingredient Recognition

Upload a photo of yer ingredients and let Gemini AI identify them with confidence scores!

**How it works:**
- Upload image via drag-and-drop or file picker
- AI processes image and identifies ingredients
- Returns ingredients with confidence scores and categories
- Automatically populates search with detected ingredients

**Backend:** `app/services/gemini_service.py`, `app/services/image_processor.py`  
**Frontend:** Image upload component in search page

---

### 2. 🔍 Smart Recipe Matching

Advanced fuzzy-matching algorithm that finds the best recipes based on yer ingredients!

**Algorithm Features:**
- Fuzzy string matching (70% similarity threshold)
- Exact match weight: 1.0, Fuzzy match weight: 0.8
- Critical ingredient detection (-20 penalty if missing)
- Dietary compliance filtering
- Match percentage calculation (0-100%)
- Minimum 40% match threshold

**Formula:**
```
Score = (Exact Matches × 1.0 + Fuzzy Matches × 0.8 - Critical Missing × 20.0) 
        × Dietary Compliance + User Preference Boost
```

**Backend:** `app/services/recipe_matcher.py` ⭐  
**Frontend:** Search results with match percentages

---

### 3. 🤖 AI Chatbot Assistant

Context-aware floating chatbot that provides cooking help across all pages!

**Features:**
- Context-aware suggestions based on current page
- Conversation history persistence
- LangChain-powered responses
- Quick question buttons
- Mobile-optimized bottom sheet
- Typing indicators and smooth animations

**Context Types:**
- Home: General cooking tips
- Search: Search optimization help
- Recipe Detail: Recipe-specific questions
- Collection: Organization tips

**Backend:** `app/api/v1/chat.py`, `app/services/langchain_service.py`  
**Frontend:** `components/chat/` directory

---

### 4. ⏱️ Cooking Tools

Built-in utilities to help ye cook like a pro!

#### **Multiple Timers**
- Create unlimited named timers
- Individual play/pause/reset controls
- Audio notifications on completion
- Visual progress bars
- Completion tracking

#### **Smart Shopping Lists**
- Auto-import ingredients from recipes
- Manual item addition with categories
- 7 categories: Produce, Meat, Dairy, Pantry, Frozen, Bakery, Other
- Checkbox completion tracking
- Export to text file
- Share/copy to clipboard
- Progress tracking

**Frontend:** `components/recipe/cooking-timer.tsx`, `components/recipe/shopping-list.tsx`

---

### 5. 🎨 Beautiful UI/UX

Modern, responsive design with attention to detail!

**Theme System:**
- Light mode (default)
- Dark mode
- System preference detection
- Smooth transitions

**Mobile Optimization:**
- Bottom navigation bar
- Touch-optimized controls
- Swipe gestures ready
- Responsive layouts
- Safe area insets

**Loading States:**
- Skeleton loaders
- Loading spinners (3 sizes)
- Progress indicators
- Smooth animations

**Frontend:** `components/theme-toggle.tsx`, `components/bottom-nav.tsx`, `components/ui/`

---

### 6. 🔍 Advanced Search & Filters

Comprehensive filtering system with 7+ filter types!

**Filter Categories:**

**Basic Filters:**
- Cuisine Type (12 options): Italian, Indian, Mexican, Chinese, Japanese, Thai, French, Greek, Middle Eastern, Hawaiian, Mediterranean, American
- Difficulty Level: Easy, Medium, Hard
- Max Cooking Time: Minutes slider

**Nutritional Filters:**
- Max Calories: 0-2000 kcal
- Min Protein: 0-100g
- Max Carbs: 0-200g

**Dietary Restrictions:**
13+ tags including: Vegetarian, Vegan, Gluten-Free, Dairy-Free, Nut-Free, Paleo, Keto, Low-Carb, Low-Fat, High-Protein, Sugar-Free, Soy-Free, Egg-Free

**Features:**
- Real-time search with debouncing
- Multiple filter combinations
- Filter persistence
- Clear all filters option

**Backend:** `app/api/v1/recipes.py`  
**Frontend:** `components/filter-bar.tsx`, `app/search/page.tsx`

---

### 7. 📊 Smart Recommendations

AI-powered recommendation engine that learns from yer preferences!

**How it Works:**
- Tracks recipe views (last 50)
- Monitors search history (last 20)
- Learns dietary preferences
- Detects cuisine preferences
- Calculates smart scores

**Scoring Factors:**
- Dietary match: +10 per tag
- Cuisine match: +15 points
- Search ingredient match: +5 per ingredient
- High ratings: +2 per star
- Recently viewed: -5 (encourages variety)

**Features:**
- Similar recipe suggestions
- "For You" personalized feed
- Trending recipes
- New recipe notifications

**Frontend:** `lib/recommendations.ts`, `components/recommended-recipes.tsx`

---

### 8. 🥗 Ingredient Substitutions

AI-powered substitution suggestions for missing ingredients!

**Features:**
- Context-aware suggestions (baking, cooking, vegan, etc.)
- Substitution ratios (1:1, 1:2, etc.)
- Detailed notes and warnings
- Fallback database for common substitutions
- Gemini AI for creative alternatives

**Backend:** `app/services/substitution_service.py`

---

### 9. ⭐ Favorites & Ratings

Save and rate yer favorite recipes!

**Features:**
- 5-star rating system
- Save to favorites collection
- View all saved recipes
- Rating history
- User reviews (text)

**Backend:** `app/api/v1/favorites.py`  
**Frontend:** `lib/use-saved-recipes.ts`, `app/collection/page.tsx`

---

### 10. 📊 Analytics & Insights

Track yer cooking journey with comprehensive analytics!

**Tracked Events:**
- Recipe views with duration
- Search queries with results
- Filter usage patterns
- Timer actions (create, complete)
- Shopping list actions
- Chatbot interactions
- Recipe saves and ratings

**Privacy:**
- All data stored locally
- No external tracking
- User can clear data anytime
- Session-based (30-minute timeout)

**Frontend:** `lib/analytics.ts`

---

## 📁 Project Structure

```
project/
├── backend/                          # Python FastAPI Backend
│   ├── app/
│   │   ├── main.py                   # Application entry point
│   │   ├── config.py                 # Configuration & settings
│   │   ├── database.py               # Supabase connection
│   │   ├── api/v1/                   # API endpoints
│   │   │   ├── health.py             # Health check
│   │   │   ├── recipes.py            # Recipe endpoints
│   │   │   ├── ingredients.py        # Ingredient recognition
│   │   │   ├── favorites.py          # Favorites & ratings
│   │   │   └── chat.py               # Chatbot endpoints
│   │   ├── services/                 # Business logic
│   │   │   ├── gemini_service.py     # Gemini AI integration
│   │   │   ├── langchain_service.py  # LangChain chatbot
│   │   │   ├── image_processor.py    # Image processing
│   │   │   ├── recipe_matcher.py     # ⭐ Matching algorithm
│   │   │   ├── substitution_service.py
│   │   │   └── spoonacular_service.py
│   │   ├── models/                   # Data models
│   │   │   ├── recipe.py
│   │   │   └── user.py
│   │   ├── schemas/                  # Pydantic schemas
│   │   │   ├── recipe_schema.py
│   │   │   ├── ingredient_schema.py
│   │   │   ├── chat_schema.py
│   │   │   └── response_schema.py
│   │   ├── utils/                    # Utilities
│   │   │   ├── error_handlers.py
│   │   │   ├── validators.py
│   │   │   ├── helpers.py
│   │   │   └── logger.py
│   │   └── middleware/               # Middleware
│   │       └── cors.py
│   ├── data/                         # Seed data
│   │   ├── seed_recipes.py           # 30+ diverse recipes
│   │   └── supabase_schema.sql       # Database schema
│   ├── tests/                        # Test suite
│   │   ├── test_recipes.py
│   │   ├── test_ingredients.py
│   │   └── test_favorites.py
│   ├── requirements.txt              # Python dependencies
│   ├── requirements-langchain.txt    # LangChain dependencies
│   ├── .env.example                  # Environment template
│   ├── README.md                     # Backend documentation
│   └── Procfile                      # Deployment config
│
├── frontend/                         # Next.js Frontend
│   ├── app/                          # Next.js App Router
│   │   ├── layout.tsx                # Root layout
│   │   ├── page.tsx                  # Home page
│   │   ├── globals.css               # Global styles
│   │   ├── search/                   # Search page
│   │   ├── collection/               # Favorites page
│   │   └── recipe/[id]/              # Recipe detail
│   ├── components/                   # React components
│   │   ├── chat/                     # Chatbot components
│   │   │   ├── floating-chat.tsx
│   │   │   ├── chat-panel.tsx
│   │   │   └── message-list.tsx
│   │   ├── recipe/                   # Recipe components
│   │   │   ├── cooking-timer.tsx
│   │   │   ├── shopping-list.tsx
│   │   │   ├── recipe-card.tsx
│   │   │   └── recipe-detail.tsx
│   │   ├── ui/                       # UI components (shadcn)
│   │   ├── filter-bar.tsx
│   │   ├── search-bar.tsx
│   │   ├── site-navbar.tsx
│   │   ├── bottom-nav.tsx
│   │   ├── mobile-menu.tsx
│   │   ├── theme-toggle.tsx
│   │   └── recommended-recipes.tsx
│   ├── lib/                          # Utilities
│   │   ├── api.ts                    # API client
│   │   ├── cache.ts                  # Caching layer
│   │   ├── recommendations.ts        # Recommendation engine
│   │   ├── analytics.ts              # Analytics tracking
│   │   └── utils.ts                  # Helper functions
│   ├── hooks/                        # Custom hooks
│   │   ├── use-recipes.ts
│   │   ├── use-mobile.ts
│   │   └── use-toast.ts
│   ├── public/                       # Static assets
│   ├── package.json                  # Node dependencies
│   ├── tsconfig.json                 # TypeScript config
│   ├── tailwind.config.ts            # Tailwind config
│   └── next.config.mjs               # Next.js config
│
└── README.md                         # This file!
```

---

## 📚 API Documentation

### Base URL

**Development:** `http://localhost:8000/api/v1`  
**Production:** `https://your-backend.railway.app/api/v1`

### Key Endpoints

#### Health Check
```http
GET /api/v1/health
```

#### Ingredient Recognition
```http
POST /api/v1/ingredients/recognize-image
Content-Type: multipart/form-data

file: <image_file>
```

#### Recipe Search
```http
POST /api/v1/recipes/search
Content-Type: application/json

{
  "ingredients": ["chicken", "tomato"],
  "dietary_restrictions": ["gluten-free"],
  "cuisine": "italian",
  "max_cook_time": 45,
  "difficulty": "easy"
}
```

#### Chat Query
```http
POST /api/v1/chat/query
Content-Type: application/json

{
  "message": "How do I make this gluten-free?",
  "context": {
    "page": "recipe_detail",
    "recipe_id": "123",
    "recipe_title": "Pasta Carbonara"
  }
}
```

#### Ingredient Substitutions
```http
POST /api/v1/ingredients/substitutions
Content-Type: application/json

{
  "ingredient": "butter",
  "context": "baking"
}
```

### Interactive Documentation

Visit `http://localhost:8000/docs` for full Swagger UI with all endpoints, request/response schemas, and the ability to test endpoints directly!

---

## 🚢 Deployment

### Backend Deployment (Railway - Recommended)

1. **Install Railway CLI:**
```bash
npm install -g @railway/cli
```

2. **Login and deploy:**
```bash
cd backend
railway login
railway init
railway up
```

3. **Set environment variables** in Railway dashboard:
   - `GEMINI_API_KEY`
   - `SUPABASE_URL` (optional)
   - `SUPABASE_KEY` (optional)

### Frontend Deployment (Vercel - Recommended)

1. **Install Vercel CLI:**
```bash
npm install -g vercel
```

2. **Deploy:**
```bash
cd frontend
vercel
```

3. **Set environment variables** in Vercel dashboard:
   - `NEXT_PUBLIC_API_URL` (yer deployed backend URL)

### Alternative Deployment Options

- **Backend:** Render, Heroku, Google Cloud Run, AWS Lambda
- **Frontend:** Netlify, AWS Amplify, GitHub Pages (with adapter)

**Detailed deployment guides:** See `backend/DEPLOYMENT.md`

---

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_recipes.py -v
```

### Frontend Tests (Coming Soon)

```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage
```

---

## 🔧 Troubleshooting

### Backend Issues

**Problem:** Import errors or module not found
```bash
# Solution: Ensure virtual environment is activated and dependencies installed
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**Problem:** Gemini API errors
```bash
# Solution: Check API key in .env file
# Verify key is active at https://makersuite.google.com/app/apikey
# Check rate limits (1500 requests/day on free tier)
```

**Problem:** No recipes found
```bash
# Solution: Seed data is loaded from data/seed_recipes.py
# Ensure file is not corrupted and server is restarted
```

### Frontend Issues

**Problem:** Cannot connect to backend
```bash
# Solution: Verify backend is running on http://localhost:8000
# Check NEXT_PUBLIC_API_URL in .env.local
# Ensure CORS is enabled in backend
```

**Problem:** Build errors
```bash
# Solution: Clear cache and reinstall
rm -rf .next node_modules
npm install
npm run build
```

### Common Issues

**Problem:** Port already in use
```bash
# Backend: Change port in .env (PORT=8001)
# Frontend: Run on different port
npm run dev -- -p 3001
```

---

## 🎓 Key Learning Outcomes

This project demonstrates:

1. **Full-Stack Development** - Complete frontend and backend integration
2. **AI Integration** - Gemini Vision API, LangChain for conversational AI
3. **Advanced Algorithms** - Fuzzy matching, scoring algorithms
4. **Modern Web Development** - Next.js 15, FastAPI, TypeScript
5. **Production Practices** - Error handling, logging, testing, deployment
6. **UI/UX Design** - Responsive design, dark mode, accessibility
7. **Performance Optimization** - Caching, lazy loading, debouncing
8. **Mobile Development** - Touch gestures, responsive layouts

---

## 🏆 Features Checklist

### Core Features ✅
- [x] AI-powered ingredient recognition from images
- [x] Smart recipe matching with fuzzy search
- [x] Ingredient substitution suggestions
- [x] Dietary restriction filtering (13+ tags)
- [x] 30+ diverse recipes with complete data
- [x] Comprehensive error handling
- [x] Loading states and animations
- [x] Full API documentation

### Advanced Features ✅
- [x] AI chatbot with context awareness
- [x] Cooking timers (multiple)
- [x] Smart shopping lists
- [x] Theme toggle (light/dark/system)
- [x] Mobile optimization with bottom nav
- [x] Recommendation engine
- [x] Analytics & insights tracking
- [x] Image lazy loading & caching
- [x] Favorites & ratings system
- [x] Advanced search filters

### Production Ready ✅
- [x] TypeScript type safety
- [x] Pydantic validation
- [x] Comprehensive logging
- [x] Test suite
- [x] Deployment configs
- [x] Environment management
- [x] API rate limiting ready
- [x] Security best practices

---

## 📊 Project Statistics

- **Total Files:** 100+
- **Lines of Code:** 5,000+
- **Documentation:** 15,000+ words
- **Recipes:** 30 (fully detailed)
- **API Endpoints:** 15+
- **Test Cases:** 20+
- **Components:** 50+
- **Supported Cuisines:** 12+
- **Dietary Tags:** 13+
- **Features:** 35+

---

## 🤝 Contributing

Contributions be welcome! Here's how ye can help:

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/amazing-feature`
3. **Commit yer changes:** `git commit -m 'Add amazing feature'`
4. **Push to branch:** `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines
- Follow existing code style
- Add tests for new features
- Update documentation
- Use TypeScript for frontend
- Use type hints for backend
- Run linters before committing

---

## 📝 License

This project be licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Authors & Acknowledgments

Created with ❤️ for the Smart Recipe Generator project.

### Special Thanks
- **Google Gemini** - For powerful AI capabilities
- **FastAPI** - For the amazing Python framework
- **Next.js Team** - For the excellent React framework
- **shadcn/ui** - For beautiful, accessible components
- **LangChain** - For conversational AI framework

---

## 📞 Support

For questions, issues, or feedback:

1. **Check Documentation:**
   - Backend: `backend/README.md`
   - API: `backend/API_DOCUMENTATION.md`
   - Deployment: `backend/DEPLOYMENT.md`
   - Quickstart: `backend/QUICKSTART.md`

2. **Common Issues:** See [Troubleshooting](#-troubleshooting) section above

3. **Report Issues:** Create an issue in the repository

---

## 🗺️ Roadmap

### Phase 3 - Future Enhancements
- [ ] User authentication (JWT/OAuth)
- [ ] Meal planning calendar
- [ ] Recipe import from URLs
- [ ] Print-friendly recipe formatting
- [ ] Recipe sharing via email/social
- [ ] Video tutorial integration
- [ ] Nutritional tracking dashboard
- [ ] Grocery delivery integration
- [ ] Voice assistant integration
- [ ] Recipe scaling (adjust servings)
- [ ] Cooking mode (step-by-step with timers)
- [ ] Community features (comments, forums)

---

## 🎯 Quick Start Summary

```bash
# 1. Clone and setup
git clone <repo-url> && cd project

# 2. Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp env.example .env
# Edit .env with yer API keys

# 3. Frontend setup (new terminal)
cd frontend
npm install
echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1" > .env.local

# 4. Run backend
cd backend
uvicorn app.main:app --reload

# 5. Run frontend (new terminal)
cd frontend
npm run dev

# 6. Open browser
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

---

## 🏴‍☠️ Final Words

This be a complete, production-ready recipe discovery platform that showcases modern web development practices, AI integration, and thoughtful UX design. Whether ye be a beginner cook or a seasoned chef, this application will help ye discover new recipes and cook with confidence!

**Ready to start cooking? Fire up the servers and let's sail! ⚓🍳**

---

*Built with FastAPI, Next.js, React, TypeScript, and lots of ☕*

*Last Updated: October 2025*


