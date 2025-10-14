"use client"

import type React from "react"

import { useCallback, useRef, useState } from "react"

type Props = {
  // Called with the list of extracted ingredients when the request succeeds
  onResult: (ingredients: string[]) => void
  // Optional: pass your backend endpoint (NEXT_PUBLIC_INGREDIENTS_API_URL recommended)
  endpoint?: string
}

export function ImageIngredientUploader({ onResult, endpoint }: Props) {
  const [file, setFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  const onFiles = useCallback((files: FileList | null) => {
    if (!files || !files.length) return
    const f = files[0]
    if (!f.type.startsWith("image/")) {
      setError("Please select an image file.")
      return
    }
    setError(null)
    setFile(f)
    setPreviewUrl(URL.createObjectURL(f))
  }, [])

  const onDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault()
      onFiles(e.dataTransfer.files)
    },
    [onFiles],
  )

  const onBrowseClick = () => inputRef.current?.click()

  const extract = async () => {
    if (!file) {
      setError("Please select an image first.")
      return
    }
    setLoading(true)
    setError(null)
    try {
      const url = endpoint || `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/ingredients/recognize-image`
      console.log('🔍 Uploading to:', url)
      console.log('📁 File:', file.name, file.size, file.type)
      
      const form = new FormData()
      form.append("file", file)
      
      const res = await fetch(url, {
        method: "POST",
        body: form,
      })
      
      console.log('📡 Response status:', res.status, res.statusText)
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}))
        throw new Error(`Request failed: ${res.status} - ${errorData.message || res.statusText}`)
      }
      const data = await res.json()
      console.log('📦 Response data:', data)
      
      // Parse the response based on the backend API structure
      let ingredients: string[] = []
      if (data.success && Array.isArray(data.ingredients)) {
        ingredients = data.ingredients.map((ing: any) => {
          // Backend returns RecognizedIngredient objects with name, confidence, etc.
          return ing.name || ing
        })
      } else if (Array.isArray(data.ingredients)) {
        ingredients = data.ingredients.map((ing: any) => ing.name || ing)
      } else if (Array.isArray(data)) {
        ingredients = data.map((ing: any) => ing.name || ing)
      }
      
      if (!ingredients.length) {
        throw new Error("No ingredients found in the image.")
      }
      
      onResult(ingredients)
    } catch (err: any) {
      setError(err?.message || "Something went wrong while extracting ingredients.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <section aria-label="Upload image to extract ingredients" className="rounded-lg border bg-background p-4">
      <div
        onDragOver={(e) => e.preventDefault()}
        onDrop={onDrop}
        className="flex flex-col items-center justify-center rounded-md border border-dashed p-6 text-center"
        role="button"
        tabIndex={0}
        onKeyDown={(e) => {
          if (e.key === "Enter") onBrowseClick()
        }}
        aria-label="Drop image here or browse files"
      >
        {previewUrl ? (
          <div className="flex w-full items-start gap-4">
            <div className="aspect-square h-16 w-16 overflow-hidden rounded-md border">
              {/* Using a simple img tag is fine for object URLs */}
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={previewUrl || "/placeholder.svg"}
                alt="Selected image preview"
                className="h-full w-full object-cover"
              />
            </div>
            <div className="flex-1 text-left">
              <p className="font-medium">Image ready</p>
              <p className="text-sm text-muted-foreground">Click Extract to detect ingredients from this image.</p>
              <div className="mt-2 flex gap-2">
                <button
                  type="button"
                  className="rounded-md border px-3 py-1 text-sm"
                  onClick={() => {
                    setFile(null)
                    setPreviewUrl(null)
                    setError(null)
                  }}
                >
                  Remove
                </button>
                <button
                  type="button"
                  className="rounded-md bg-primary px-3 py-1 text-sm text-primary-foreground"
                  onClick={extract}
                  disabled={loading}
                >
                  {loading ? "Extracting..." : "Extract ingredients"}
                </button>
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-2">
            <p className="font-medium">Drop a recipe photo here</p>
            <p className="text-sm text-muted-foreground">or</p>
            <button type="button" className="rounded-md border px-3 py-1 text-sm" onClick={onBrowseClick}>
              Browse files
            </button>
            <input
              ref={inputRef}
              type="file"
              accept="image/*"
              className="sr-only"
              onChange={(e) => onFiles(e.target.files)}
            />
          </div>
        )}
      </div>

      {error && (
        <p className="mt-2 text-sm text-destructive" role="alert" aria-live="polite">
          {error}
        </p>
      )}
      {!error && loading && (
        <p className="mt-2 text-sm text-muted-foreground" aria-live="polite">
          Analyzing image…
        </p>
      )}
    </section>
  )
}
