"use client"

import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

const diets = ["Any", "Vegetarian", "Vegan", "Pescatarian", "Gluten-Free", "High-Protein", "Low-Carb"]
const cuisines = ["Any", "Italian", "Indian", "Mexican", "Japanese", "Thai", "Chinese", "Greek", "French", "American", "Mediterranean", "Middle Eastern", "Hawaiian"]
const difficulties = ["Any", "Easy", "Medium", "Hard"]

export type Filters = {
  diet: string
  cuisine?: string
  difficulty?: string
  maxTime?: number
  maxCalories?: number
  maxProtein?: number
  maxCarbs?: number
}

export function FilterBar({
  onChange,
}: {
  onChange: (f: Filters) => void
}) {
  const [diet, setDiet] = useState<string>("Any")
  const [cuisine, setCuisine] = useState<string>("Any")
  const [difficulty, setDifficulty] = useState<string>("Any")
  const [maxTime, setMaxTime] = useState<string>("")
  const [maxCalories, setMaxCalories] = useState<string>("")
  const [maxProtein, setMaxProtein] = useState<string>("")
  const [maxCarbs, setMaxCarbs] = useState<string>("")

  const updateFilters = (updates: Partial<Filters>) => {
    const newFilters: Filters = {
      diet,
      cuisine,
      difficulty,
      maxTime: maxTime ? Number(maxTime) : undefined,
      maxCalories: maxCalories ? Number(maxCalories) : undefined,
      maxProtein: maxProtein ? Number(maxProtein) : undefined,
      maxCarbs: maxCarbs ? Number(maxCarbs) : undefined,
      ...updates
    }
    onChange(newFilters)
  }

  return (
    <div className="space-y-4">
      {/* Basic Filters */}
      <div className="grid gap-3 rounded-lg border p-4 md:grid-cols-4">
        <div className="space-y-1">
          <Label htmlFor="diet">Diet</Label>
          <Select
            value={diet}
            onValueChange={(v) => {
              setDiet(v)
              updateFilters({ diet: v })
            }}
          >
            <SelectTrigger id="diet" aria-label="Diet filter">
              <SelectValue placeholder="Select diet" />
            </SelectTrigger>
            <SelectContent>
              {diets.map((d) => (
                <SelectItem key={d} value={d}>
                  {d}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        
        <div className="space-y-1">
          <Label htmlFor="cuisine">Cuisine</Label>
          <Select
            value={cuisine}
            onValueChange={(v) => {
              setCuisine(v)
              updateFilters({ cuisine: v })
            }}
          >
            <SelectTrigger id="cuisine" aria-label="Cuisine filter">
              <SelectValue placeholder="Select cuisine" />
            </SelectTrigger>
            <SelectContent>
              {cuisines.map((c) => (
                <SelectItem key={c} value={c}>
                  {c}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-1">
          <Label htmlFor="difficulty">Difficulty</Label>
          <Select
            value={difficulty}
            onValueChange={(v) => {
              setDifficulty(v)
              updateFilters({ difficulty: v })
            }}
          >
            <SelectTrigger id="difficulty" aria-label="Difficulty filter">
              <SelectValue placeholder="Select difficulty" />
            </SelectTrigger>
            <SelectContent>
              {difficulties.map((d) => (
                <SelectItem key={d} value={d}>
                  {d}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-1">
          <Label htmlFor="time">Max Time (min)</Label>
          <Input
            id="time"
            inputMode="numeric"
            placeholder="e.g. 20"
            value={maxTime}
            onChange={(e) => {
              const v = e.target.value
              setMaxTime(v)
              updateFilters({ maxTime: v ? Number(v) : undefined })
            }}
          />
        </div>
      </div>

      {/* Nutritional Filters */}
      <div className="grid gap-3 rounded-lg border p-4 md:grid-cols-3">
        <div className="space-y-1">
          <Label htmlFor="calories">Max Calories</Label>
          <Input
            id="calories"
            inputMode="numeric"
            placeholder="e.g. 500"
            value={maxCalories}
            onChange={(e) => {
              const v = e.target.value
              setMaxCalories(v)
              updateFilters({ maxCalories: v ? Number(v) : undefined })
            }}
          />
        </div>
        
        <div className="space-y-1">
          <Label htmlFor="protein">Min Protein (g)</Label>
          <Input
            id="protein"
            inputMode="numeric"
            placeholder="e.g. 20"
            value={maxProtein}
            onChange={(e) => {
              const v = e.target.value
              setMaxProtein(v)
              updateFilters({ maxProtein: v ? Number(v) : undefined })
            }}
          />
        </div>

        <div className="space-y-1">
          <Label htmlFor="carbs">Max Carbs (g)</Label>
          <Input
            id="carbs"
            inputMode="numeric"
            placeholder="e.g. 50"
            value={maxCarbs}
            onChange={(e) => {
              const v = e.target.value
              setMaxCarbs(v)
              updateFilters({ maxCarbs: v ? Number(v) : undefined })
            }}
          />
        </div>
      </div>
    </div>
  )
}
