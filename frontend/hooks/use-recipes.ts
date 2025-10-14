"use client"

import { useState, useEffect, useCallback } from 'react'
import { recipeApi, type FrontendRecipe, type RecipeSearchRequest } from '@/lib/api'

interface RecipeMatch {
  recipe: FrontendRecipe
  matchPercentage: number
  matchedIngredients: string[]
  missingIngredients: string[]
  canMakeWithSubstitutions: boolean
}

interface UseRecipesState {
  recipes: FrontendRecipe[]
  recipeMatches: RecipeMatch[]
  loading: boolean
  error: string | null
  totalFound: number
}

interface UseRecipesReturn extends UseRecipesState {
  refetch: () => Promise<void>
  searchRecipes: (searchRequest: RecipeSearchRequest) => Promise<void>
  clearError: () => void
}

export function useRecipes(initialPage: number = 1, pageSize: number = 20): UseRecipesReturn {
  const [state, setState] = useState<UseRecipesState>({
    recipes: [],
    recipeMatches: [],
    loading: true,
    error: null,
    totalFound: 0
  })

  const fetchRecipes = useCallback(async (page: number = initialPage) => {
    setState(prev => ({ ...prev, loading: true, error: null }))
    
    try {
      const recipes = await recipeApi.getRecipes(page, pageSize)
      setState(prev => ({
        ...prev,
        recipes,
        loading: false,
        totalFound: recipes.length
      }))
    } catch (error) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: error instanceof Error ? error.message : 'Failed to fetch recipes'
      }))
    }
  }, [initialPage, pageSize])

  const searchRecipes = useCallback(async (searchRequest: RecipeSearchRequest) => {
    setState(prev => ({ ...prev, loading: true, error: null }))
    
    try {
      const result = await recipeApi.searchRecipes(searchRequest)
      setState(prev => ({
        ...prev,
        recipes: result.recipes,
        recipeMatches: result.recipeMatches,
        loading: false,
        totalFound: result.totalFound
      }))
    } catch (error) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: error instanceof Error ? error.message : 'Failed to search recipes'
      }))
    }
  }, [])

  const refetch = useCallback(() => fetchRecipes(), [fetchRecipes])
  
  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }))
  }, [])

  useEffect(() => {
    fetchRecipes()
  }, [fetchRecipes])

  return {
    ...state,
    refetch,
    searchRecipes,
    clearError
  }
}

interface UseRecipeReturn {
  recipe: FrontendRecipe | null
  loading: boolean
  error: string | null
  refetch: () => Promise<void>
}

export function useRecipe(recipeId: string): UseRecipeReturn {
  const [recipe, setRecipe] = useState<FrontendRecipe | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchRecipe = useCallback(async () => {
    if (!recipeId) return
    
    setLoading(true)
    setError(null)
    
    try {
      const fetchedRecipe = await recipeApi.getRecipeById(recipeId)
      setRecipe(fetchedRecipe)
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to fetch recipe')
    } finally {
      setLoading(false)
    }
  }, [recipeId])

  useEffect(() => {
    fetchRecipe()
  }, [fetchRecipe])

  return {
    recipe,
    loading,
    error,
    refetch: fetchRecipe
  }
}

interface UseRecipeOptionsReturn {
  options: {
    cuisine_types: string[]
    difficulty_levels: string[]
    dietary_restrictions: string[]
    total_recipes: number
  } | null
  loading: boolean
  error: string | null
  refetch: () => Promise<void>
}

export function useRecipeOptions(): UseRecipeOptionsReturn {
  const [options, setOptions] = useState<UseRecipeOptionsReturn['options']>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchOptions = useCallback(async () => {
    setLoading(true)
    setError(null)
    
    try {
      const fetchedOptions = await recipeApi.getRecipeOptions()
      setOptions(fetchedOptions)
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to fetch recipe options')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchOptions()
  }, [fetchOptions])

  return {
    options,
    loading,
    error,
    refetch: fetchOptions
  }
}
