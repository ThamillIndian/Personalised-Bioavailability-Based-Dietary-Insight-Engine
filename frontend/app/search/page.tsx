"use client"

import { useState, useCallback, useEffect } from "react"
import { SearchBar } from "@/components/search-bar"
import { FilterBar, type Filters } from "@/components/filter-bar"
import { RecipeList } from "@/components/recipe-list"
import { RecipeListWithMatch } from "@/components/recipe-list-with-match"
import { ImageIngredientUploader } from "@/components/search/image-ingredient-uploader"
import { useRecipes } from "@/hooks/use-recipes"
import { Button } from "@/components/ui/button"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Loader2, AlertCircle } from "lucide-react"
import type { RecipeSearchRequest } from "@/lib/api"
import { analytics } from "@/lib/analytics"
import { RecommendationEngine } from "@/lib/recommendations"

export default function SearchPage() {
  const [query, setQuery] = useState("")
  const [filters, setFilters] = useState<Filters>({ 
    diet: "Any",
    cuisine: "Any",
    difficulty: "Any"
  })
  const [mode, setMode] = useState<"text" | "image">("text")
  const [chips, setChips] = useState<string[]>([]) // show extracted ingredients
  const [hasSearched, setHasSearched] = useState(false)

  // Use the recipes hook for API calls
  const { recipes: searchResults, recipeMatches, loading, error, searchRecipes, refetch } = useRecipes()

  // Default recipes for initial load
  const { recipes: defaultRecipes, loading: defaultLoading, error: defaultError } = useRecipes(1, 20)

  const performSearch = useCallback(async () => {
    // Check if we have any search criteria
    const hasQuery = query.trim()
    const hasFilters = filters.diet !== "Any" || 
                      filters.cuisine !== "Any" || 
                      filters.difficulty !== "Any" || 
                      filters.maxTime || 
                      filters.maxCalories ||
                      filters.maxProtein ||
                      filters.maxCarbs
    
    if (!hasQuery && !hasFilters) {
      setHasSearched(false)
      return
    }

    setHasSearched(true)
    
    // Map frontend diet values to backend enum values
    const dietMapping: Record<string, string> = {
      "Vegetarian": "vegetarian",
      "Vegan": "vegan", 
      "Pescatarian": "pescatarian",
      "Gluten-Free": "gluten-free",
      "High-Protein": "low-carb", // Map to closest match
      "Low-Carb": "low-carb"
    }

    // Map frontend difficulty values to backend enum values
    const difficultyMapping: Record<string, string> = {
      "Easy": "easy",
      "Medium": "medium",
      "Hard": "hard"
    }
    
    const searchRequest: RecipeSearchRequest = {
      // If no query but filters applied, use a comprehensive ingredient list
      ingredients: hasQuery
        ? query.split(',').map(ing => ing.trim()).filter(Boolean)
        : ["chicken", "tomato", "onion", "garlic", "pasta", "rice", "vegetables", "beans", "cheese", "eggs", "flour", "oil", "salt", "pepper"], // Comprehensive default search
      dietary_restrictions: filters.diet !== "Any" && dietMapping[filters.diet]
        ? [dietMapping[filters.diet] as any]
        : undefined,
      cuisine_type: filters.cuisine !== "Any" ? filters.cuisine as any : undefined,
      difficulty: filters.difficulty !== "Any" ? difficultyMapping[filters.difficulty] as any : undefined,
      max_cook_time: filters.maxTime,
      limit: 50
    }

    try {
      if (process.env.NODE_ENV === 'development') {
        console.log('🔍 Enhanced Search Request:', searchRequest)
      }
      const result = await searchRecipes(searchRequest)
      
      // Track search analytics
      analytics.trackSearch(query || 'filter-only', result?.recipes?.length || 0)
      
      // Track filter usage if filters are active
      if (hasFilters) {
        analytics.trackFilterUsage(filters)
      }
      
      // Track search for recommendations
      RecommendationEngine.trackSearch(query, searchRequest)
    } catch (error) {
      console.error('Search failed:', error)
    }
  }, [query, filters, searchRecipes])

  // Auto-search when query or filters change
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      const hasQuery = query.trim()
      const hasFilters = filters.diet !== "Any" || 
                        filters.cuisine !== "Any" || 
                        filters.difficulty !== "Any" || 
                        filters.maxTime || 
                        filters.maxCalories ||
                        filters.maxProtein ||
                        filters.maxCarbs
      
      if (hasQuery || hasFilters) {
        performSearch()
      } else {
        setHasSearched(false)
      }
    }, 500) // Debounce search

    return () => clearTimeout(timeoutId)
  }, [query, filters, performSearch])

  // Use search results if we've searched, otherwise use default recipes
  const displayRecipes = hasSearched ? searchResults : defaultRecipes
  const isLoading = hasSearched ? loading : defaultLoading
  const displayError = hasSearched ? error : defaultError

  return (
    <main className="mx-auto max-w-6xl px-4 py-8">
      <h1 className="mb-4 text-2xl font-semibold">Search & Generate</h1>
      <div className="mb-4 inline-flex rounded-md border bg-background p-1 text-sm">
        <button
          type="button"
          onClick={() => setMode("text")}
          className={`rounded px-3 py-1 ${mode === "text" ? "bg-primary text-primary-foreground" : ""}`}
          aria-pressed={mode === "text"}
        >
          Text
        </button>
        <button
          type="button"
          onClick={() => setMode("image")}
          className={`rounded px-3 py-1 ${mode === "image" ? "bg-primary text-primary-foreground" : ""}`}
          aria-pressed={mode === "image"}
        >
          Image
        </button>
      </div>

      {mode === "text" ? (
        <>
          <SearchBar
            onSearch={(q) => {
              setQuery(q)
              setChips([])
            }}
          />
          <div className="mt-4">
            <FilterBar onChange={setFilters} />
          </div>
        </>
      ) : (
        <>
          <ImageIngredientUploader
            onResult={(ings) => {
              const q = ings.join(", ")
              setChips(ings)
              setQuery(q)
              setMode("text")
            }}
            endpoint={`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/ingredients/recognize-image`}
          />
          {chips.length > 0 && (
            <div className="mt-3 flex flex-wrap gap-2">
              {chips.map((c) => (
                <span key={c} className="rounded-full border px-2 py-0.5 text-xs">
                  {c}
                </span>
              ))}
            </div>
          )}
          <div className="mt-4">
            <FilterBar onChange={setFilters} />
          </div>
        </>
      )}

      {/* Loading State */}
      {isLoading && (
        <div className="mt-6 flex items-center justify-center py-12">
          <div className="flex items-center gap-2">
            <Loader2 className="h-5 w-5 animate-spin" />
            <span className="text-sm text-muted-foreground">
              {hasSearched ? 'Searching recipes...' : 'Loading recipes...'}
            </span>
          </div>
        </div>
      )}

      {/* Error State */}
      {displayError && (
        <div className="mt-6 space-y-4">
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>
              {hasSearched ? 'Search failed' : 'Failed to load recipes'}: {displayError}
            </AlertDescription>
          </Alert>
          <Button onClick={refetch} variant="outline" size="sm">
            Try Again
          </Button>
        </div>
      )}

      {/* Results */}
      {!isLoading && !displayError && (
        <div className="mt-6">
          {hasSearched && query && (
            <div className="mb-4 text-sm text-muted-foreground">
              Found {displayRecipes.length} recipes for "{query}"
            </div>
          )}
          {hasSearched && recipeMatches.length > 0 ? (
            <RecipeListWithMatch recipeMatches={recipeMatches} />
          ) : (
            <RecipeList recipes={displayRecipes} />
          )}
        </div>
      )}
    </main>
  )
}
