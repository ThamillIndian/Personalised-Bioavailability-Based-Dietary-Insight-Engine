"use client"

import type { FrontendRecipe } from "@/lib/api"
import { RecipeCard } from "./recipe-card"

export function RecipeList({ recipes }: { recipes: FrontendRecipe[] }) {
  if (!recipes?.length) {
    return (
      <div className="rounded-lg border p-8 text-center">
        <p className="text-pretty text-sm text-foreground/70">
          No recipes found. Try adjusting your search or filters.
        </p>
      </div>
    )
  }

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {recipes.map((r) => (
        <RecipeCard key={r.id} recipe={r} />
      ))}
    </div>
  )
}
