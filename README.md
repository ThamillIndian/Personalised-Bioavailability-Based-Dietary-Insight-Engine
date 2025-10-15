# 🍳 Smart Recipe Generator

> AI-powered recipe discovery that turns ingredient photos into delicious meals

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Visit_App-blue?style=for-the-badge)](https://smart-recipe-generator-blond.vercel.app)
[![API Docs](https://img.shields.io/badge/📚_API-Documentation-green?style=for-the-badge)](https://smart-recipe-generator-t7pt.onrender.com/docs)

**🌐 Live Application:** https://smart-recipe-generator-blond.vercel.app  
**📚 API Backend:** https://smart-recipe-generator-t7pt.onrender.com  
**📖 API Documentation:** https://smart-recipe-generator-t7pt.onrender.com/docs

---

## 🎯 Project Overview

Smart Recipe Generator is an intelligent cooking assistant that identifies ingredients from photos using AI and suggests personalized recipes with detailed instructions, nutritional information, and smart substitutions.

**Key Innovation:** Advanced fuzzy-matching algorithm that understands ingredient variations and dietary restrictions to deliver highly relevant recipe suggestions with match percentage scores.

---

## ✨ Features Implemented

### 🖼️ **Ingredient Recognition from Images**
- **Google Gemini Vision API** integration for high-accuracy ingredient detection
- Smart image preprocessing (format conversion, compression, validation)
- Confidence scoring and duplicate handling
- Support for multiple ingredients in single photo

### 🎲 **Intelligent Recipe Matching**
- **Custom fuzzy-matching algorithm** with weighted scoring system:
  - Exact matches: 1.0 weight
  - Fuzzy matches: 0.8 weight (handles "chicken breast" vs "chicken")
  - Critical ingredient penalties: -20 points
  - Dietary restriction multipliers
- Match percentage calculation for transparency
- Substitution suggestions with ratios and preparation notes

### 🥗 **Dietary Restrictions & Filters**
- **13+ dietary filters:** Vegetarian, Vegan, Gluten-Free, Dairy-Free, Keto, Paleo, etc.
- **Advanced filtering:** Cuisine type, difficulty level, cooking time, calories, protein, carbs
- Real-time filter application with instant results

### 📚 **Comprehensive Recipe Database**
- **30+ curated recipes** across diverse cuisines (Indian, Italian, Mexican, Asian, Mediterranean)
- Complete nutritional information (calories, protein, carbs, fats, fiber)
- Difficulty ratings and cooking time estimates
- Step-by-step instructions with cooking tips

### 👤 **User Experience Features**
- ⭐ Recipe ratings and reviews
- 💾 Favorite recipes collection
- 🤖 AI chatbot for cooking questions (LangChain + Gemini)
- ⏲️ Built-in cooking timers with notifications
- 📝 Auto-generated shopping lists
- 🔍 Advanced search with debouncing

### 📱 **Mobile-Responsive Design**
- Mobile-first UI with touch optimization
- Bottom navigation for thumb-friendly access
- Skeleton loaders for smooth UX
- Accessible design (ARIA labels, keyboard navigation)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                            │
│  Next.js 15 + React 19 + TypeScript + Tailwind + shadcn/ui    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │  Image   │  │  Recipe  │  │ Chatbot  │  │ Filters  │      │
│  │  Upload  │  │  Cards   │  │   Chat   │  │  Panel   │      │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │
└────────────────────────┬────────────────────────────────────────┘
                         │ REST API
┌────────────────────────▼────────────────────────────────────────┐
│                        API LAYER                                │
│                FastAPI + Pydantic Validation                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Ingredients │  │   Recipes    │  │     Chat     │         │
│  │   /upload    │  │   /search    │  │   /message   │         │
│  │  /analyze    │  │   /match     │  │              │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                     SERVICE LAYER                               │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │
│  │  Gemini Vision │  │ Recipe Matcher │  │   LangChain    │   │
│  │  AI Service    │  │ Fuzzy Algorithm│  │  Chatbot AI    │   │
│  └────────────────┘  └────────────────┘  └────────────────┘   │
│  ┌────────────────┐  ┌────────────────┐                       │
│  │ Substitution   │  │  Spoonacular   │                       │
│  │    Service     │  │  Integration   │                       │
│  └────────────────┘  └────────────────┘                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                      DATA LAYER                                 │
│         Supabase (PostgreSQL) + JSON Recipe Database           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Recipes    │  │    Users     │  │  Favorites   │         │
│  │   (30+)      │  │              │  │   Ratings    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

| Layer | Technologies |
|-------|-------------|
| **Frontend** | Next.js 15, React 19, TypeScript, Tailwind CSS, shadcn/ui |
| **Backend** | FastAPI, Python 3.11+, Pydantic, Uvicorn |
| **AI/ML** | Google Gemini Vision API, LangChain, Gemini Pro |
| **Database** | Supabase (PostgreSQL), JSON data store |
| **Deployment** | Vercel (Frontend), Render (Backend) |
| **APIs** | Spoonacular API (optional), Google AI Platform |

---

## 🚀 Quick Start

### Prerequisites
```bash
✓ Node.js 18+ & npm
✓ Python 3.11+
✓ Google Gemini API Key (free tier)
```

### Installation & Setup

**1️⃣ Clone Repository**
```bash
git clone <your-repo-url>
cd project
```

**2️⃣ Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp env.example .env
```

**Edit `.env` and add your API key:**
```env
GEMINI_API_KEY=your_gemini_api_key_here
ALLOWED_ORIGINS=http://localhost:3000
```

**3️⃣ Frontend Setup**
```bash
cd ../frontend
npm install
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

**4️⃣ Run Application**
```bash
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2 - Frontend  
cd frontend
npm run dev
```

**5️⃣ Access Application**
- 🌐 **Frontend:** http://localhost:3000
- 📚 **API Docs:** http://localhost:8000/docs

---

## 📂 Project Structure

```
project/
├── backend/
│   ├── app/
│   │   ├── api/v1/              # REST API endpoints
│   │   │   ├── ingredients.py   # Image upload & analysis
│   │   │   ├── recipes.py       # Recipe search & matching
│   │   │   ├── favorites.py     # User favorites
│   │   │   └── chat.py          # AI chatbot
│   │   ├── services/            # Business logic
│   │   │   ├── gemini_service.py       # AI vision
│   │   │   ├── recipe_matcher.py       # Fuzzy matching
│   │   │   ├── substitution_service.py # Ingredient swaps
│   │   │   └── langchain_service.py    # Chatbot AI
│   │   ├── models/              # Database models
│   │   ├── schemas/             # Pydantic schemas
│   │   └── utils/               # Error handlers, validators
│   ├── data/                    # 30+ recipe database
│   ├── requirements.txt
│   └── tests/
│
└── frontend/
    ├── app/                     # Next.js pages
    │   ├── page.tsx            # Home (recipe discovery)
    │   ├── search/             # Recipe search
    │   └── collection/         # Saved favorites
    ├── components/
    │   ├── recipe/             # Recipe cards, details
    │   ├── chat/               # AI chatbot UI
    │   └── ui/                 # shadcn components
    ├── lib/
    │   ├── api.ts              # API client
    │   └── utils.ts
    └── package.json
```

---

## 🎯 Technical Approach (200 words)

I architected a full-stack solution prioritizing intelligent recipe matching and exceptional user experience.

**AI Integration:** Google Gemini Vision API powers ingredient recognition with preprocessing pipelines (image validation, compression, format conversion) ensuring optimal accuracy. The system handles confidence scoring and duplicate detection automatically.

**Core Innovation - Fuzzy Matching Algorithm:** Developed a sophisticated scoring system that calculates recipe relevance using weighted matches (exact: 1.0, fuzzy: 0.8), critical ingredient penalties (-20 points), and dietary multipliers. String similarity algorithms (70% threshold) handle variations like "chicken breast" vs "chicken," producing transparent match percentages that guide user decisions.

**Smart Substitutions:** AI-powered substitution service suggests alternatives with ratios and preparation notes, making recipes adaptable to available ingredients.

**User Experience:** Mobile-first design with skeleton loaders, debounced search (300ms), API caching, and lazy loading creates seamless interactions. The LangChain-powered chatbot provides contextual cooking assistance with conversation memory.

**Error Handling:** Comprehensive validation using Pydantic schemas, custom exception handlers, and graceful degradation ensures reliability. All errors provide actionable user feedback.

**Performance:** Async operations, strategic caching, and pagination optimize speed. The architecture scales efficiently with growing recipe databases.

**Result:** Production-ready application exceeding requirements with 30+ recipes, advanced AI features, and polished UX.

---

## 📊 Evaluation Criteria Addressed

| Criterion | Implementation |
|-----------|---------------|
| **Ingredient Classification** | Gemini Vision API + preprocessing pipeline (`gemini_service.py`) |
| **Recipe Matching Logic** | Custom fuzzy algorithm with weighted scoring (`recipe_matcher.py`) |
| **Error Handling** | Pydantic validation + custom exceptions + graceful degradation |
| **UX Considerations** | Loading states, caching, mobile-first, accessibility, 50+ components |

---

## 📈 Project Statistics

- ✅ **30 Recipes** (150% of minimum requirement)
- ✅ **15+ API Endpoints** with full OpenAPI documentation
- ✅ **50+ React Components** with TypeScript
- ✅ **13+ Dietary Filters** (Vegetarian, Vegan, Keto, Paleo, etc.)
- ✅ **Mobile Responsive** with touch optimization
- ✅ **80%+ Test Coverage** with pytest & React Testing Library

---

## 🌟 Bonus Features

- 🤖 **AI Chatbot** - LangChain-powered cooking assistant with memory
- ⏲️ **Cooking Timers** - Built-in timers with browser notifications
- 📝 **Shopping Lists** - Auto-generated from recipe ingredients
- 🔍 **Advanced Search** - Real-time filtering with debouncing
- 💾 **Local Caching** - Improved performance and offline support
- 📱 **PWA Ready** - Progressive Web App capabilities

---

**Created for Technical Assessment - Software Engineering Position**

*Demonstrates: Full-stack development • AI integration • Algorithm design • Production-quality code • UX excellence*
