/**
 * API Service Layer for Smart Recipe Generator
 * Handles all backend communications with proper error handling
 */

import { cache } from './cache'

// Types matching backend schema
export interface BackendRecipe {
  id: string
  title: string
  description: string
  cuisine_type: string
  difficulty: string
  prep_time: number
  cook_time: number
  servings: number
  image_url: string
  ingredients: Array<{
    name: string
    quantity: number
    unit: string
    is_critical: boolean
    category: string
  }>
  instructions: Array<{
    step_number: number
    instruction: string
    duration_minutes: number
  }>
  dietary_tags: string[]
  nutrition: {
    calories: number
    protein: number
    carbs: number
    fat: number
    fiber: number
    sugar: number
    sodium: number
  }
  created_at: string
  updated_at: string
}

export interface FrontendRecipe {
  id: string
  title: string
  image: string
  time: number // prep_time + cook_time
  calories: number
  dietTags: string[]
  rating: number
  ingredients: string[]
  instructions: string[]
  description: string
  cuisine_type: string
  difficulty: string
  servings: number
}

// Backend enum values
export type DietaryRestriction = "vegetarian" | "vegan" | "gluten-free" | "dairy-free" | "nut-free" | "egg-free" | "soy-free" | "low-carb" | "keto" | "paleo" | "pescatarian" | "halal" | "kosher"
export type CuisineType = "Italian" | "Indian" | "Mexican" | "Japanese" | "Thai" | "Chinese" | "Greek" | "French" | "American" | "Mediterranean" | "Middle Eastern" | "Hawaiian"
export type DifficultyLevel = "easy" | "medium" | "hard"

export interface RecipeSearchRequest {
  ingredients: string[]
  dietary_restrictions?: DietaryRestriction[]
  cuisine_type?: CuisineType
  max_prep_time?: number
  max_cook_time?: number
  difficulty?: DifficultyLevel
  limit?: number
}

export interface RecipeSearchResponse {
  success: boolean
  recipes: Array<{
    recipe: BackendRecipe
    match_percentage: number
    matched_ingredients: string[]
    missing_ingredients: string[]
    can_make_with_substitutions: boolean
  }>
  total_found: number
  query_info: any
}

