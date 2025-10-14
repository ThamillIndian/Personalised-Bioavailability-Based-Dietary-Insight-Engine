"use client"

import { useCallback, useEffect, useMemo, useRef, useState } from "react"

export function RatingWidget({
  recipeId,
  initialRating = 0,
  onRated,
  className,
  enableAutosave = true,
  showSaveButton = false,
}: {
  recipeId: string
  initialRating?: number
  onRated?: (rating: number) => void
  className?: string
  enableAutosave?: boolean
  showSaveButton?: boolean
}) {
  const storageKey = useMemo(() => `srgr:rating:${recipeId}`, [recipeId])
  const userIdKey = useMemo(() => `srgr:user_id`, [])
  const [rating, setRating] = useState<number>(() => {
    if (typeof window === "undefined") return initialRating
    const saved = window.localStorage.getItem(storageKey)
    return saved ? Number(saved) : initialRating
  })
  const [hover, setHover] = useState<number>(0)
  const [submitting, setSubmitting] = useState(false)
  const [lastSaved, setLastSaved] = useState<number | null>(null)
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false)
  const debounceRef = useRef<NodeJS.Timeout>()

  // Generate or retrieve user ID
  const getUserId = useCallback(() => {
    if (typeof window === "undefined") return "anonymous"
    let userId = window.localStorage.getItem(userIdKey)
    if (!userId) {
      userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
      window.localStorage.setItem(userIdKey, userId)
    }
    return userId
  }, [userIdKey])

  // Debounced save function
  const debouncedSave = useCallback((r: number) => {
    if (debounceRef.current) {
      clearTimeout(debounceRef.current)
    }
    
    debounceRef.current = setTimeout(async () => {
      await submit(r)
    }, enableAutosave ? 1000 : 0) // 1 second delay for autosave
  }, [enableAutosave])

  // Save rating to localStorage immediately
  useEffect(() => {
    if (typeof window !== "undefined") {
      window.localStorage.setItem(storageKey, String(rating))
      setHasUnsavedChanges(rating !== lastSaved)
    }
  }, [rating, storageKey, lastSaved])

  async function submit(r: number) {
    setSubmitting(true)
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
      const response = await fetch(`${apiUrl}/api/v1/favorites/ratings`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          recipe_id: recipeId,
          user_id: getUserId(),
          rating: r,
          review: null
        }),
      })

      if (response.ok) {
        const result = await response.json()
        setLastSaved(r)
        setHasUnsavedChanges(false)
        console.log("✅ Rating saved:", result)
        onRated?.(r)
      } else {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }
    } catch (e) {
      console.error("❌ Rating submit error:", (e as Error).message)
      // Show error to user but don't reset rating
    } finally {
      setSubmitting(false)
    }
  }

  const handleRatingClick = (n: number) => {
    setRating(n)
    if (enableAutosave) {
      debouncedSave(n)
    } else {
      setHasUnsavedChanges(true)
    }
  }

  const handleSaveClick = async () => {
    if (hasUnsavedChanges) {
      await submit(rating)
    }
  }

  // Cleanup debounce on unmount
  useEffect(() => {
    return () => {
      if (debounceRef.current) {
        clearTimeout(debounceRef.current)
      }
    }
  }, [])

  return (
    <section className={className} aria-label="Rate this recipe">
      <div className="mb-2 text-sm font-medium">Rate This Recipe</div>
      <div className="flex items-center gap-1">
        {[1, 2, 3, 4, 5].map((n) => {
          const active = (hover || rating) >= n
          return (
            <button
              key={n}
              aria-label={`Rate ${n} star${n > 1 ? "s" : ""}`}
              onMouseEnter={() => setHover(n)}
              onMouseLeave={() => setHover(0)}
              onClick={() => handleRatingClick(n)}
              className={`h-6 w-6 rounded transition-colors ${
                active ? "text-yellow-500" : "text-muted-foreground hover:text-yellow-400"
              }`}
              title={`${n} star${n > 1 ? "s" : ""}`}
              disabled={submitting}
            >
              {"★"}
            </button>
          )
        })}
        <span className="ml-2 text-sm text-muted-foreground">
          {submitting ? "Saving..." : rating ? `${rating.toFixed(1)}` : "No rating yet"}
        </span>
        {hasUnsavedChanges && !enableAutosave && (
          <span className="ml-2 text-xs text-orange-500">• Unsaved</span>
        )}
      </div>
      
      {showSaveButton && hasUnsavedChanges && !enableAutosave && (
        <button
          onClick={handleSaveClick}
          disabled={submitting}
          className="mt-2 rounded bg-blue-600 px-3 py-1 text-xs text-white hover:bg-blue-700 disabled:opacity-50"
        >
          {submitting ? "Saving..." : "Save Rating"}
        </button>
      )}
      
      {enableAutosave && hasUnsavedChanges && (
        <div className="mt-1 text-xs text-blue-600">
          Auto-saving in a moment...
        </div>
      )}
    </section>
  )
}
