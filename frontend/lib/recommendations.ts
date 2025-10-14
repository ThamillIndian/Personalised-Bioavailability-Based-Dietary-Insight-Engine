/**
 * Recipe Recommendation Engine
 * Provides personalized recipe suggestions based on user behavior
 */

import { FrontendRecipe } from './api'

interface UserPreferences {
  favoriteRecipes: string[]
  viewedRecipes: string[]
  searchHistory: string[]
  dietaryPreferences: string[]
  cuisinePreferences: string[]
}

export class RecommendationEngine {
  private static STORAGE_KEY = 'srgr:user_preferences'

  /**
   * Get user preferences from localStorage
   */
  static getUserPreferences(): UserPreferences {
    if (typeof window === 'undefined') {
      return {
        favoriteRecipes: [],
        viewedRecipes: [],
        searchHistory: [],
        dietaryPreferences: [],
        cuisinePreferences: []
      }
    }

    const stored = localStorage.getItem(this.STORAGE_KEY)
    if (!stored) {
      return {
        favoriteRecipes: [],
        viewedRecipes: [],
        searchHistory: [],
        dietaryPreferences: [],
        cuisinePreferences: []
      }
    }

    try {
      return JSON.parse(stored)
    } catch {
      return {
        favoriteRecipes: [],
        viewedRecipes: [],
        searchHistory: [],
        dietaryPreferences: [],
        cuisinePreferences: []
      }
    }
  }

  /**
   * Save user preferences to localStorage
   */
  static saveUserPreferences(preferences: UserPreferences) {
    if (typeof window === 'undefined') return
    localStorage.setItem(this.STORAGE_KEY, JSON.stringify(preferences))
  }

  /**
   * Track recipe view
   */
  static trackRecipeView(recipeId: string) {
    const preferences = this.getUserPreferences()
    
    // Add to viewed recipes (keep last 50)
    preferences.viewedRecipes = [
      recipeId,
      ...preferences.viewedRecipes.filter(id => id !== recipeId)
    ].slice(0, 50)

    this.saveUserPreferences(preferences)
  }

  /**
   * Track search query
   */
  static trackSearch(query: string, filters?: any) {
    const preferences = this.getUserPreferences()
    
    // Track search ingredients
    preferences.searchHistory = [
      query,
      ...preferences.searchHistory.filter(q => q !== query)
    ].slice(0, 20)

    // Track dietary preferences from filters
    if (filters?.dietary_restrictions) {
      filters.dietary_restrictions.forEach((diet: string) => {
        if (!preferences.dietaryPreferences.includes(diet)) {
          preferences.dietaryPreferences.push(diet)
        }
      })
    }

    // Track cuisine preferences from filters
    if (filters?.cuisine_type && !preferences.cuisinePreferences.includes(filters.cuisine_type)) {
      preferences.cuisinePreferences.push(filters.cuisine_type)
    }

    this.saveUserPreferences(preferences)
  }

  /**
   * Calculate recipe score based on user preferences
   */
  static calculateRecipeScore(recipe: FrontendRecipe, preferences: UserPreferences): number {
    let score = 0

    // Check if recipe matches dietary preferences
    if (preferences.dietaryPreferences.length > 0) {
      const matchingDiets = recipe.dietTags.filter(tag => 
        preferences.dietaryPreferences.includes(tag)
      )
      score += matchingDiets.length * 10
    }

    // Check if recipe matches cuisine preferences
    if (preferences.cuisinePreferences.length > 0 && recipe.cuisine_type) {
      if (preferences.cuisinePreferences.includes(recipe.cuisine_type)) {
        score += 15
      }
    }

    // Boost score for recipes with ingredients from search history
    if (preferences.searchHistory.length > 0 && recipe.ingredients) {
      const searchTerms = preferences.searchHistory.flatMap(q => q.toLowerCase().split(',').map(t => t.trim()))
      const matchingIngredients = recipe.ingredients.filter(ingredient =>
        searchTerms.some(term => ingredient.toLowerCase().includes(term))
      )
      score += matchingIngredients.length * 5
    }

    // Boost highly rated recipes
    score += recipe.rating * 2

    // Penalize recipes already viewed recently (for variety)
    if (preferences.viewedRecipes.slice(0, 10).includes(recipe.id)) {
      score -= 5
    }

    return score
  }

  /**
   * Get recommended recipes
   */
  static getRecommendations(
    recipes: FrontendRecipe[],
    count: number = 6
  ): FrontendRecipe[] {
    const preferences = this.getUserPreferences()
    
    // Calculate scores for all recipes
    const scoredRecipes = recipes.map(recipe => ({
      recipe,
      score: this.calculateRecipeScore(recipe, preferences)
    }))

    // Sort by score (descending) and return top N
    return scoredRecipes
      .sort((a, b) => b.score - a.score)
      .slice(0, count)
      .map(item => item.recipe)
  }

  /**
   * Get similar recipes based on a given recipe
   */
  static getSimilarRecipes(
    targetRecipe: FrontendRecipe,
    allRecipes: FrontendRecipe[],
    count: number = 6
  ): FrontendRecipe[] {
    const scoredRecipes = allRecipes
      .filter(recipe => recipe.id !== targetRecipe.id)
      .map(recipe => {
        let score = 0

        // Same cuisine type
        if (recipe.cuisine_type === targetRecipe.cuisine_type) {
          score += 20
        }

        // Same difficulty
        if (recipe.difficulty === targetRecipe.difficulty) {
          score += 10
        }

        // Matching dietary tags
        const matchingTags = recipe.dietTags.filter(tag =>
          targetRecipe.dietTags.includes(tag)
        )
        score += matchingTags.length * 8

        // Similar cooking time (within 15 minutes)
        if (Math.abs(recipe.time - targetRecipe.time) <= 15) {
          score += 5
        }

        // Similar calories (within 100 kcal)
        if (Math.abs(recipe.calories - targetRecipe.calories) <= 100) {
          score += 5
        }

        return { recipe, score }
      })

    return scoredRecipes
      .sort((a, b) => b.score - a.score)
      .slice(0, count)
      .map(item => item.recipe)
  }

  /**
   * Clear user preferences
   */
  static clearPreferences() {
    if (typeof window === 'undefined') return
    localStorage.removeItem(this.STORAGE_KEY)
  }
}
