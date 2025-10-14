"use client"

import { useMemo, useState } from "react"
import { Button } from "@/components/ui/button"

type SubOption = {
  name: string
  ratio?: string
  note?: string
}

type SubResponse = {
  ingredient: string
  options: SubOption[]
}

export function SubstitutionsPanel({
  recipeId,
  ingredients,
  className,
}: {
  recipeId: string
  ingredients?: string[]
  className?: string
}) {
  const [open, setOpen] = useState(false)
  const [loading, setLoading] = useState(false)
  const [data, setData] = useState<SubResponse[] | null>(null)

  const hasIngredients = (ingredients?.length ?? 0) > 0

  // Demo substitutions if no backend is configured
  const demoSubstitutions = useMemo<SubResponse[]>(() => {
    const pool: Record<string, SubOption[]> = {
      butter: [
        { name: "Coconut Oil", ratio: "1:1", note: "Best for baking" },
        { name: "Applesauce", ratio: "1:1", note: "Low‑fat option" },
        { name: "Margarine", ratio: "1:1", note: "Direct replacement" },
      ],
      egg: [
        { name: "Flax Egg", ratio: "1 tbsp flax + 3 tbsp water", note: "Binding" },
        { name: "Chia Egg", ratio: "1 tbsp chia + 3 tbsp water", note: "Binding" },
        { name: "Unsweetened Yogurt", ratio: "1/4 cup", note: "Moisture" },
      ],
      milk: [
        { name: "Oat Milk", ratio: "1:1", note: "Neutral flavor" },
        { name: "Almond Milk", ratio: "1:1", note: "Light, nutty" },
        { name: "Evaporated Milk + Water", ratio: "1:1", note: "Richer body" },
      ],
    }
    const ing = (ingredients ?? []).map((s) => s.toLowerCase())
    const uniq = Array.from(new Set(ing))
    return uniq.slice(0, 5).map((ingName) => ({
      ingredient: ingName,
      options: pool[ingName] ?? [
        { name: "Yogurt", ratio: "1:1", note: "Adds moisture" },
        { name: "Silken Tofu", ratio: "1:1", note: "Neutral, protein" },
      ],
    }))
  }, [ingredients])

  async function fetchSubs() {
    setLoading(true)
    try {
      const url = process.env.NEXT_PUBLIC_SUBSTITUTIONS_API_URL
      if (url && hasIngredients) {
        const res = await fetch(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ recipeId, ingredients }),
        })
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        const json = (await res.json()) as { substitutions: SubResponse[] }
        setData(json.substitutions ?? [])
        if (typeof window !== "undefined") {
          window.localStorage.setItem(`srgr:subs:${recipeId}`, JSON.stringify(json.substitutions ?? []))
        }
      } else {
        setData(demoSubstitutions)
        if (typeof window !== "undefined") {
          window.localStorage.setItem(`srgr:subs:${recipeId}`, JSON.stringify(demoSubstitutions))
        }
      }
      setOpen(true)
    } catch (e) {
      console.log("[v0] substitutions fetch error:", (e as Error).message)
      setData(demoSubstitutions)
      if (typeof window !== "undefined") {
        window.localStorage.setItem(`srgr:subs:${recipeId}`, JSON.stringify(demoSubstitutions))
      }
      setOpen(true)
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className={className}>
      <div className="mb-2 flex items-center gap-2">
        <span className="font-medium">Ingredient Substitutions</span>
        {!open ? (
          <Button size="sm" onClick={fetchSubs} disabled={loading || !hasIngredients}>
            {loading ? "Generating..." : "Generate Substitutions"}
          </Button>
        ) : (
          <Button size="sm" variant="secondary" onClick={() => setOpen(false)}>
            Hide Substitutions
          </Button>
        )}
      </div>

      {open && (
        <div className="rounded-md border p-3 space-y-2">
          {(data ?? demoSubstitutions).map((row) => (
            <div key={row.ingredient} className="rounded-md border p-2">
              <div className="text-sm font-semibold mb-1">{row.ingredient}</div>
              <ul className="space-y-1">
                {row.options.map((opt, i) => (
                  <li key={i} className="text-sm leading-6">
                    <span className="font-medium">{opt.name}</span>
                    {opt.ratio ? <span className="ml-1 text-muted-foreground">({opt.ratio})</span> : null}
                    {opt.note ? <div className="text-muted-foreground">{opt.note}</div> : null}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}

      {!hasIngredients && (
        <p className="mt-2 text-sm text-muted-foreground">Add ingredients to this recipe to enable substitutions.</p>
      )}
    </section>
  )
}
