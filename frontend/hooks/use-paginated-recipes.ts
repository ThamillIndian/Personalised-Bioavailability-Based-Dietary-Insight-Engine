"use client"

import { useState, useCallback } from 'react'
import { recipeApi, type PaginatedRecipeResponse } from '@/lib/api'

export function usePaginatedRecipes(pageSize: number = 20) {
  const [data, setData] = useState<PaginatedRecipeResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchRecipes = useCallback(async (page: number) => {
    setLoading(true)
    setError(null)
    
    try {
      const result = await recipeApi.getRecipesPaginated(page, pageSize)
      setData(result)
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to fetch recipes')
    } finally {
      setLoading(false)
    }
  }, [pageSize])

  return {
    data,
    loading,
    error,
    fetchRecipes
  }
}

