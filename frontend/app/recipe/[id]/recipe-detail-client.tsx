"use client"

import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { SaveRecipeButton } from "@/components/save-recipe-button"
import { SubstitutionsPanel } from "@/components/recipe/substitutions-panel"
import { RatingWidget } from "@/components/recipe/rating-widget"
import { CookingTimer } from "@/components/recipe/cooking-timer"
import { ShoppingList } from "@/components/recipe/shopping-list"
import { useRecipe } from "@/hooks/use-recipes"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Loader2, AlertCircle } from "lucide-react"
import { useRecipeContext } from "@/components/chat/recipe-context-provider"
import { RecommendationEngine } from "@/lib/recommendations"
import { useEffect } from "react"

interface RecipeDetailClientProps {
  recipeId: string
}

export function RecipeDetailClient({ recipeId }: RecipeDetailClientProps) {
  const { recipe, loading, error, refetch } = useRecipe(recipeId)
  const { setRecipeContext, clearRecipeContext } = useRecipeContext()

  // Track recipe view and set context for chatbot
  useEffect(() => {
    if (recipe) {
      // Track view for recommendations
      RecommendationEngine.trackRecipeView(recipe.id)
      
      // Set context for chatbot
      setRecipeContext({
        id: recipe.id,
        title: recipe.title,
        ingredients: recipe.ingredients,
        dietaryTags: recipe.dietTags,
        cuisineType: recipe.cuisine_type,
        difficulty: recipe.difficulty,
        cookTime: recipe.time,
        prepTime: 0 // We don't have separate prep time in frontend
      })
    }

    // Clear context when component unmounts
    return () => {
      clearRecipeContext()
    }
  }, [recipe, setRecipeContext, clearRecipeContext])

  if (loading) {
    return (
      <main className="mx-auto max-w-4xl px-4 py-8">
        <div className="flex items-center justify-center py-12">
          <div className="flex items-center gap-2">
            <Loader2 className="h-5 w-5 animate-spin" />
            <span className="text-sm text-muted-foreground">Loading recipe...</span>
          </div>
        </div>
      </main>
    )
  }

  if (error) {
    return (
      <main className="mx-auto max-w-4xl px-4 py-8">
        <div className="space-y-4">
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>
              Failed to load recipe: {error}
            </AlertDescription>
          </Alert>
          <Button onClick={refetch} variant="outline" size="sm">
            Try Again
          </Button>
        </div>
      </main>
    )
  }

  if (!recipe) {
    return (
      <main className="mx-auto max-w-3xl px-4 py-10">
        <div className="rounded-lg border p-8 text-center">
          <h1 className="mb-2 text-xl font-semibold">Recipe not found</h1>
          <p className="text-foreground/70">Try browsing or searching for another recipe.</p>
          <div className="mt-4 flex justify-center">
            <Link href="/search">
              <Button>Search</Button>
            </Link>
          </div>
        </div>
      </main>
    )
  }

  return (
    <main className="mx-auto max-w-4xl px-4 py-8">
      <div className="grid gap-6">
        <div>
          <h1 className="text-pretty text-2xl font-semibold">{recipe.title}</h1>
          <p className="mt-2 text-sm text-muted-foreground">{recipe.description}</p>
          <div className="mt-2 flex flex-wrap gap-2">
            {recipe.dietTags.map((t) => (
              <Badge key={t} variant="secondary">
                {t}
              </Badge>
            ))}
          </div>
          <div className="mt-3 text-sm text-foreground/70">
            <span className="mr-3">⏱ {recipe.time} min</span>
            <span>🔥 {recipe.calories} kcal</span>
            <span className="ml-3">👥 {recipe.servings} servings</span>
            <span className="ml-3">🌍 {recipe.cuisine_type}</span>
          </div>
          <div className="mt-4 flex gap-2">
            <SaveRecipeButton recipeId={recipe.id} />
            <Link href="/search">
              <Button variant="outline">Back to Search</Button>
            </Link>
          </div>
          <div className="mt-4">
            <RatingWidget 
              recipeId={recipe.id} 
              enableAutosave={true}
              showSaveButton={false}
            />
          </div>
        </div>
      </div>

      <section className="mt-8 grid gap-6 md:grid-cols-2">
        <div className="rounded-lg border p-4">
          <h2 className="mb-2 text-lg font-semibold">Ingredients</h2>
          <ul className="list-inside list-disc space-y-1">
            {recipe.ingredients.map((i, idx) => (
              <li key={idx}>{i}</li>
            ))}
          </ul>
        </div>
        <div className="rounded-lg border p-4">
          <h2 className="mb-2 text-lg font-semibold">Instructions</h2>
          <ol className="list-inside list-decimal space-y-2">
            {recipe.instructions.map((step, idx) => (
              <li key={idx}>{step}</li>
            ))}
          </ol>
        </div>
      </section>

      <section className="mt-8 grid gap-6 md:grid-cols-2">
        <RatingWidget
          recipeId={recipe.id}
          initialRating={0}
          enableAutosave={true}
          showSaveButton={false}
          className="rounded-lg border p-4"
        />
        <SubstitutionsPanel recipeId={recipe.id} ingredients={recipe.ingredients} className="rounded-lg border p-4" />
      </section>

      {/* Cooking Tools Section */}
      <section className="mt-8 grid gap-6 md:grid-cols-2">
        <CookingTimer />
        <ShoppingList ingredients={recipe.ingredients} />
      </section>
    </main>
  )
}
