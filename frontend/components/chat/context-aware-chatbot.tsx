"use client"

import { useState, useRef, useEffect, useCallback } from 'react'
import { usePathname } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { MessageCircle, X, Send, Bot, User, Sparkles, ChefHat, Search, Heart } from 'lucide-react'
import { cn } from '@/lib/utils'
import { chatApi } from '@/lib/api'
import { useRecipeContext } from './recipe-context-provider'

interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

interface ContextAwareChatbotProps {
  className?: string
  recipeContext?: {
    id?: string
    title?: string
    ingredients?: string[]
    dietaryTags?: string[]
  }
}

export function ContextAwareChatbot({ className, recipeContext }: ContextAwareChatbotProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [conversationId, setConversationId] = useState<string | undefined>()
  const [quickQuestions, setQuickQuestions] = useState<string[]>([])
  const [showAllQuestions, setShowAllQuestions] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const pathname = usePathname()
  const { recipeContext: globalRecipeContext } = useRecipeContext()

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    setTimeout(() => {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, 100)
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const getPageContext = useCallback(() => {
    if (pathname === '/') return 'home'
    if (pathname === '/search') return 'search'
    if (pathname === '/collection') return 'collection'
    if (pathname.startsWith('/recipe/')) return 'recipe_detail'
    return 'general'
  }, [pathname])

  const getDefaultQuestions = useCallback(() => {
    const context = getPageContext()
    switch (context) {
      case 'home':
        return [
          "What are some easy dinner recipes?",
          "Can you suggest healthy breakfast ideas?",
          "What can I cook with chicken?"
        ]
      case 'search':
        return [
          "How do I substitute eggs in baking?",
          "What are good vegetarian protein sources?",
          "Can you help me find gluten-free recipes?"
        ]
      case 'collection':
        return [
          "How can I organize my saved recipes?",
          "Can you suggest similar recipes to my favorites?",
          "What cooking tips do you have?"
        ]
      case 'recipe_detail':
        return [
          "Can I substitute any ingredients in this recipe?",
          "How do I adjust the serving size?",
          "What side dishes go well with this?"
        ]
      default:
        return [
          "What are some popular recipes?",
          "Can you help with cooking tips?",
          "What ingredients can I substitute?"
        ]
    }
  }, [getPageContext])

  const loadContextAwareQuestions = useCallback(async () => {
    try {
      const context: any = { page: getPageContext() }
      
      // Use prop context first, then fall back to global context
      const activeContext = recipeContext || globalRecipeContext
      
      if (activeContext) {
        context.recipe_id = activeContext.id
        context.recipe_title = activeContext.title
        context.current_ingredients = activeContext.ingredients
        context.dietary_restrictions = activeContext.dietaryTags
      }

      const response = await chatApi.getQuickQuestions(
        context.page,
        context.recipe_id,
        context.recipe_title
      )
      setQuickQuestions(response.questions)
    } catch (error) {
      console.error('Failed to load quick questions:', error)
      // Fallback to default questions
      setQuickQuestions(getDefaultQuestions())
    }
  }, [pathname, recipeContext?.id, globalRecipeContext?.id, getDefaultQuestions])

  // Load context-aware quick questions when chatbot opens
  useEffect(() => {
    if (isOpen && quickQuestions.length === 0) {
      loadContextAwareQuestions()
    }
  }, [isOpen, pathname, recipeContext?.id, globalRecipeContext?.id, loadContextAwareQuestions])

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
      const context: any = { 
        page: getPageContext(),
        timestamp: new Date().toISOString()
      }
      
      // Use prop context first, then fall back to global context
      const activeContext = recipeContext || globalRecipeContext
      
      if (activeContext) {
        context.recipe_id = activeContext.id
        context.recipe_title = activeContext.title
        context.current_ingredients = activeContext.ingredients
        context.dietary_restrictions = activeContext.dietaryTags
      }

      const response = await chatApi.sendMessage(
        content.trim(),
        conversationId,
        context
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
      setShowAllQuestions(false)
    }
  }

  const getPageIcon = () => {
    const context = getPageContext()
    switch (context) {
      case 'home': return <ChefHat className="h-4 w-4" />
      case 'search': return <Search className="h-4 w-4" />
      case 'collection': return <Heart className="h-4 w-4" />
      case 'recipe_detail': return <ChefHat className="h-4 w-4" />
      default: return <Bot className="h-4 w-4" />
    }
  }

  const getPageTitle = () => {
    const context = getPageContext()
    switch (context) {
      case 'home': return 'Recipe Assistant'
      case 'search': return 'Search Helper'
      case 'collection': return 'Collection Helper'
      case 'recipe_detail': return 'Recipe Helper'
      default: return 'Recipe Assistant'
    }
  }

  return (
    <div className={cn("fixed bottom-6 right-6 z-50", className)}>
      {/* Chat Button */}
      {!isOpen && (
        <Button
          onClick={toggleChat}
          size="lg"
          className="h-14 w-14 rounded-full bg-orange-500 hover:bg-orange-600 shadow-xl hover:shadow-2xl transition-all duration-300 hover:scale-110 border-2 border-white"
        >
          <MessageCircle className="h-6 w-6 text-white" />
        </Button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <Card className="w-80 h-[500px] shadow-2xl border border-gray-200 bg-white rounded-lg overflow-hidden">
          <CardHeader className="bg-slate-800 text-white p-4 border-b border-slate-700 relative">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-lg">Recipe Assistant</h3>
                <p className="text-slate-300 text-sm">Context: {getPageContext()}</p>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={toggleChat}
                className="h-8 w-8 p-0 text-white hover:text-slate-800 hover:bg-white rounded-full transition-all duration-200 flex items-center justify-center bg-white/10 hover:bg-white"
              >
                <X className="h-5 w-5" />
              </Button>
            </div>
          </CardHeader>

          <CardContent className="p-0 flex flex-col h-full">
            {/* Messages */}
            <div className="flex-1 overflow-y-auto bg-white scrollbar-thin scrollbar-thumb-slate-300 scrollbar-track-slate-100">
              <div className="p-4">
                {messages.length === 0 ? (
                  <div className="space-y-4">
                    {/* Welcome Message */}
                    <div className="flex items-start space-x-3">
                      <div className="flex-shrink-0 w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center border border-slate-200">
                        <Bot className="h-4 w-4 text-slate-600" />
                      </div>
                      <div className="bg-slate-50 rounded-2xl rounded-tl-sm px-4 py-3 max-w-[85%] border border-slate-200">
                        <p className="text-sm text-slate-700 leading-relaxed">
                          Hi! I'm your Recipe Assistant. Ask me about substitutions, steps, or nutrition.
                        </p>
                      </div>
                    </div>

                    {/* Quick Questions */}
                    {quickQuestions.length > 0 && (
                      <div className="flex flex-wrap gap-2">
                        {(showAllQuestions ? quickQuestions : quickQuestions.slice(0, 2)).map((question, index) => (
                          <Button
                            key={index}
                            onClick={() => handleQuickQuestion(question)}
                            className="bg-emerald-500 hover:bg-emerald-600 text-white text-sm px-4 py-2 rounded-full border-0 shadow-sm transition-all duration-200 hover:shadow-md"
                          >
                            {question}
                          </Button>
                        ))}
                        {quickQuestions.length > 2 && !showAllQuestions && (
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => setShowAllQuestions(true)}
                            className="text-slate-500 text-sm px-4 py-2 rounded-full border-slate-300 hover:bg-slate-50 hover:border-slate-400"
                          >
                            More
                          </Button>
                        )}
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="space-y-4">
                    {messages.map((message) => (
                      <div
                        key={message.id}
                        className={cn(
                          "flex items-start space-x-3 mb-4",
                          message.role === 'user' ? 'flex-row-reverse space-x-reverse' : ''
                        )}
                      >
                        <div className={cn(
                          "flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center border",
                          message.role === 'user' 
                            ? 'bg-blue-500 text-white border-blue-500' 
                            : 'bg-slate-100 text-slate-600 border-slate-200'
                        )}>
                          {message.role === 'user' ? (
                            <User className="h-4 w-4" />
                          ) : (
                            <Bot className="h-4 w-4" />
                          )}
                        </div>
                        <div className={cn(
                          "max-w-[85%] rounded-2xl px-4 py-3 text-sm border shadow-sm",
                          message.role === 'user'
                            ? 'bg-blue-500 text-white border-blue-500 rounded-br-sm'
                            : 'bg-slate-50 text-slate-700 border-slate-200 rounded-bl-sm'
                        )}>
                          <p className="whitespace-pre-wrap leading-relaxed">{message.content}</p>
                        </div>
                      </div>
                    ))}
                    {isLoading && (
                      <div className="flex items-start space-x-3 mb-4">
                        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center border border-slate-200">
                          <Bot className="h-4 w-4 text-slate-600" />
                        </div>
                        <div className="bg-slate-50 rounded-2xl rounded-tl-sm px-4 py-3 border border-slate-200 shadow-sm">
                          <div className="flex space-x-1">
                            <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" />
                            <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                            <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                          </div>
                        </div>
                      </div>
                    )}
                    <div ref={messagesEndRef} className="h-4" />
                  </div>
                )}
                <div className="h-4" />
              </div>
            </div>

            {/* Input */}
            <div className="border-t border-slate-200 p-4 bg-slate-50">
              <form onSubmit={handleSubmit} className="flex space-x-3">
                <Input
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  placeholder="Type your question..."
                  disabled={isLoading}
                  className="flex-1 border-slate-300 focus:border-slate-400 rounded-full px-4 py-2 bg-white shadow-sm"
                />
                <Button 
                  type="submit" 
                  disabled={isLoading || !inputValue.trim()}
                  className="bg-orange-500 hover:bg-orange-600 text-white border-0 rounded-full px-6 shadow-sm transition-all duration-200 hover:shadow-md"
                >
                  Send
                </Button>
              </form>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
