"use client"

import Link from "next/link"
import { useSavedRecipes } from "@/lib/use-saved-recipes"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import type { FrontendRecipe } from "@/lib/api"
import { cn } from "@/lib/utils"

export function RecipeCard({ recipe }: { recipe: FrontendRecipe }) {
  const { isSaved, toggle } = useSavedRecipes()
  const saved = isSaved(recipe.id)

  return (
    <Card className="transition-shadow hover:shadow-md">
      <CardHeader className="space-y-2">
        <CardTitle className="text-balance text-base">
          <Link href={`/recipe/${recipe.id}`} aria-label={`Open ${recipe.title}`} className="hover:underline">
            {recipe.title}
          </Link>
        </CardTitle>
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
