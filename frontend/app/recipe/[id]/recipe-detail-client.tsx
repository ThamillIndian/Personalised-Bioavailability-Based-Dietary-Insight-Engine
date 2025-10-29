"use client"

import Link from "next/link"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { SaveRecipeButton } from "@/components/save-recipe-button"
import { SubstitutionsPanel } from "@/components/recipe/substitutions-panel"
import { RatingWidget } from "@/components/recipe/rating-widget"
import { CookingTimer } from "@/components/recipe/cooking-timer"
import { ShoppingList } from "@/components/recipe/shopping-list"
import { BioavailabilityPanel } from "@/components/nutrition/bioavailability-panel"
import { useRecipe } from "@/hooks/use-recipes"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Loader2, AlertCircle } from "lucide-react"
import { useRecipeContext } from "@/components/chat/recipe-context-provider"
import { RecommendationEngine } from "@/lib/recommendations"
import { useEffect } from "react"
import { nutritionApi, type StressLevel, type CookingMethod } from "@/lib/api"

interface RecipeDetailClientProps {
  recipeId: string
}

export function RecipeDetailClient({ recipeId }: RecipeDetailClientProps) {
  const { recipe, loading, error, refetch } = useRecipe(recipeId)
  const { setRecipeContext, clearRecipeContext } = useRecipeContext()

  // Nutrition calculation state
  const [openPanel, setOpenPanel] = useState(false)
  const [isCalculating, setIsCalculating] = useState(false)
  const [bioResults, setBioResults] = useState<{
    base: Record<string, number>
    adjusted: Record<string, number>
    userContext?: {
      age: number
      weight_kg: number
      height_cm: number
      stress_level: StressLevel
      cooking_method: CookingMethod
      post_workout: boolean
    }
  } | null>(null)
  const [rdaResults, setRdaResults] = useState<{
    coverage: Record<string, string>
    recommendations: Array<{
      nutrient: string
      coverage: string
      suggestions: { high: string[]; medium: string[] }
    }>
  } | null>(null)

  // Parse ingredient string to extract name and quantity
  const parseIngredient = (ingStr: string): { name: string; quantity_g: number; category: string } => {
    // Try to parse "300 g basmati rice" format
    const match = ingStr.match(/^\s*(\d+(?:\.\d+)?)\s*([A-Za-z]+)\s+(.+)$/i)
    if (match) {
      const qty = parseFloat(match[1])
      const unit = match[2].toLowerCase()
      const name = match[3].trim()
      
      // Convert to grams (rough estimates)
      let grams = qty
      if (unit === "kg") grams = qty * 1000
      else if (unit === "g" || unit === "gram" || unit === "grams") grams = qty
      else if (unit === "tbsp" || unit === "tablespoon") grams = qty * 15 // rough estimate
      else if (unit === "tsp" || unit === "teaspoon") grams = qty * 5 // rough estimate
      else if (unit === "cup" || unit === "cups") grams = qty * 240 // rough estimate
      else if (unit === "ml" || unit === "milliliter") grams = qty // close enough for liquids
      
      // Categorize ingredient
      const lower = name.toLowerCase()
      let category = "Vegetables"
      if (lower.includes("paneer") || lower.includes("chicken") || lower.includes("egg") || 
          lower.includes("dal") || lower.includes("rajma") || lower.includes("chana") ||
          lower.includes("meat") || lower.includes("fish")) {
        category = "Meat"
      } else if (lower.includes("rice") || lower.includes("wheat") || lower.includes("flour") || 
                 lower.includes("poha") || lower.includes("roti") || lower.includes("bread")) {
        category = "Grains"
      } else if (lower.includes("milk") || lower.includes("curd") || lower.includes("yogurt") ||
                 lower.includes("cheese") || lower.includes("butter")) {
        category = "Dairy"
      }
      
      return { name, quantity_g: grams, category }
    }
    
    // Fallback: assume 100g
    return { name: ingStr.trim(), quantity_g: 100, category: "Vegetables" }
  }

  // Handle bioavailability calculation
  const handleBioavailabilitySubmit = async (values: {
    age: number
    weight_kg: number
    height_cm: number
    stress_level: StressLevel
    cooking_method: CookingMethod
    post_workout: boolean
    sleep_hours?: number
    meal_time?: string
    time_since_last_meal_min?: number
    hydration_liters?: number
    caffeine_mg?: number
    menstrual_phase?: string
  }) => {
    if (!recipe) return
    
    setIsCalculating(true)
    try {
      const ingredients = recipe.ingredients.map(parseIngredient)

      const response = await nutritionApi.bioavailability({
        ingredients,
        cooking_method: values.cooking_method,
        stress_level: values.stress_level,
        age: values.age,
        post_workout: values.post_workout,
        sleep_hours: values.sleep_hours,
        meal_time: values.meal_time,
        time_since_last_meal_min: values.time_since_last_meal_min,
        hydration_liters: values.hydration_liters,
        caffeine_mg: values.caffeine_mg,
        menstrual_phase: values.menstrual_phase,
      })

      setBioResults({
        base: response.base_nutrients,
        adjusted: response.adjusted_nutrients,
        userContext: {
          age: values.age,
          weight_kg: values.weight_kg,
          height_cm: values.height_cm,
          stress_level: values.stress_level,
          cooking_method: values.cooking_method,
          post_workout: values.post_workout,
        },
      })
      setRdaResults(null) // Clear previous RDA results
      setOpenPanel(false)
    } catch (error) {
      console.error("Failed to calculate bioavailability:", error)
      alert("Failed to calculate bioavailability. Please try again.")
    } finally {
      setIsCalculating(false)
    }
  }

  // Handle RDA calculation
  const handleRDACalculation = async () => {
    if (!bioResults || !bioResults.userContext) return
    
    setIsCalculating(true)
    try {
      const response = await nutritionApi.rdaCoverage({
        adjusted_nutrients: bioResults.adjusted,
        age: bioResults.userContext.age,
        weight_kg: bioResults.userContext.weight_kg,
        height_cm: bioResults.userContext.height_cm,
      })

      setRdaResults({
        coverage: response.rda_coverage,
        recommendations: response.recommendations,
      })
    } catch (error) {
      console.error("Failed to calculate RDA:", error)
      alert("Failed to calculate RDA coverage. Please try again.")
    } finally {
      setIsCalculating(false)
    }
  }

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
          <div className="mt-4 flex flex-wrap gap-2">
            <SaveRecipeButton recipeId={recipe.id} />
            <Link href="/search">
              <Button variant="outline">Back to Search</Button>
            </Link>
            <Button
              onClick={() => setOpenPanel(true)}
              disabled={isCalculating}
              variant="default"
            >
              Check Bioavailability
            </Button>
            <Button
              onClick={handleRDACalculation}
              disabled={isCalculating || !bioResults}
              variant="secondary"
            >
              RDA
            </Button>
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

      {/* Bioavailability Results */}
      {bioResults && (
        <section className="mt-8 rounded-lg border p-4">
          <h2 className="mb-4 text-lg font-semibold">Bioavailability Results</h2>
          <div className="grid gap-6 md:grid-cols-2">
            <div className="space-y-2">
              <h3 className="font-medium text-base">Base Nutrients</h3>
              <div className="rounded-md bg-muted/30 p-3">
                <ul className="space-y-1.5 text-sm">
                  {Object.entries(bioResults.base).length > 0 ? (
                    Object.entries(bioResults.base).map(([nutrient, value]) => (
                      <li key={nutrient} className="flex justify-between">
                        <span className="text-muted-foreground">{nutrient}:</span>
                        <span className="font-medium">{typeof value === 'number' ? value.toFixed(2) : value} {nutrient.includes('Energy') || nutrient.includes('Calories') ? 'kcal' : nutrient.includes('Protein') || nutrient.includes('Carbohydrate') || nutrient.includes('Fat') || nutrient.includes('Fiber') ? 'g' : 'mg'}</span>
                      </li>
                    ))
                  ) : (
                    <li className="text-muted-foreground">No nutrient data available</li>
                  )}
                </ul>
              </div>
            </div>
            <div className="space-y-2">
              <h3 className="font-medium text-base">Adjusted Nutrients (Bioavailable)</h3>
              <div className="rounded-md bg-primary/5 p-3">
                <ul className="space-y-1.5 text-sm">
                  {Object.entries(bioResults.adjusted).length > 0 ? (
                    Object.entries(bioResults.adjusted).map(([nutrient, value]) => (
                      <li key={nutrient} className="flex justify-between">
                        <span className="text-muted-foreground">{nutrient}:</span>
                        <span className="font-medium">{typeof value === 'number' ? value.toFixed(2) : value} {nutrient.includes('Energy') || nutrient.includes('Calories') ? 'kcal' : nutrient.includes('Protein') || nutrient.includes('Carbohydrate') || nutrient.includes('Fat') || nutrient.includes('Fiber') ? 'g' : 'mg'}</span>
                      </li>
                    ))
                  ) : (
                    <li className="text-muted-foreground">No nutrient data available</li>
                  )}
                </ul>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* RDA Coverage Results */}
      {rdaResults && (
        <section className="mt-6 rounded-lg border p-4">
          <h2 className="mb-4 text-lg font-semibold">RDA Coverage</h2>
          <div className="space-y-4">
            <div className="rounded-md bg-muted/30 p-3">
              <h3 className="mb-2 font-medium text-sm">Coverage Percentages</h3>
              <ul className="space-y-1.5 text-sm">
                {Object.entries(rdaResults.coverage).length > 0 ? (
                  Object.entries(rdaResults.coverage).map(([nutrient, coverage]) => {
                    const coverageNum = parseFloat(coverage.replace('%', ''))
                    const isLow = coverageNum < 50
                    return (
                      <li key={nutrient} className="flex items-center justify-between">
                        <span className={isLow ? "text-destructive font-medium" : ""}>{nutrient}:</span>
                        <span className={`font-medium ${isLow ? "text-destructive" : ""}`}>{coverage}</span>
                      </li>
                    )
                  })
                ) : (
                  <li className="text-muted-foreground">No coverage data available</li>
                )}
              </ul>
            </div>

            {rdaResults.recommendations && rdaResults.recommendations.length > 0 && (
              <div className="space-y-3">
                <h3 className="font-medium text-base">Suggestions for Low Coverage Nutrients</h3>
                <div className="space-y-3">
                  {rdaResults.recommendations.map((rec, idx) => (
                    <div key={idx} className="rounded-md border p-3">
                      <div className="mb-2">
                        <span className="font-medium text-sm">{rec.nutrient}</span>
                        <span className="ml-2 text-sm text-muted-foreground">- {rec.coverage}</span>
                      </div>
                      <div className="grid gap-2 text-xs">
                        {rec.suggestions.high && rec.suggestions.high.length > 0 && (
                          <div>
                            <span className="font-medium text-green-600 dark:text-green-400">High sources: </span>
                            <span className="text-muted-foreground">{rec.suggestions.high.join(", ")}</span>
                          </div>
                        )}
                        {rec.suggestions.medium && rec.suggestions.medium.length > 0 && (
                          <div>
                            <span className="font-medium text-blue-600 dark:text-blue-400">Medium sources: </span>
                            <span className="text-muted-foreground">{rec.suggestions.medium.join(", ")}</span>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </section>
      )}

      {/* Cooking Tools Section */}
      <section className="mt-8 grid gap-6 md:grid-cols-2">
        <CookingTimer />
        <ShoppingList ingredients={recipe.ingredients} />
      </section>

      {/* Bioavailability Panel */}
      <BioavailabilityPanel
        open={openPanel}
        onOpenChange={setOpenPanel}
        onSubmit={handleBioavailabilitySubmit}
      />
    </main>
  )
}
