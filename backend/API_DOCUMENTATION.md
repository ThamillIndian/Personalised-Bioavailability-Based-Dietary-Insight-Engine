# 📖 API Documentation

Complete API reference for Smart Recipe Generator.

---

## Base URL

```
Production: https://your-app.railway.app/api/v1
Local: http://localhost:8000/api/v1
```

## Interactive Documentation

- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`

---

## Authentication

Currently no authentication required. Future versions will support:
- JWT tokens
- API keys
- OAuth2

---

## Common Response Format

### Success Response

```json
{
  "success": true,
  "data": { ... },
  "message": "Optional message"
}
```

### Error Response

```json
{
  "success": false,
  "error": {
    "message": "Error description",
    "details": { ... },
    "status_code": 400
  }
}
```

---

## Endpoints

### 1. Health & Status

#### GET /health

Check API health and service status.

**Response:**
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

---

### 2. Ingredient Recognition

#### POST /ingredients/recognize-image

Upload an image to recognize ingredients using AI.

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `file`: Image file (JPEG, PNG, WebP, max 10MB)

**Example:**
```bash
curl -X POST \
  -F "file=@ingredients.jpg" \
  https://api.example.com/api/v1/ingredients/recognize-image
```

**Response:**
```json
{
  "success": true,
  "ingredients": [
    {
      "name": "tomato",
      "confidence": 0.95,
      "quantity_estimate": "3-4 pieces",
      "category": "vegetable"
    },
    {
      "name": "onion",
      "confidence": 0.92,
      "quantity_estimate": "1 large",
      "category": "vegetable"
    }
  ],
  "total_found": 2,
  "processing_time_ms": 2340,
  "message": "Successfully recognized 2 ingredients"
}
```

**Error Codes:**
- `400`: Invalid file type or size
- `422`: Image processing failed
- `500`: AI service unavailable

---

#### POST /ingredients/recognize-text

Parse ingredients from text input.

**Request:**
```json
{
  "ingredients_text": "tomato, onion, garlic, chicken breast"
}
```

**Response:**
```json
{
  "success": true,
  "ingredients": ["tomato", "onion", "garlic", "chicken breast"],
  "total_found": 4
}
```

---

#### POST /ingredients/substitutions

Get substitution suggestions for an ingredient.

**Request:**
```json
{
  "ingredient": "butter",
  "context": "baking",
  "recipe_type": "cookies"
}
```

**Response:**
```json
{
  "success": true,
  "original_ingredient": "butter",
  "substitutions": [
    {
      "substitute": "coconut oil",
      "ratio": "1:1",
      "notes": "Best for baking, adds slight coconut flavor"
    },
    {
      "substitute": "applesauce",
      "ratio": "1:1",
      "notes": "Low-fat option, reduces calories"
    }
  ],
  "context": "baking cookies"
}
```

---

### 3. Recipe Search & Discovery

#### POST /recipes/search

Search recipes by ingredients and preferences.

**Request:**
```json
{
  "ingredients": ["chicken", "tomato", "onion", "garlic"],
  "dietary_restrictions": ["gluten-free"],
  "cuisine_type": "Indian",
  "max_prep_time": 30,
  "max_cook_time": 45,
  "difficulty": "medium",
  "limit": 10
}
```

**Response:**
```json
{
  "success": true,
  "recipes": [
    {
      "recipe": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "Chicken Tikka Masala",
        "description": "Creamy Indian curry...",
        "cuisine_type": "Indian",
        "difficulty": "medium",
        "prep_time": 30,
        "cook_time": 40,
        "servings": 6,
        "image_url": "https://...",
        "ingredients": [
          {
            "name": "chicken breast",
            "quantity": 800,
            "unit": "g",
            "is_critical": true,
            "category": "protein"
          }
        ],
        "instructions": [
          {
            "step_number": 1,
            "instruction": "Marinate chicken...",
            "duration_minutes": 30
          }
        ],
        "dietary_tags": ["gluten-free"],
        "nutrition": {
          "calories": 380,
          "protein": 35,
          "carbs": 18,
          "fat": 20,
          "fiber": 3,
          "sodium": 620
        }
      },
      "match_percentage": 85.5,
      "matched_ingredients": ["chicken", "tomato", "onion", "garlic"],
      "missing_ingredients": ["yogurt", "cream", "garam masala"],
      "can_make_with_substitutions": true
    }
  ],
  "total_found": 8,
  "query_info": {
    "ingredients_count": 4,
    "dietary_restrictions": ["gluten-free"],
    "cuisine_type": "Indian",
    "filters_applied": {
      "max_prep_time": 30,
      "max_cook_time": 45,
      "difficulty": "medium"
    }
  }
}
```

**Query Parameters:**
- `ingredients` (required): Array of ingredient names
- `dietary_restrictions` (optional): Array of dietary tags
- `cuisine_type` (optional): Cuisine filter
- `max_prep_time` (optional): Maximum prep time in minutes
- `max_cook_time` (optional): Maximum cook time in minutes
- `difficulty` (optional): easy | medium | hard
- `limit` (optional): Results limit (1-50, default: 10)

---

#### GET /recipes/

List all recipes with pagination and filters.

**Query Parameters:**
- `page` (default: 1)
- `page_size` (default: 10, max: 50)
- `cuisine` (optional)
- `difficulty` (optional)
- `dietary_tags` (optional, comma-separated)

**Example:**
```
GET /recipes/?page=1&page_size=10&cuisine=Italian&dietary_tags=vegetarian
```

**Response:**
```json
{
  "success": true,
  "recipes": [ ... ],
  "total": 30,
  "page": 1,
  "page_size": 10
}
```

---

#### GET /recipes/{recipe_id}

Get detailed information for a specific recipe.

**Path Parameters:**
- `recipe_id`: Recipe ID or index

**Response:**
```json
{
  "success": true,
  "recipe": {
    "id": "...",
    "title": "Spaghetti Carbonara",
    "description": "...",
    "ingredients": [...],
    "instructions": [...],
    "nutrition": {...}
  }
}
```

---

#### GET /recipes/filter/by-nutrition

Filter recipes by nutritional values.

**Query Parameters:**
- `max_calories` (optional)
- `min_protein` (optional)
- `max_carbs` (optional)
- `max_fat` (optional)

**Example:**
```
GET /recipes/filter/by-nutrition?max_calories=500&min_protein=20
```

**Response:**
```json
{
  "success": true,
  "recipes": [...],
  "total_found": 15
}
```

---

### 4. Favorites & Ratings

#### POST /favorites/

Add a recipe to favorites.

**Request:**
```json
{
  "recipe_id": "recipe-123",
  "user_id": "user-456"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Recipe added to favorites",
  "total_favorites": 5
}
```

---

#### GET /favorites/{user_id}

Get all favorites for a user.

**Response:**
```json
{
  "success": true,
  "user_id": "user-456",
  "favorites": ["recipe-123", "recipe-789"],
  "total": 2
}
```

---

#### DELETE /favorites/

Remove a recipe from favorites.

**Request:**
```json
{
  "recipe_id": "recipe-123",
  "user_id": "user-456"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Recipe removed from favorites",
  "total_favorites": 4
}
```

---

#### POST /favorites/ratings

Rate a recipe.

**Request:**
```json
{
  "recipe_id": "recipe-123",
  "user_id": "user-456",
  "rating": 5,
  "review": "Absolutely delicious!"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Rating added",
  "average_rating": 4.5,
  "total_ratings": 10
}
```

**Validation:**
- `rating`: Must be 1-5

---

#### GET /favorites/ratings/{recipe_id}

Get all ratings for a recipe.

**Response:**
```json
{
  "success": true,
  "recipe_id": "recipe-123",
  "average_rating": 4.5,
  "total_ratings": 10,
  "ratings": [
    {
      "user_id": "user-456",
      "rating": 5,
      "review": "Delicious!"
    }
  ]
}
```

---

## Data Models

### Recipe

```typescript
{
  id: UUID,
  title: string,
  description?: string,
  cuisine_type?: string,
  difficulty: "easy" | "medium" | "hard",
  prep_time: number,  // minutes
  cook_time: number,  // minutes
  servings: number,
  image_url?: string,
  ingredients: Ingredient[],
  instructions: Instruction[],
  dietary_tags: string[],
  nutrition?: NutritionInfo,
  created_at: datetime,
  updated_at: datetime
}
```

### Ingredient

```typescript
{
  name: string,
  quantity?: number,
  unit?: string,
  is_critical: boolean,
  category?: string
}
```

### NutritionInfo

```typescript
{
  calories?: number,
  protein?: number,  // grams
  carbs?: number,    // grams
  fat?: number,      // grams
  fiber?: number,    // grams
  sugar?: number,    // grams
  sodium?: number    // mg
}
```

---

## Rate Limits

- **Default**: 60 requests/minute per IP
- **Image Recognition**: 10 requests/minute
- **Gemini API**: 1500 requests/day (Google's limit)
- **Spoonacular**: 150 requests/day (free tier)

**Rate Limit Headers:**
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1642261200
```

