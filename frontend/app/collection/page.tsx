"use client"

import { Button } from "@/components/ui/button"
import { RecipeList } from "@/components/recipe-list"
import { useSavedRecipes } from "@/lib/use-saved-recipes"
import { useRecipes } from "@/hooks/use-recipes"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Loader2, AlertCircle } from "lucide-react"

export default function CollectionPage() {
  const { savedIds, clear, isLoading, error } = useSavedRecipes()
  
  // Fetch all recipes to filter saved ones (limited to 50 by backend)
  const { recipes: allRecipes, loading: recipesLoading, error: recipesError } = useRecipes(1, 50)
  
  // Filter to get only saved recipes
  const savedRecipes = allRecipes.filter((r) => savedIds.includes(r.id))

  const handleClear = async () => {
    await clear()
  }

  return (
    <main className="mx-auto max-w-6xl px-4 py-10">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">My Collection</h1>
        {savedRecipes.length > 0 && (
          <Button variant="outline" size="sm" onClick={handleClear}>
            Clear all
          </Button>
        )}
      </div>

      <div className="mt-6">
        {/* Loading State */}
        {(isLoading || recipesLoading) ? (
          <div className="rounded-lg border p-8 text-center">
            <div className="flex items-center justify-center gap-2">
              <Loader2 className="h-5 w-5 animate-spin" />
              <p className="text-foreground/70">Loading your saved recipes…</p>
            </div>
          </div>
        ) : /* Error State */ (error || recipesError) ? (
          <div className="space-y-4">
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>
                Failed to load collection: {error || recipesError}
              </AlertDescription>
            </Alert>
          </div>
        ) : /* Empty State */ savedRecipes.length === 0 ? (
          <div className="rounded-lg border p-8 text-center">
            <p className="text-pretty text-foreground/70">
              Your saved recipes will appear here. From any recipe card, click "Add to favourite" to add it to your
              collection.
            </p>
          </div>
        ) : /* Saved Recipes */ (
          <>
            <div className="mb-4 text-sm text-muted-foreground">
              {savedRecipes.length} saved recipe{savedRecipes.length !== 1 ? 's' : ''}
            </div>
            <RecipeList recipes={savedRecipes} />
          </>
        )}
      </div>
    </main>
  )
}
