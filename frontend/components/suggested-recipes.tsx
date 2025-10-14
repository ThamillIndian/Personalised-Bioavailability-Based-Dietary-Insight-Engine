"use client"

import * as React from "react"
import { useSavedRecipes } from "@/lib/use-saved-recipes"
import { type FrontendRecipe } from "@/lib/api"
import { RecipeCard } from "@/components/recipe-card"
import { cn } from "@/lib/utils"

export function SuggestedRecipes({
  recipes = [],
  max = 6,
  className,
}: {
  recipes?: FrontendRecipe[]
  max?: number
  className?: string
}) {
  const { savedIds } = useSavedRecipes()
  const savedSet = React.useMemo(() => new Set(savedIds), [savedIds])

  // Build simple affinity counts from saved items using dietTags
  const affinity = React.useMemo(() => {
    const counts = new Map<string, number>()
    recipes.forEach((r) => {
      if (!savedSet.has(r.id)) return
      r.dietTags?.forEach((t) => counts.set(t, (counts.get(t) || 0) + 1))
    })
    return counts
  }, [recipes, savedSet])

  const suggestions = React.useMemo(() => {
    if (!savedIds?.length) return []
    return recipes
      .filter((r) => !savedSet.has(r.id))
      .map((r) => {
        let score = 0
        r.dietTags?.forEach((t) => (score += affinity.get(t) || 0))
        return { r, score }
      })
      .filter((x) => x.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, max)
      .map((x) => x.r)
  }, [recipes, savedSet, affinity, max, savedIds])

  if (!savedIds?.length || suggestions.length === 0) return null

  return (
    <section aria-labelledby="suggested-heading" className={cn("space-y-4", className)}>
      <div className="flex items-center justify-between">
        <h2 id="suggested-heading" className="text-lg font-semibold text-pretty">
          Suggested recipes based on your favorites
        </h2>
        <span className="text-xs text-muted-foreground">Personalized from saved items</span>
      </div>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {suggestions.map((recipe) => (
          <RecipeCard key={recipe.id} recipe={recipe} />
        ))}
      </div>
    </section>
  )
}
