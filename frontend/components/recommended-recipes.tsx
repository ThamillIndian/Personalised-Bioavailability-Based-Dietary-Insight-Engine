"use client"

import { useEffect, useState } from 'react'
import { RecipeList } from './recipe-list'
import { useRecipes } from '@/hooks/use-recipes'
import { RecommendationEngine } from '@/lib/recommendations'
import { FrontendRecipe } from '@/lib/api'
import { Sparkles } from 'lucide-react'

interface RecommendedRecipesProps {
  count?: number
  className?: string
}

export function RecommendedRecipes({ count = 6, className }: RecommendedRecipesProps) {
  const { recipes: allRecipes, loading } = useRecipes(1, 50)
  const [recommendations, setRecommendations] = useState<FrontendRecipe[]>([])

  useEffect(() => {
    if (allRecipes.length > 0) {
      const recommended = RecommendationEngine.getRecommendations(allRecipes, count)
      setRecommendations(recommended)
    }
  }, [allRecipes, count])

  if (loading) {
    return (
      <div className={className}>
        <h2 className="mb-4 flex items-center gap-2 text-xl font-semibold">
          <Sparkles className="h-5 w-5 text-primary" />
          Recommended For You
        </h2>
        <div className="animate-pulse space-y-4">
          <div className="h-32 rounded-lg bg-gray-200" />
          <div className="h-32 rounded-lg bg-gray-200" />
          <div className="h-32 rounded-lg bg-gray-200" />
        </div>
      </div>
    )
  }

  if (recommendations.length === 0) {
    return null
  }

  return (
    <div className={className}>
      <h2 className="mb-4 flex items-center gap-2 text-xl font-semibold">
        <Sparkles className="h-5 w-5 text-primary" />
        Recommended For You
      </h2>
      <RecipeList recipes={recommendations} />
    </div>
  )
}