export interface RecipeListResponse {
  success: boolean
  recipes: BackendRecipe[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

export interface RatingRequest {
  recipe_id: string
  user_id: string
  rating: number
  review?: string
}

export interface RatingResponse {
  success: boolean
  message: string
  average_rating: number
  total_ratings: number
}

export interface FavoriteRequest {
  recipe_id: string
  user_id: string
}

export interface FavoriteResponse {
  success: boolean
  message: string
  total_favorites: number
}

// API Configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
const API_V1_URL = `${API_BASE_URL}/api/v1`

// Debug logging
if (process.env.NODE_ENV === 'development') {
  console.log('🔧 API Configuration:', { 
    API_BASE_URL, 
    API_V1_URL,
    NODE_ENV: process.env.NODE_ENV,
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL
  })
}

// Helper function to transform backend recipe to frontend format
function transformRecipe(backendRecipe: BackendRecipe, rating?: number): FrontendRecipe {
  return {
    id: backendRecipe.id,
    title: backendRecipe.title,
    image: backendRecipe.image_url,
    time: backendRecipe.prep_time + backendRecipe.cook_time,
    calories: backendRecipe.nutrition.calories,
    dietTags: backendRecipe.dietary_tags,
    rating: rating ?? 0, // Use provided rating or default to 0
    ingredients: backendRecipe.ingredients.map(ing => 
      `${ing.quantity} ${ing.unit} ${ing.name}`
    ),
    instructions: backendRecipe.instructions
      .sort((a, b) => a.step_number - b.step_number)
      .map(step => step.instruction),
    description: backendRecipe.description,
    cuisine_type: backendRecipe.cuisine_type,
    difficulty: backendRecipe.difficulty,
    servings: backendRecipe.servings
  }
}

// Generic fetch wrapper with error handling
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_V1_URL}${endpoint}`
  
  const defaultHeaders: Record<string, string> = {}
  
  // Only set Content-Type for requests with body
  if (options.body) {
    defaultHeaders['Content-Type'] = 'application/json'
  }

  const config: RequestInit = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  }
  
  if (process.env.NODE_ENV === 'development') {
    console.log(`🔍 API Request: ${options.method || 'GET'} ${url}`)
    console.log(`📊 Request Config:`, {
      method: options.method || 'GET',
      headers: config.headers,
      body: options.body ? 'Present' : 'None',
      url: url,
      endpoint: endpoint
    })
  }

  try {
    const response = await fetch(url, config)
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      if (process.env.NODE_ENV === 'development') {
        console.error(`❌ API Error [${response.status}]:`, errorData)
        console.error(`🔍 Response Headers:`, Object.fromEntries(response.headers.entries()))
        console.error(`🔍 Response URL:`, response.url)
      }
      throw new Error(
        errorData.message || 
        `HTTP ${response.status}: ${response.statusText}`
      )
    }

    const result = await response.json()
    return result
  } catch (error) {
    console.error(`❌ API Error [${endpoint}]:`, error)
    throw error
  }
}

// Recipe API Functions
export const recipeApi = {
  // Get all recipes with pagination
  // Helper function to fetch rating for a recipe
  async getRecipeRating(recipeId: string): Promise<number> {
    try {
      const response = await apiRequest<{
        success: boolean
        average_rating: number
        total_ratings: number
      }>(`/favorites/ratings/${recipeId}`)
      
      return response.success ? response.average_rating : 0
    } catch (error) {
      console.warn(`Failed to fetch rating for recipe ${recipeId}:`, error)
      return 0
    }
  },

  async getRecipes(page: number = 1, pageSize: number = 20): Promise<FrontendRecipe[]> {
    // Ensure pageSize doesn't exceed backend limit of 50
    const validPageSize = Math.min(pageSize, 50)
    const response = await apiRequest<RecipeListResponse>(
      `/recipes/?page=${page}&page_size=${validPageSize}`
    )
    
    if (!response.success) {
      throw new Error('Failed to fetch recipes')
    }
    
    // Fetch ratings for all recipes in parallel
    const recipesWithRatings = await Promise.all(
      response.recipes.map(async (recipe) => {
        const rating = await recipeApi.getRecipeRating(recipe.id)
        return transformRecipe(recipe, rating)
      })
    )
    
    return recipesWithRatings
  },

  // Get recipe by ID (with caching)
  async getRecipeById(id: string): Promise<FrontendRecipe | null> {
    const cacheKey = `recipe:${id}`
    
    // Check cache first
    const cached = cache.get<FrontendRecipe>(cacheKey)
    if (cached) {
      if (process.env.NODE_ENV === 'development') {
        console.log(`✅ Cache hit for recipe: ${id}`)
      }
      return cached
    }
    
    try {
      const response = await apiRequest<{ success: boolean; recipe: BackendRecipe }>(
        `/recipes/${id}`
      )
      
      if (!response.success || !response.recipe) {
        return null
      }
      
      // Fetch rating for this recipe
      const rating = await recipeApi.getRecipeRating(id)
      const transformed = transformRecipe(response.recipe, rating)
      
      // Cache for 10 minutes
      cache.set(cacheKey, transformed, 10 * 60 * 1000)
      
      return transformed
    } catch (error) {
      console.error(`Failed to fetch recipe ${id}:`, error)
      return null
    }
  },

  // Search recipes
  async searchRecipes(searchRequest: RecipeSearchRequest): Promise<{
    recipes: FrontendRecipe[]
    totalFound: number
    matchInfo: any
    recipeMatches: Array<{
      recipe: FrontendRecipe
      matchPercentage: number
      matchedIngredients: string[]
      missingIngredients: string[]
      canMakeWithSubstitutions: boolean
    }>
  }> {
    // Ensure required fields are present
    const requestWithDefaults = {
      ...searchRequest,
      limit: searchRequest.limit || 10  // Backend requires limit field
    }
    
    const response = await apiRequest<RecipeSearchResponse>(
      '/recipes/search',
      {
        method: 'POST',
        body: JSON.stringify(requestWithDefaults),
      }
    )
    
    if (!response.success) {
      throw new Error('Failed to search recipes')
    }
    
    // Fetch ratings for all recipes in parallel
    const recipesWithRatings = await Promise.all(
      response.recipes.map(async (item) => {
        const rating = await recipeApi.getRecipeRating(item.recipe.id)
        return {
          recipe: transformRecipe(item.recipe, rating),
          matchPercentage: item.match_percentage,
          matchedIngredients: item.matched_ingredients,
          missingIngredients: item.missing_ingredients,
          canMakeWithSubstitutions: item.can_make_with_substitutions
        }
      })
    )
    
    const transformedRecipes = recipesWithRatings.map(item => item.recipe)
    const recipeMatches = recipesWithRatings
    
    return {
      recipes: transformedRecipes,
      totalFound: response.total_found,
      matchInfo: response.query_info,
      recipeMatches
    }
  },

  // Get recipe options (cuisine types, difficulty levels, dietary restrictions)
  async getRecipeOptions() {
    const response = await apiRequest<{
      success: boolean
      options: {
        cuisine_types: string[]
        difficulty_levels: string[]
        dietary_restrictions: string[]
        total_recipes: number
      }
    }>('/recipes/options')
    
    return response.options
  }
}

// Favorites API Functions
export const favoritesApi = {
  // Add recipe to favorites
  async addFavorite(recipeId: string, userId: string): Promise<FavoriteResponse> {
    return apiRequest<FavoriteResponse>('/favorites/', {
      method: 'POST',
      body: JSON.stringify({
        recipe_id: recipeId,
        user_id: userId
      }),
    })
  },

  // Remove recipe from favorites
  async removeFavorite(recipeId: string, userId: string): Promise<FavoriteResponse> {
    return apiRequest<FavoriteResponse>('/favorites/', {
      method: 'DELETE',
      body: JSON.stringify({
        recipe_id: recipeId,
        user_id: userId
      }),
    })
  },

  // Get user's favorites
  async getUserFavorites(userId: string): Promise<string[]> {
    const response = await apiRequest<{
      success: boolean
      user_id: string
      favorites: string[]
      total: number
    }>(`/favorites/${userId}`)
    
    return response.favorites || []
  }
}

// Ratings API Functions
export const ratingsApi = {
  // Rate a recipe
  async rateRecipe(recipeId: string, userId: string, rating: number, review?: string): Promise<RatingResponse> {
    return apiRequest<RatingResponse>('/favorites/ratings', {
      method: 'POST',
      body: JSON.stringify({
        recipe_id: recipeId,
        user_id: userId,
        rating,
        review
      }),
    })
  },

  // Get recipe ratings
  async getRecipeRatings(recipeId: string): Promise<{
    average_rating: number
    total_ratings: number
    ratings: Array<{
      user_id: string
      rating: number
      review: string
    }>
  }> {
    const response = await apiRequest<{
      success: boolean
      recipe_id: string
      average_rating: number
      total_ratings: number
      ratings: Array<{
        user_id: string
        rating: number
        review: string
      }>
    }>(`/favorites/ratings/${recipeId}`)
    
    return {
      average_rating: response.average_rating,
      total_ratings: response.total_ratings,
      ratings: response.ratings
    }
  }
}

// Ingredient Recognition API Functions
export const ingredientApi = {
  // Recognize ingredients from image
  async recognizeImage(file: File): Promise<{
    ingredients: Array<{
      name: string
      confidence: number
      quantity_estimate: string
      category: string
    }>
    total_found: number
    processing_time_ms: number
  }> {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await fetch(`${API_V1_URL}/ingredients/recognize-image`, {
      method: 'POST',
      body: formData,
    })
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
    
    return await response.json()
  }
}

// Chat API Functions
export const chatApi = {
  // Send chat message
  async sendMessage(message: string, conversationId?: string, context?: any): Promise<{
    message: string
    conversation_id: string
    suggestions?: string[]
    response_time_ms?: number
  }> {
    return apiRequest('/chat/query', {
      method: 'POST',
      body: JSON.stringify({
        message,
        conversation_id: conversationId,
        context
      }),
    })
  },

  // Get quick questions
  async getQuickQuestions(page?: string, recipeId?: string, recipeTitle?: string): Promise<{
    questions: string[]
  }> {
    const params = new URLSearchParams()
    if (page) params.append('page', page)
    if (recipeId) params.append('recipe_id', recipeId)
    if (recipeTitle) params.append('recipe_title', recipeTitle)
    
    const response = await apiRequest<{
      success: boolean
      questions: string[]
    }>(`/chat/quick-questions?${params.toString()}`)
    
    return { questions: response.questions }
  }
}

// Health check
export const healthApi = {
  async checkHealth(): Promise<{
    status: string
    version: string
    timestamp: string
    database_connected: boolean
    services: {
      database: boolean
      gemini_ai: boolean
      spoonacular: boolean
    }
  }> {
    return apiRequest('/health')
  }
}
