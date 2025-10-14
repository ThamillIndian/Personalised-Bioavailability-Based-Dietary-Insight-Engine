"use client"

import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"

export function SearchBar({
  onSearch,
  suggested = ["chicken", "vegan", "pasta", "quick"],
}: {
  onSearch: (q: string) => void
  suggested?: string[]
}) {
  const [q, setQ] = useState("")

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-2">
        <Input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Describe ingredients, diets, or a dish..."
          aria-label="Search recipes"
        />
        <Button onClick={() => onSearch(q)}>Search</Button>
      </div>
      <div className="flex flex-wrap items-center gap-2">
        <span className="text-xs text-foreground/60">Try:</span>
        {suggested.map((s) => (
          <button
            key={s}
            onClick={() => {
              setQ(s)
              onSearch(s)
            }}
            className="focus-visible:outline-ring/50 focus-visible:ring-2"
            aria-label={`Search ${s}`}
          >
            <Badge variant="secondary" className="cursor-pointer">
              {s}
            </Badge>
          </button>
        ))}
      </div>
    </div>
  )
}
