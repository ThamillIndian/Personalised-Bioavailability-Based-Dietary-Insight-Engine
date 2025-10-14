"use client"

import { useRef, useState, ReactNode, TouchEvent } from 'react'
import { cn } from '@/lib/utils'

interface SwipeableProps {
  children: ReactNode
  onSwipeLeft?: () => void
  onSwipeRight?: () => void
  className?: string
  threshold?: number
}

export function Swipeable({
  children,
  onSwipeLeft,
  onSwipeRight,
  className,
  threshold = 50
}: SwipeableProps) {
  const [touchStart, setTouchStart] = useState(0)
  const [touchEnd, setTouchEnd] = useState(0)
  const [isSwiping, setIsSwiping] = useState(false)
  const elementRef = useRef<HTMLDivElement>(null)

  const handleTouchStart = (e: TouchEvent) => {
    setTouchStart(e.targetTouches[0].clientX)
    setIsSwiping(true)
  }

  const handleTouchMove = (e: TouchEvent) => {
    setTouchEnd(e.targetTouches[0].clientX)
  }

  const handleTouchEnd = () => {
    if (!isSwiping) return

    const swipeDistance = touchStart - touchEnd
    const isLeftSwipe = swipeDistance > threshold
    const isRightSwipe = swipeDistance < -threshold

    if (isLeftSwipe && onSwipeLeft) {
      onSwipeLeft()
    }

    if (isRightSwipe && onSwipeRight) {
      onSwipeRight()
    }

    setIsSwiping(false)
    setTouchStart(0)
    setTouchEnd(0)
  }

  return (
    <div
      ref={elementRef}
      onTouchStart={handleTouchStart}
      onTouchMove={handleTouchMove}
      onTouchEnd={handleTouchEnd}
      className={cn("touch-pan-y", className)}
    >
      {children}
    </div>
  )
}