---

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request - Invalid input |
| 404 | Not Found - Resource doesn't exist |
| 422 | Unprocessable Entity - Validation error |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error |
| 503 | Service Unavailable - External API down |

---

## Best Practices

1. **Always validate input** before sending
2. **Handle errors gracefully** - check success field
3. **Cache responses** when possible
4. **Respect rate limits** - implement backoff
5. **Use pagination** for large datasets
6. **Compress images** before uploading (< 5MB ideal)
7. **Set timeouts** for requests (10s recommended)

---

## Code Examples

### Python

```python
import requests

# Search recipes
response = requests.post(
    "https://api.example.com/api/v1/recipes/search",
    json={
        "ingredients": ["chicken", "rice"],
        "dietary_restrictions": ["gluten-free"],
        "limit": 5
    }
)

data = response.json()
if data["success"]:
    for match in data["recipes"]:
        print(f"{match['recipe']['title']}: {match['match_percentage']}%")
```

### JavaScript

```javascript
// Upload image
const formData = new FormData();
formData.append('file', imageFile);

const response = await fetch('/api/v1/ingredients/recognize-image', {
  method: 'POST',
  body: formData
});

const data = await response.json();
console.log(data.ingredients);
```

### cURL

```bash
# Get recipe detail
curl -X GET \
  "https://api.example.com/api/v1/recipes/0" \
  -H "Accept: application/json"
```

