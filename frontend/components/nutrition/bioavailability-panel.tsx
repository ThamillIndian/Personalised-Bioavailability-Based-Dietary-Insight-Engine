"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetFooter, SheetDescription } from "@/components/ui/sheet"
import { ScrollArea } from "@/components/ui/scroll-area"
import type { StressLevel, CookingMethod } from "@/lib/api"

type BioavailabilityPanelProps = {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSubmit: (values: {
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
  }) => Promise<void> | void
}

export function BioavailabilityPanel({ open, onOpenChange, onSubmit }: BioavailabilityPanelProps) {
  const [age, setAge] = useState(28)
  const [weight, setWeight] = useState(70)
  const [height, setHeight] = useState(175)
  const [stress, setStress] = useState<StressLevel>("low")
  const [method, setMethod] = useState<CookingMethod>("Boiled")
  const [postWorkout, setPostWorkout] = useState(false)

  // Optional fields
  const [sleep, setSleep] = useState<number | undefined>(7)
  const [mealTime, setMealTime] = useState<string | undefined>("Lunch")
  const [sinceLast, setSinceLast] = useState<number | undefined>(180)
  const [hydration, setHydration] = useState<number | undefined>(1.5)
  const [caffeine, setCaffeine] = useState<number | undefined>(0)
  const [menstrualPhase, setMenstrualPhase] = useState<string | undefined>(undefined)

  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async () => {
    setIsSubmitting(true)
    try {
      await onSubmit({
        age,
        weight_kg: weight,
        height_cm: height,
        stress_level: stress,
        cooking_method: method,
        post_workout: postWorkout,
        sleep_hours: sleep,
        meal_time: mealTime,
        time_since_last_meal_min: sinceLast,
        hydration_liters: hydration,
        caffeine_mg: caffeine,
        menstrual_phase: menstrualPhase,
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  const cookingMethods: CookingMethod[] = [
    "Raw",
    "Boiled",
    "Steamed",
    "Fried",
    "Baked",
    "Sauteed",
    "Pressure Cooked",
  ]

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent side="right" className="w-[420px] sm:w-[480px] flex flex-col h-full">
        <SheetHeader className="flex-shrink-0">
          <SheetTitle>Bioavailability Context</SheetTitle>
          <SheetDescription>
            Enter your details to calculate nutrient bioavailability for this recipe
          </SheetDescription>
        </SheetHeader>

        <ScrollArea className="flex-1 min-h-0 -mx-1 px-1">
          <div className="space-y-4 px-1 py-2">
            {/* Basic Info */}
            <div className="space-y-2">
              <Label className="text-sm font-medium">Basic Information</Label>
              <div className="grid grid-cols-3 gap-2">
                <div className="space-y-1.5">
                  <Label htmlFor="age" className="text-xs text-muted-foreground">Age</Label>
                  <Input
                    id="age"
                    type="number"
                    min="1"
                    max="120"
                    value={age}
                    onChange={(e) => setAge(Number(e.target.value))}
                    placeholder="28"
                  />
                </div>
                <div className="space-y-1.5">
                  <Label htmlFor="weight" className="text-xs text-muted-foreground">Weight (kg)</Label>
                  <Input
                    id="weight"
                    type="number"
                    min="1"
                    step="0.1"
                    value={weight}
                    onChange={(e) => setWeight(Number(e.target.value))}
                    placeholder="70"
                  />
                </div>
                <div className="space-y-1.5">
                  <Label htmlFor="height" className="text-xs text-muted-foreground">Height (cm)</Label>
                  <Input
                    id="height"
                    type="number"
                    min="50"
                    step="1"
                    value={height}
                    onChange={(e) => setHeight(Number(e.target.value))}
                    placeholder="175"
                  />
                </div>
              </div>
            </div>

            {/* Stress & Cooking Method */}
            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-1.5">
                <Label htmlFor="stress" className="text-sm font-medium">Stress Level</Label>
                <Select value={stress} onValueChange={(v) => setStress(v as StressLevel)}>
                  <SelectTrigger id="stress">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="low">Low</SelectItem>
                    <SelectItem value="medium">Medium</SelectItem>
                    <SelectItem value="high">High</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-1.5">
                <Label htmlFor="cooking-method" className="text-sm font-medium">Cooking Method</Label>
                <Select value={method} onValueChange={(v) => setMethod(v as CookingMethod)}>
                  <SelectTrigger id="cooking-method">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {cookingMethods.map((m) => (
                      <SelectItem key={m} value={m}>
                        {m}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            {/* Post-workout toggle */}
            <div className="space-y-1.5">
              <Label className="text-sm font-medium">Activity Status</Label>
              <Button
                type="button"
                variant={postWorkout ? "default" : "outline"}
                className="w-full"
                onClick={() => setPostWorkout(!postWorkout)}
              >
                {postWorkout ? "✓ Post-workout" : "Not post-workout"}
              </Button>
            </div>

            {/* Optional Fields */}
            <div className="space-y-3">
              <Label className="text-sm font-medium">Lifestyle Factors (Optional)</Label>
              
              <div className="grid grid-cols-2 gap-3">
                <div className="space-y-1.5">
                  <Label htmlFor="sleep" className="text-xs text-muted-foreground">Sleep (hours)</Label>
                  <Input
                    id="sleep"
                    type="number"
                    min="0"
                    max="24"
                    step="0.5"
                    value={sleep ?? ""}
                    onChange={(e) => setSleep(e.target.value ? Number(e.target.value) : undefined)}
                    placeholder="7"
                  />
                </div>
                <div className="space-y-1.5">
                  <Label htmlFor="meal-time" className="text-xs text-muted-foreground">Meal Time</Label>
                  <Input
                    id="meal-time"
                    type="text"
                    value={mealTime ?? ""}
                    onChange={(e) => setMealTime(e.target.value || undefined)}
                    placeholder="Lunch"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="space-y-1.5">
                  <Label htmlFor="time-since-last" className="text-xs text-muted-foreground">
                    Mins Since Last Meal
                  </Label>
                  <Input
                    id="time-since-last"
                    type="number"
                    min="0"
                    value={sinceLast ?? ""}
                    onChange={(e) => setSinceLast(e.target.value ? Number(e.target.value) : undefined)}
                    placeholder="180"
                  />
                </div>
                <div className="space-y-1.5">
                  <Label htmlFor="hydration" className="text-xs text-muted-foreground">Hydration (L)</Label>
                  <Input
                    id="hydration"
                    type="number"
                    min="0"
                    step="0.1"
                    value={hydration ?? ""}
                    onChange={(e) => setHydration(e.target.value ? Number(e.target.value) : undefined)}
                    placeholder="1.5"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="space-y-1.5">
                  <Label htmlFor="caffeine" className="text-xs text-muted-foreground">Caffeine (mg)</Label>
                  <Input
                    id="caffeine"
                    type="number"
                    min="0"
                    value={caffeine ?? ""}
                    onChange={(e) => setCaffeine(e.target.value ? Number(e.target.value) : undefined)}
                    placeholder="0"
                  />
                </div>
                <div className="space-y-1.5">
                  <Label htmlFor="menstrual-phase" className="text-xs text-muted-foreground">
                    Menstrual Phase
                  </Label>
                  <Input
                    id="menstrual-phase"
                    type="text"
                    value={menstrualPhase ?? ""}
                    onChange={(e) => setMenstrualPhase(e.target.value || undefined)}
                    placeholder="None"
                  />
                </div>
              </div>
            </div>
          </div>
        </ScrollArea>

        <SheetFooter className="flex-shrink-0 gap-2 border-t pt-4 mt-4">
          <Button
            variant="outline"
            onClick={() => onOpenChange(false)}
            disabled={isSubmitting}
            className="flex-1"
          >
            Cancel
          </Button>
          <Button
            onClick={handleSubmit}
            disabled={isSubmitting}
            className="flex-1"
          >
            {isSubmitting ? "Computing..." : "Apply & Compute"}
          </Button>
        </SheetFooter>
      </SheetContent>
    </Sheet>
  )
}

