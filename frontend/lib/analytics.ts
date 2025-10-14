/**
 * Analytics and User Behavior Tracking
 * Tracks user interactions for insights and improvements
 */

interface AnalyticsEvent {
  event: string
  timestamp: number
  data?: Record<string, any>
}

interface PageView {
  path: string
  timestamp: number
  duration?: number
}

interface AnalyticsData {
  events: AnalyticsEvent[]
  pageViews: PageView[]
  sessionStart: number
  lastActivity: number
}

class Analytics {
  private static STORAGE_KEY = 'srgr:analytics'
  private static SESSION_TIMEOUT = 30 * 60 * 1000 // 30 minutes
  private currentPageStart: number = Date.now()
  private currentPath: string = ''

  /**
   * Get analytics data from localStorage
   */
  private getData(): AnalyticsData {
    if (typeof window === 'undefined') {
      return this.getEmptyData()
    }

    const stored = localStorage.getItem(Analytics.STORAGE_KEY)
    if (!stored) {
      return this.getEmptyData()
    }

    try {
      const data = JSON.parse(stored)
      
      // Check if session expired
      if (Date.now() - data.lastActivity > Analytics.SESSION_TIMEOUT) {
        return this.getEmptyData()
      }
      
      return data
    } catch {
      return this.getEmptyData()
    }
  }

  /**
   * Get empty analytics data structure
   */
  private getEmptyData(): AnalyticsData {
    return {
      events: [],
      pageViews: [],
      sessionStart: Date.now(),
      lastActivity: Date.now()
    }
  }

  /**
   * Save analytics data to localStorage
   */
  private saveData(data: AnalyticsData) {
    if (typeof window === 'undefined') return
    
    // Keep only last 100 events and 50 page views to prevent storage bloat
    const trimmedData = {
      ...data,
      events: data.events.slice(-100),
      pageViews: data.pageViews.slice(-50),
      lastActivity: Date.now()
    }
    
    localStorage.setItem(Analytics.STORAGE_KEY, JSON.stringify(trimmedData))
  }

  /**
   * Track a custom event
   */
  trackEvent(event: string, data?: Record<string, any>) {
    const analyticsData = this.getData()
    
    analyticsData.events.push({
      event,
      timestamp: Date.now(),
      data
    })
    
    this.saveData(analyticsData)
    
    if (process.env.NODE_ENV === 'development') {
      console.log('📊 Analytics Event:', event, data)
    }
  }

  /**
   * Track a page view
   */
  trackPageView(path: string) {
    const analyticsData = this.getData()
    
    // Save duration of previous page
    if (this.currentPath && this.currentPageStart) {
      const duration = Date.now() - this.currentPageStart
      const lastPageView = analyticsData.pageViews.find(pv => pv.path === this.currentPath && !pv.duration)
      if (lastPageView) {
        lastPageView.duration = duration
      }
    }
    
    // Track new page view
    analyticsData.pageViews.push({
      path,
      timestamp: Date.now()
    })
    
    this.currentPath = path
    this.currentPageStart = Date.now()
    
    this.saveData(analyticsData)
    
    if (process.env.NODE_ENV === 'development') {
      console.log('📊 Page View:', path)
    }
  }

  /**
   * Track search query
   */
  trackSearch(query: string, results: number) {
    this.trackEvent('search', { query, results })
  }

  /**
   * Track recipe view
   */
  trackRecipeView(recipeId: string, recipeTitle: string) {
    this.trackEvent('recipe_view', { recipeId, recipeTitle })
  }

  /**
   * Track recipe save/favorite
   */
  trackRecipeSave(recipeId: string, action: 'save' | 'unsave') {
    this.trackEvent('recipe_save', { recipeId, action })
  }

  /**
   * Track recipe rating
   */
  trackRecipeRating(recipeId: string, rating: number) {
    this.trackEvent('recipe_rating', { recipeId, rating })
  }

  /**
   * Track filter usage
   */
  trackFilterUsage(filters: Record<string, any>) {
    this.trackEvent('filter_usage', filters)
  }

  /**
   * Track timer usage
   */
  trackTimerUsage(action: 'create' | 'start' | 'complete', duration?: number) {
    this.trackEvent('timer', { action, duration })
  }

  /**
   * Track shopping list usage
   */
  trackShoppingList(action: 'add' | 'remove' | 'export' | 'share', itemCount?: number) {
    this.trackEvent('shopping_list', { action, itemCount })
  }

  /**
   * Track chatbot usage
   */
  trackChatbot(action: 'open' | 'close' | 'message' | 'quick_question') {
    this.trackEvent('chatbot', { action })
  }

  /**
   * Get session insights
   */
  getSessionInsights() {
    const data = this.getData()
    const now = Date.now()
    const sessionDuration = now - data.sessionStart
    
    return {
      sessionDuration,
      totalEvents: data.events.length,
      totalPageViews: data.pageViews.length,
      mostVisitedPages: this.getMostVisitedPages(data.pageViews),
      topEvents: this.getTopEvents(data.events),
      averagePageDuration: this.getAveragePageDuration(data.pageViews)
    }
  }

  /**
   * Get most visited pages
   */
  private getMostVisitedPages(pageViews: PageView[]) {
    const counts: Record<string, number> = {}
    pageViews.forEach(pv => {
      counts[pv.path] = (counts[pv.path] || 0) + 1
    })
    return Object.entries(counts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([path, count]) => ({ path, count }))
  }

  /**
   * Get top events
   */
  private getTopEvents(events: AnalyticsEvent[]) {
    const counts: Record<string, number> = {}
    events.forEach(event => {
      counts[event.event] = (counts[event.event] || 0) + 1
    })
    return Object.entries(counts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([event, count]) => ({ event, count }))
  }

  /**
   * Get average page duration
   */
  private getAveragePageDuration(pageViews: PageView[]) {
    const durations = pageViews.filter(pv => pv.duration).map(pv => pv.duration!)
    if (durations.length === 0) return 0
    return Math.round(durations.reduce((a, b) => a + b, 0) / durations.length)
  }

  /**
   * Clear analytics data
   */
  clearData() {
    if (typeof window === 'undefined') return
    localStorage.removeItem(Analytics.STORAGE_KEY)
  }
}

export const analytics = new Analytics()
