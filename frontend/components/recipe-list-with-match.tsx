"use client"

import { RecipeCardWithMatch } from "./recipe-card-with-match"

interface RecipeMatch {
  recipe: any
  matchPercentage: number
  matchedIngredients: string[]
  missingIngredients: string[]
  canMakeWithSubstitutions: boolean
}

interface RecipeListWithMatchProps {
  recipeMatches: RecipeMatch[]
  className?: string
}

export function RecipeListWithMatch({ recipeMatches, className }: RecipeListWithMatchProps) {
  if (!recipeMatches.length) {
    return (
      <div className={`text-center py-8 ${className || ''}`}>
        <p className="text-muted-foreground">No recipes found. Try adjusting your search criteria.</p>
      </div>
    )
  }

  return (
    <div className={`grid gap-4 md:grid-cols-2 lg:grid-cols-3 ${className || ''}`}>
      {recipeMatches.map((recipeMatch) => (
        <RecipeCardWithMatch
          key={recipeMatch.recipe.id}
          recipeMatch={recipeMatch}
        />
      ))}
    </div>
  )
}