---

### 5. AI Chat Assistant

#### POST /chat/query

Get AI-powered recipe assistance and cooking tips.

**Request:**
```json
{
  "message": "How do I make this recipe gluten-free?",
  "context": {
    "page": "recipe_detail",
    "recipe_id": "recipe-123",
    "recipe_title": "Chicken Tikka Masala",
    "current_ingredients": ["chicken", "tomato", "onion"]
  },
  "conversation_id": "conv_123456"
}
```

**Response:**
```json
{
  "success": true,
  "message": "To make this recipe gluten-free, replace regular yogurt with gluten-free yogurt and ensure all spices are certified gluten-free. The recipe is naturally gluten-free as it doesn't contain wheat, barley, or rye.",
  "conversation_id": "conv_123456",
  "context_used": {
    "page": "recipe_detail",
    "recipe_id": "recipe-123",
    "recipe_title": "Chicken Tikka Masala"
  },
  "suggestions": [
    "How to make this spicier?",
    "What sides go well with this?",
    "Can I substitute any ingredients?",
    "How many calories in this recipe?"
  ],
  "response_time_ms": 1250
}
```

---

#### GET /chat/quick-questions

Get context-aware quick questions for the AI assistant.

**Query Parameters:**
- `page` (optional): Current page context
- `recipe_id` (optional): Current recipe ID
- `recipe_title` (optional): Current recipe title

**Response:**
```json
{
  "success": true,
  "questions": [
    "How to make this spicier?",
    "What can I substitute for this ingredient?",
    "How many calories in this recipe?",
    "Is this suitable for my diet?",
    "What sides go well with this?",
    "How to make this healthier?"
  ],
  "context": {
    "page": "recipe_detail",
    "recipe_id": "recipe-123",
    "recipe_title": "Chicken Tikka Masala"
  }
}
```

---

#### GET /chat/history/{conversation_id}

Get chat history for a conversation.

**Response:**
```json
{
  "success": true,
  "conversation_id": "conv_123456",
  "messages": [
    {
      "role": "user",
      "content": "How do I make this recipe gluten-free?",
      "timestamp": "2024-01-15T10:30:00Z"
    },
    {
      "role": "assistant",
      "content": "To make this recipe gluten-free, replace regular yogurt with gluten-free yogurt...",
      "timestamp": "2024-01-15T10:30:01Z"
    }
  ],
  "total_messages": 2
}
```

**Features:**
- Context-aware responses based on current page/recipe
- Short, crisp answers (max 2-3 sentences)
- Fallback support when recipes aren't in database
- Nutrition tracking and dietary advice
- Cooking tips and ingredient substitutions
- **LangChain-powered conversation memory**
- **Intelligent conversation history analysis**
- **Context-aware follow-up suggestions**
- **Conversation topic tracking**
- **Memory-based personalized recommendations**

#### DELETE /chat/history/{conversation_id}

Clear all conversation history for a conversation.

**Response:**
```json
{
  "success": true,
  "message": "Conversation history cleared for conv_123456",
  "conversation_id": "conv_123456"
}
```

**Enhanced Features with LangChain:**
- **Conversation Memory**: AI remembers previous questions and builds context
- **Topic Analysis**: Tracks conversation topics (nutrition, substitutions, cooking techniques)
- **Smart Suggestions**: Generates follow-up questions based on conversation history
- **Context Continuity**: References previous messages for better responses
- **Personalized Recommendations**: Tailors suggestions based on user's conversation patterns

---

## Support

- **Documentation**: `/docs`
- **Issues**: GitHub Issues
- **Email**: support@example.com

---

**Happy Cooking! 🍳**

