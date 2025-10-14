"use client"

import { SuggestedRecipes } from "@/components/suggested-recipes"
import { RecommendedRecipes } from "@/components/recommended-recipes"
import { useRecipes } from "@/hooks/use-recipes"
import { Button } from "@/components/ui/button"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Loader2, AlertCircle } from "lucide-react"

export function HomePageClient() {
  const { recipes, loading, error, refetch } = useRecipes(1, 8) // Get first 8 recipes for home page

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="flex items-center gap-2">
          <Loader2 className="h-5 w-5 animate-spin" />
          <span className="text-sm text-muted-foreground">Loading featured recipes...</span>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="space-y-4">
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>
            Failed to load recipes: {error}
          </AlertDescription>
        </Alert>
        <Button onClick={refetch} variant="outline" size="sm">
          Try Again
        </Button>
        <div className="rounded-lg border p-8 text-center">
          <p className="text-sm text-muted-foreground">
            Unable to load recipes from server. Please check your connection and try again.
          </p>
        </div>
      </div>
    )
  }

  if (!recipes.length) {
    return (
      <div className="rounded-lg border p-8 text-center">
        <p className="text-sm text-muted-foreground">
          No recipes available at the moment. Please try again later.
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <RecommendedRecipes count={6} />
      <SuggestedRecipes recipes={recipes} />
    </div>
  )
}
