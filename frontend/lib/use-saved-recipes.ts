"use client"

import { useState, useEffect, useCallback } from 'react'
import { favoritesApi } from '@/lib/api'

const KEY = "saved-recipes"
const USER_ID_KEY = "srgr:user_id"

// Generate or retrieve user ID
function getUserId(): string {
  if (typeof window === "undefined") return "anonymous"
  let userId = window.localStorage.getItem(USER_ID_KEY)
  if (!userId) {
    userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    window.localStorage.setItem(USER_ID_KEY, userId)
  }
  return userId
}

// Local storage fallback functions
function readSaved(): string[] {
  if (typeof window === "undefined") return []
  try {
    const raw = localStorage.getItem(KEY)
    return raw ? JSON.parse(raw) : []
  } catch {
    return []
  }
}

function writeSaved(ids: string[]) {
  if (typeof window === "undefined") return
  localStorage.setItem(KEY, JSON.stringify(ids))
}

export function useSavedRecipes() {
  const [savedIds, setSavedIds] = useState<string[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const userId = getUserId()

  const fetchSavedRecipes = useCallback(async () => {
    setLoading(true)
    setError(null)
    
    try {
      // Try to fetch from backend first
      const backendSavedIds = await favoritesApi.getUserFavorites(userId)
      setSavedIds(backendSavedIds)
      
      // Sync with localStorage as backup
      writeSaved(backendSavedIds)
    } catch (error) {
      console.warn('Failed to fetch from backend, using localStorage:', error)
      // Fallback to localStorage
      const localSavedIds = readSaved()
      setSavedIds(localSavedIds)
      setError('Using offline data. Sync when connection restored.')
    } finally {
      setLoading(false)
    }
  }, [userId])

  const toggle = useCallback(async (id: string) => {
    const isCurrentlySaved = savedIds.includes(id)
    
    try {
      if (isCurrentlySaved) {
        // Remove from favorites
        await favoritesApi.removeFavorite(id, userId)
        const newSavedIds = savedIds.filter((x) => x !== id)
        setSavedIds(newSavedIds)
        writeSaved(newSavedIds)
      } else {
        // Add to favorites
        await favoritesApi.addFavorite(id, userId)
        const newSavedIds = Array.from(new Set([...savedIds, id]))
        setSavedIds(newSavedIds)
        writeSaved(newSavedIds)
      }
    } catch (error) {
      console.error('Failed to toggle favorite:', error)
      // Fallback to localStorage only
      const localSavedIds = isCurrentlySaved 
        ? savedIds.filter((x) => x !== id)
        : Array.from(new Set([...savedIds, id]))
      
      setSavedIds(localSavedIds)
      writeSaved(localSavedIds)
      setError('Failed to sync with server. Changes saved locally.')
    }
  }, [savedIds, userId])

  const clear = useCallback(async () => {
    try {
      // Clear from backend (remove each favorite)
      await Promise.all(
        savedIds.map(id => favoritesApi.removeFavorite(id, userId))
      )
      setSavedIds([])
      writeSaved([])
    } catch (error) {
      console.error('Failed to clear favorites from backend:', error)
      // Fallback to localStorage only
      setSavedIds([])
      writeSaved([])
      setError('Failed to sync with server. Cleared locally.')
    }
  }, [savedIds, userId])

  const isSaved = useCallback((id: string) => savedIds.includes(id), [savedIds])

  const clearError = useCallback(() => {
    setError(null)
  }, [])

  useEffect(() => {
    fetchSavedRecipes()
  }, [fetchSavedRecipes])

  return { 
    savedIds, 
    isSaved, 
    toggle, 
    clear, 
    isLoading: loading,
    error,
    clearError,
    refetch: fetchSavedRecipes
  }
}
