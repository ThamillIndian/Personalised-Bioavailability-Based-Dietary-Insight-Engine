"use client"

import { Button } from "@/components/ui/button"
import { useSavedRecipes } from "@/lib/use-saved-recipes"

export function SaveRecipeButton({ recipeId }: { recipeId: string }) {
  const { isSaved, toggle } = useSavedRecipes()
  const saved = isSaved(recipeId)

  async function commitMeta() {
    if (typeof window === "undefined") return
    try {
      const ratingRaw = window.localStorage.getItem(`srgr:rating:${recipeId}`)
      const subsRaw = window.localStorage.getItem(`srgr:subs:${recipeId}`)
      const rating = ratingRaw ? Number(ratingRaw) : null
      let substitutions: unknown = null
      try {
        substitutions = subsRaw ? JSON.parse(subsRaw) : null
      } catch {
        substitutions = null
      }

      const payload = {
        recipeId,
        rating,
        substitutions,
        savedAt: new Date().toISOString(),
      }

      // save combined meta locally so My Collection or backend sync can read it
      window.localStorage.setItem(`srgr:meta:${recipeId}`, JSON.stringify(payload))

      // optional webhook to your backend to consume both rating + substitutions together
      const webhook = process.env.NEXT_PUBLIC_RECIPE_META_URL
      if (webhook) {
        await fetch(webhook, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        })
      }
    } catch (e) {
      console.log("[v0] commitMeta error:", (e as Error).message)
    }
  }

  return (
    <Button
      variant={saved ? "secondary" : "default"}
      onClick={async () => {
        const nextSaved = !saved
        toggle(recipeId)
        if (nextSaved) {
          await commitMeta()
        }
      }}
      aria-pressed={saved}
    >
      {saved ? "Added to favourite" : "Add to favourite"}
    </Button>
  )
}
