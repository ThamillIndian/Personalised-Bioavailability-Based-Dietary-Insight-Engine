"use client"

import { useState, useEffect, useRef } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Play, Pause, Square, Clock, Bell } from 'lucide-react'
import { cn } from '@/lib/utils'

interface Timer {
  id: string
  name: string
  duration: number // in seconds
  remaining: number
  isRunning: boolean
  isCompleted: boolean
}

interface CookingTimerProps {
  className?: string
}

export function CookingTimer({ className }: CookingTimerProps) {
  const [timers, setTimers] = useState<Timer[]>([])
  const [newTimerName, setNewTimerName] = useState('')
  const [newTimerMinutes, setNewTimerMinutes] = useState('')
  const intervalRef = useRef<NodeJS.Timeout | null>(null)

  // Update timers every second
  useEffect(() => {
    intervalRef.current = setInterval(() => {
      setTimers(prev => prev.map(timer => {
        if (!timer.isRunning || timer.isCompleted) return timer

        const newRemaining = timer.remaining - 1
        if (newRemaining <= 0) {
          // Timer completed
          playNotificationSound()
          return { ...timer, remaining: 0, isRunning: false, isCompleted: true }
        }
        return { ...timer, remaining: newRemaining }
      }))
    }, 1000)

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
      }
    }
  }, [])

  const playNotificationSound = () => {
    // Create a simple notification sound
    const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)()
    const oscillator = audioContext.createOscillator()
    const gainNode = audioContext.createGain()
    
    oscillator.connect(gainNode)
    gainNode.connect(audioContext.destination)
    
    oscillator.frequency.setValueAtTime(800, audioContext.currentTime)
    oscillator.frequency.setValueAtTime(600, audioContext.currentTime + 0.1)
    oscillator.frequency.setValueAtTime(800, audioContext.currentTime + 0.2)
    
    gainNode.gain.setValueAtTime(0.3, audioContext.currentTime)
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5)
    
    oscillator.start(audioContext.currentTime)
    oscillator.stop(audioContext.currentTime + 0.5)
  }

  const addTimer = () => {
    if (!newTimerName.trim() || !newTimerMinutes) return

    const duration = parseInt(newTimerMinutes) * 60
    const newTimer: Timer = {
      id: Date.now().toString(),
      name: newTimerName.trim(),
      duration,
      remaining: duration,
      isRunning: false,
      isCompleted: false
    }

    setTimers(prev => [...prev, newTimer])
    setNewTimerName('')
    setNewTimerMinutes('')
  }

  const toggleTimer = (id: string) => {
    setTimers(prev => prev.map(timer => 
      timer.id === id 
        ? { ...timer, isRunning: !timer.isRunning }
        : timer
    ))
  }

  const resetTimer = (id: string) => {
    setTimers(prev => prev.map(timer => 
      timer.id === id 
        ? { ...timer, remaining: timer.duration, isRunning: false, isCompleted: false }
        : timer
    ))
  }

  const deleteTimer = (id: string) => {
    setTimers(prev => prev.filter(timer => timer.id !== id))
  }

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  const getProgress = (timer: Timer) => {
    return ((timer.duration - timer.remaining) / timer.duration) * 100
  }

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Clock className="h-5 w-5" />
          Cooking Timer
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Add Timer Form */}
        <div className="grid gap-3 md:grid-cols-3">
          <div>
            <Label htmlFor="timer-name">Timer Name</Label>
            <Input
              id="timer-name"
              placeholder="e.g. Pasta"
              value={newTimerName}
              onChange={(e) => setNewTimerName(e.target.value)}
            />
          </div>
          <div>
            <Label htmlFor="timer-minutes">Minutes</Label>
            <Input
              id="timer-minutes"
              type="number"
              min="1"
              max="999"
              placeholder="10"
              value={newTimerMinutes}
              onChange={(e) => setNewTimerMinutes(e.target.value)}
            />
          </div>
          <div className="flex items-end">
            <Button onClick={addTimer} className="w-full">
              Add Timer
            </Button>
          </div>
        </div>

        {/* Timers List */}
        {timers.length > 0 && (
          <div className="space-y-3">
            {timers.map((timer) => (
              <div
                key={timer.id}
                className={cn(
                  "rounded-lg border p-3 transition-all",
                  timer.isCompleted ? "border-green-200 bg-green-50" : "border-gray-200"
                )}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <h4 className="font-medium">{timer.name}</h4>
                    {timer.isCompleted && (
                      <Bell className="h-4 w-4 text-green-600" />
                    )}
                  </div>
                  <div className="flex items-center gap-2">
                    <span className={cn(
                      "text-lg font-mono",
                      timer.isCompleted ? "text-green-600" : 
                      timer.isRunning ? "text-blue-600" : "text-gray-600"
                    )}>
                      {formatTime(timer.remaining)}
                    </span>
                    <div className="flex gap-1">
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => toggleTimer(timer.id)}
                        disabled={timer.isCompleted}
                      >
                        {timer.isRunning ? (
                          <Pause className="h-3 w-3" />
                        ) : (
                          <Play className="h-3 w-3" />
                        )}
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => resetTimer(timer.id)}
                      >
                        <Square className="h-3 w-3" />
                      </Button>
                    </div>
                  </div>
                </div>
                
                {/* Progress Bar */}
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={cn(
                      "h-2 rounded-full transition-all duration-1000",
                      timer.isCompleted ? "bg-green-500" : "bg-blue-500"
                    )}
                    style={{ width: `${getProgress(timer)}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        )}

        {timers.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            <Clock className="h-12 w-12 mx-auto mb-2 opacity-50" />
            <p>No timers set. Add one to get started!</p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
