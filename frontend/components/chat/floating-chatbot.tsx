"use client"

import { useState, useRef, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { ScrollArea } from '@/components/ui/scroll-area'
import { MessageCircle, X, Send, Bot, User, Sparkles } from 'lucide-react'
import { cn } from '@/lib/utils'
import { chatApi } from '@/lib/api'

interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

interface FloatingChatbotProps {
  className?: string
}

export function FloatingChatbot({ className }: FloatingChatbotProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [conversationId, setConversationId] = useState<string | undefined>()
  const [quickQuestions, setQuickQuestions] = useState<string[]>([])
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Load quick questions when chatbot opens
  useEffect(() => {
    if (isOpen && quickQuestions.length === 0) {
      loadQuickQuestions()
    }
  }, [isOpen])

  const loadQuickQuestions = async () => {
    try {
      const response = await chatApi.getQuickQuestions()
      setQuickQuestions(response.questions)
    } catch (error) {
      console.error('Failed to load quick questions:', error)
    }
  }

  const sendMessage = async (content: string) => {
    if (!content.trim() || isLoading) return

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: content.trim(),
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    setIsLoading(true)

    try {
      const response = await chatApi.sendMessage(
        content.trim(),
        conversationId,
        { page: 'chatbot' }
      )

      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.message,
        timestamp: new Date()
      }

      setMessages(prev => [...prev, assistantMessage])
      
      if (response.conversation_id) {
        setConversationId(response.conversation_id)
      }

      // Update quick questions if provided
      if (response.suggestions) {
        setQuickQuestions(response.suggestions)
      }
    } catch (error) {
      console.error('Failed to send message:', error)
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    sendMessage(inputValue)
  }

  const handleQuickQuestion = (question: string) => {
    sendMessage(question)
  }

  const toggleChat = () => {
    setIsOpen(!isOpen)
    if (!isOpen) {
      // Reset conversation when opening
      setMessages([])
      setConversationId(undefined)
    }
  }

  return (
    <div className={cn("fixed bottom-6 right-6 z-50", className)}>
      {/* Chat Button */}
      {!isOpen && (
        <Button
          onClick={toggleChat}
          size="lg"
          className="h-14 w-14 rounded-full bg-primary shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105"
        >
          <MessageCircle className="h-6 w-6" />
        </Button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <Card className="w-80 h-96 shadow-2xl border-0 bg-white/95 backdrop-blur-sm">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2 bg-gradient-to-r from-primary to-primary/80 text-white rounded-t-lg">
            <div className="flex items-center space-x-2">
              <div className="flex items-center space-x-1">
                <Bot className="h-4 w-4" />
                <span className="font-semibold">Recipe Assistant</span>
              </div>
              <Badge variant="secondary" className="text-xs">
                <Sparkles className="h-3 w-3 mr-1" />
                AI
              </Badge>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={toggleChat}
              className="h-8 w-8 p-0 text-white hover:bg-white/20"
            >
              <X className="h-4 w-4" />
            </Button>
          </CardHeader>

          <CardContent className="p-0 flex flex-col h-full">
            {/* Messages */}
            <ScrollArea className="flex-1 p-4">
              {messages.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-full text-center text-muted-foreground">
                  <Bot className="h-12 w-12 mb-4 text-primary/50" />
                  <h3 className="font-semibold mb-2">Welcome to Recipe Assistant!</h3>
                  <p className="text-sm mb-4">
                    I can help you with recipe suggestions, cooking tips, and ingredient substitutions.
                  </p>
                  {quickQuestions.length > 0 && (
                    <div className="space-y-2 w-full">
                      <p className="text-xs font-medium">Quick questions:</p>
                      <div className="flex flex-wrap gap-2 justify-center">
                        {quickQuestions.slice(0, 3).map((question, index) => (
                          <Button
                            key={index}
                            variant="outline"
                            size="sm"
                            onClick={() => handleQuickQuestion(question)}
                            className="text-xs h-auto py-1 px-2"
                          >
                            {question}
                          </Button>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="space-y-4">
                  {messages.map((message) => (
                    <div
                      key={message.id}
                      className={cn(
                        "flex items-start space-x-2",
                        message.role === 'user' ? 'flex-row-reverse space-x-reverse' : ''
                      )}
                    >
                      <div className={cn(
                        "flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center",
                        message.role === 'user' 
                          ? 'bg-primary text-primary-foreground' 
                          : 'bg-muted text-muted-foreground'
                      )}>
                        {message.role === 'user' ? (
                          <User className="h-4 w-4" />
                        ) : (
                          <Bot className="h-4 w-4" />
                        )}
                      </div>
                      <div className={cn(
                        "max-w-[80%] rounded-lg px-3 py-2 text-sm",
                        message.role === 'user'
                          ? 'bg-primary text-primary-foreground'
                          : 'bg-muted'
                      )}>
                        <p className="whitespace-pre-wrap">{message.content}</p>
                        <p className="text-xs opacity-70 mt-1">
                          {message.timestamp.toLocaleTimeString([], { 
                            hour: '2-digit', 
                            minute: '2-digit' 
                          })}
                        </p>
                      </div>
                    </div>
                  ))}
                  {isLoading && (
                    <div className="flex items-start space-x-2">
                      <div className="flex-shrink-0 w-8 h-8 rounded-full bg-muted text-muted-foreground flex items-center justify-center">
                        <Bot className="h-4 w-4" />
                      </div>
                      <div className="bg-muted rounded-lg px-3 py-2 text-sm">
                        <div className="flex space-x-1">
                          <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" />
                          <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                          <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                        </div>
                      </div>
                    </div>
                  )}
                  <div ref={messagesEndRef} />
                </div>
              )}
            </ScrollArea>

            {/* Input */}
            <div className="border-t p-4">
              <form onSubmit={handleSubmit} className="flex space-x-2">
                <Input
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  placeholder="Ask about recipes, cooking tips..."
                  disabled={isLoading}
                  className="flex-1"
                />
                <Button type="submit" size="sm" disabled={isLoading || !inputValue.trim()}>
                  <Send className="h-4 w-4" />
                </Button>
              </form>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}