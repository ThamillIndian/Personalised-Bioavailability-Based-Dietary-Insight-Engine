/**
 * Simple in-memory cache for API responses
 */

interface CacheEntry<T> {
  data: T
  timestamp: number
  expiresIn: number
}

class Cache {
  private cache: Map<string, CacheEntry<any>> = new Map()
  
  set<T>(key: string, data: T, expiresIn: number = 5 * 60 * 1000) {
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      expiresIn
    })
  }

  get<T>(key: string): T | null {
    const entry = this.cache.get(key)
    
    if (!entry) {
      return null
    }

    const isExpired = Date.now() - entry.timestamp > entry.expiresIn
    
    if (isExpired) {
      this.cache.delete(key)
      return null
    }

    return entry.data as T
  }

  has(key: string): boolean {
    const entry = this.cache.get(key)
    
    if (!entry) {
      return false
    }

    const isExpired = Date.now() - entry.timestamp > entry.expiresIn
    
    if (isExpired) {
      this.cache.delete(key)
      return false
    }

    return true
  }

  delete(key: string): void {
    this.cache.delete(key)
  }

  clear(): void {
    this.cache.clear()
  }

  // Clear expired entries
  cleanup(): void {
    const now = Date.now()
    const keysToDelete: string[] = []

    this.cache.forEach((entry, key) => {
      if (now - entry.timestamp > entry.expiresIn) {
        keysToDelete.push(key)
      }
    })

    keysToDelete.forEach(key => this.cache.delete(key))
  }
}

export const cache = new Cache()

// Run cleanup every 5 minutes
if (typeof window !== 'undefined') {
  setInterval(() => {
    cache.cleanup()
  }, 5 * 60 * 1000)
}
