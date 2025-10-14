"use client"

import Link from "next/link"
import { useSavedRecipes } from "@/lib/use-saved-recipes"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Alert, AlertDescription } from "@/components/ui/alert"
import type { FrontendRecipe } from "@/lib/api"
import { cn } from "@/lib/utils"
import { AlertTriangle, CheckCircle, ShoppingCart } from "lucide-react"

interface RecipeMatch {
  recipe: FrontendRecipe
  matchPercentage: number
  matchedIngredients: string[]
  missingIngredients: string[]
  canMakeWithSubstitutions: boolean
}

interface RecipeCardWithMatchProps {
  recipeMatch: RecipeMatch
}

export function RecipeCardWithMatch({ recipeMatch }: RecipeCardWithMatchProps) {
  const { recipe, matchPercentage, matchedIngredients, missingIngredients, canMakeWithSubstitutions } = recipeMatch
  const { isSaved, toggle } = useSavedRecipes()
  const saved = isSaved(recipe.id)

  const getMatchColor = (percentage: number) => {
    if (percentage >= 80) return "text-green-600"
    if (percentage >= 60) return "text-yellow-600"
    if (percentage >= 40) return "text-orange-600"
    return "text-red-600"
  }

  const getMatchIcon = (percentage: number) => {
    if (percentage >= 80) return <CheckCircle className="h-4 w-4 text-green-600" />
    if (percentage >= 60) return <AlertTriangle className="h-4 w-4 text-yellow-600" />
    return <AlertTriangle className="h-4 w-4 text-orange-600" />
  }

  return (
    <Card className="transition-shadow hover:shadow-md">
      <CardHeader className="space-y-2">
        <CardTitle className="text-balance text-base">
          <Link href={`/recipe/${recipe.id}`} aria-label={`Open ${recipe.title}`} className="hover:underline">
            {recipe.title}
          </Link>
        </CardTitle>
        
        {/* Match Information */}
        <div className="flex items-center gap-2 text-sm">
          {getMatchIcon(matchPercentage)}
          <span className={cn("font-medium", getMatchColor(matchPercentage))}>
            {matchPercentage.toFixed(0)}% ingredient match
          </span>
        </div>

        {/* Matched Ingredients */}
        {matchedIngredients.length > 0 && (
          <div className="space-y-1">
            <p className="text-xs text-green-600 font-medium">✅ You have:</p>
            <div className="flex flex-wrap gap-1">
              {matchedIngredients.slice(0, 3).map((ingredient) => (
                <Badge key={ingredient} variant="secondary" className="text-xs bg-green-100 text-green-800 border-green-200">
                  {ingredient}
                </Badge>
              ))}
              {matchedIngredients.length > 3 && (
                <Badge variant="secondary" className="text-xs bg-green-100 text-green-800 border-green-200">
                  +{matchedIngredients.length - 3} more
                </Badge>
              )}
            </div>
          </div>
        )}

        {/* Missing Ingredients Alert */}
        {missingIngredients.length > 0 && (
          <Alert className="py-2">
            <ShoppingCart className="h-4 w-4" />
            <AlertDescription className="text-xs">
              <div className="space-y-1">
                <p className="font-medium text-orange-600">Missing ingredients:</p>
                <div className="flex flex-wrap gap-1">
                  {missingIngredients.slice(0, 3).map((ingredient) => (
                    <Badge key={ingredient} variant="outline" className="text-xs border-orange-200 text-orange-700">
                      {ingredient}
                    </Badge>
                  ))}
                  {missingIngredients.length > 3 && (
                    <Badge variant="outline" className="text-xs border-orange-200 text-orange-700">
                      +{missingIngredients.length - 3} more
                    </Badge>
                  )}
                </div>
                {canMakeWithSubstitutions && (
                  <p className="text-green-600 text-xs mt-1">💡 Can be made with substitutions</p>
                )}
              </div>
            </AlertDescription>
          </Alert>
        )}

        {/* Recipe Tags */}
        <div className="flex flex-wrap gap-1">
          {recipe.dietTags.slice(0, 3).map((tag) => (
            <Badge key={tag} variant="secondary" className="text-xs">
              {tag}
            </Badge>
          ))}
        </div>
      </CardHeader>
      
      <CardContent className="flex items-center justify-between">
        <div className="text-sm text-foreground/70">
          <span className="mr-3">{recipe.time} min</span>
          <span>{recipe.calories} kcal</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-sm" aria-label="rating">
            ⭐ {recipe.rating > 0 ? recipe.rating.toFixed(1) : "No rating"}
          </span>
          <Button
            variant={saved ? "secondary" : "outline"}
            size="sm"
            onClick={() => toggle(recipe.id)}
            aria-pressed={saved}
            className={cn(saved && "bg-secondary")}
          >
            {saved ? "Added to favourite" : "Add to favourite"}
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
