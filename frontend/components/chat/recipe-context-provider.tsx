"use client"

import { createContext, useContext, useState, ReactNode, useCallback } from 'react'

interface RecipeContextType {
  id?: string
  title?: string
  ingredients?: string[]
  dietaryTags?: string[]
  cuisineType?: string
  difficulty?: string
  cookTime?: number
  prepTime?: number
}

interface RecipeContextProviderProps {
  children: ReactNode
}

const RecipeContext = createContext<{
  recipeContext: RecipeContextType
  setRecipeContext: (context: RecipeContextType) => void
  clearRecipeContext: () => void
} | undefined>(undefined)

export function RecipeContextProvider({ children }: RecipeContextProviderProps) {
  const [recipeContext, setRecipeContextState] = useState<RecipeContextType>({})

  const setRecipeContext = useCallback((context: RecipeContextType) => {
    setRecipeContextState(context)
  }, [])

  const clearRecipeContext = useCallback(() => {
    setRecipeContextState({})
  }, [])

  return (
    <RecipeContext.Provider value={{ recipeContext, setRecipeContext, clearRecipeContext }}>
      {children}
    </RecipeContext.Provider>
  )
}

export function useRecipeContext() {
  const context = useContext(RecipeContext)
  if (context === undefined) {
    throw new Error('useRecipeContext must be used within a RecipeContextProvider')
  }
  return context
}
