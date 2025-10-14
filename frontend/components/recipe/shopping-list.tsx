"use client"

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Checkbox } from '@/components/ui/checkbox'
import { Badge } from '@/components/ui/badge'
import { ShoppingCart, Plus, Trash2, Download, Share2 } from 'lucide-react'
import { cn } from '@/lib/utils'

interface ShoppingItem {
  id: string
  name: string
  quantity: string
  category: string
  isChecked: boolean
}

interface ShoppingListProps {
  ingredients?: string[]
  className?: string
}

const categories = [
  'Produce',
  'Meat & Seafood',
  'Dairy & Eggs',
  'Pantry',
  'Frozen',
  'Bakery',
  'Other'
]

export function ShoppingList({ ingredients = [], className }: ShoppingListProps) {
  const [items, setItems] = useState<ShoppingItem[]>([])
  const [newItemName, setNewItemName] = useState('')
  const [newItemQuantity, setNewItemQuantity] = useState('')
  const [newItemCategory, setNewItemCategory] = useState('Other')

  // Initialize items from recipe ingredients
  useEffect(() => {
    if (ingredients.length > 0 && items.length === 0) {
      const initialItems: ShoppingItem[] = ingredients.map((ingredient, index) => ({
        id: `recipe-${index}`,
        name: ingredient,
        quantity: '',
        category: 'Pantry',
        isChecked: false
      }))
      setItems(initialItems)
    }
  }, [ingredients, items.length])

  const addItem = () => {
    if (!newItemName.trim()) return

    const newItem: ShoppingItem = {
      id: Date.now().toString(),
      name: newItemName.trim(),
      quantity: newItemQuantity.trim(),
      category: newItemCategory,
      isChecked: false
    }

    setItems(prev => [...prev, newItem])
    setNewItemName('')
    setNewItemQuantity('')
    setNewItemCategory('Other')
  }

  const toggleItem = (id: string) => {
    setItems(prev => prev.map(item =>
      item.id === id ? { ...item, isChecked: !item.isChecked } : item
    ))
  }

  const deleteItem = (id: string) => {
    setItems(prev => prev.filter(item => item.id !== id))
  }

  const clearCompleted = () => {
    setItems(prev => prev.filter(item => !item.isChecked))
  }

  const exportList = () => {
    const listText = items
      .filter(item => !item.isChecked)
      .map(item => `${item.quantity ? `${item.quantity} ` : ''}${item.name}`)
      .join('\n')
    
    const blob = new Blob([listText], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'shopping-list.txt'
    a.click()
    URL.revokeObjectURL(url)
  }

  const shareList = async () => {
    const listText = items
      .filter(item => !item.isChecked)
      .map(item => `${item.quantity ? `${item.quantity} ` : ''}${item.name}`)
      .join('\n')

    if (navigator.share) {
      try {
        await navigator.share({
          title: 'Shopping List',
          text: listText
        })
      } catch (error) {
        console.log('Error sharing:', error)
      }
    } else {
      // Fallback: copy to clipboard
      try {
        await navigator.clipboard.writeText(listText)
        alert('Shopping list copied to clipboard!')
      } catch (error) {
        console.log('Error copying:', error)
      }
    }
  }

  const itemsByCategory = items.reduce((acc, item) => {
    if (!acc[item.category]) {
      acc[item.category] = []
    }
    acc[item.category].push(item)
    return acc
  }, {} as Record<string, ShoppingItem[]>)

  const totalItems = items.length
  const completedItems = items.filter(item => item.isChecked).length
  const remainingItems = totalItems - completedItems

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <ShoppingCart className="h-5 w-5" />
            Shopping List
          </CardTitle>
          <div className="flex gap-2">
            <Button size="sm" variant="outline" onClick={exportList}>
              <Download className="h-3 w-3" />
            </Button>
            <Button size="sm" variant="outline" onClick={shareList}>
              <Share2 className="h-3 w-3" />
            </Button>
          </div>
        </div>
        {totalItems > 0 && (
          <div className="flex gap-2">
            <Badge variant="secondary">
              {remainingItems} remaining
            </Badge>
            <Badge variant="outline">
              {completedItems} completed
            </Badge>
          </div>
        )}
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Add Item Form */}
        <div className="grid gap-3 md:grid-cols-4">
          <div>
            <Label htmlFor="item-name">Item Name</Label>
            <Input
              id="item-name"
              placeholder="e.g. Tomatoes"
              value={newItemName}
              onChange={(e) => setNewItemName(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && addItem()}
            />
          </div>
          <div>
            <Label htmlFor="item-quantity">Quantity</Label>
            <Input
              id="item-quantity"
              placeholder="e.g. 2 lbs"
              value={newItemQuantity}
              onChange={(e) => setNewItemQuantity(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && addItem()}
            />
          </div>
          <div>
            <Label htmlFor="item-category">Category</Label>
            <select
              id="item-category"
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
              value={newItemCategory}
              onChange={(e) => setNewItemCategory(e.target.value)}
            >
              {categories.map(category => (
                <option key={category} value={category}>
                  {category}
                </option>
              ))}
            </select>
          </div>
          <div className="flex items-end">
            <Button onClick={addItem} className="w-full">
              <Plus className="h-4 w-4 mr-2" />
              Add
            </Button>
          </div>
        </div>

        {/* Items by Category */}
        {totalItems > 0 ? (
          <div className="space-y-4">
            {Object.entries(itemsByCategory).map(([category, categoryItems]) => (
              <div key={category} className="space-y-2">
                <h4 className="font-medium text-sm text-gray-600 uppercase tracking-wide">
                  {category}
                </h4>
                <div className="space-y-2">
                  {categoryItems.map((item) => (
                    <div
                      key={item.id}
                      className={cn(
                        "flex items-center gap-3 p-2 rounded-lg border transition-all",
                        item.isChecked 
                          ? "bg-green-50 border-green-200" 
                          : "bg-white border-gray-200 hover:border-gray-300"
                      )}
                    >
                      <Checkbox
                        checked={item.isChecked}
                        onCheckedChange={() => toggleItem(item.id)}
                      />
                      <div className="flex-1">
                        <span className={cn(
                          "text-sm",
                          item.isChecked && "line-through text-gray-500"
                        )}>
                          {item.quantity && `${item.quantity} `}
                          {item.name}
                        </span>
                      </div>
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => deleteItem(item.id)}
                        className="h-6 w-6 p-0 text-gray-400 hover:text-red-500"
                      >
                        <Trash2 className="h-3 w-3" />
                      </Button>
                    </div>
                  ))}
                </div>
              </div>
            ))}
            
            {completedItems > 0 && (
              <div className="pt-4 border-t">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={clearCompleted}
                  className="w-full"
                >
                  Clear Completed ({completedItems})
                </Button>
              </div>
            )}
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            <ShoppingCart className="h-12 w-12 mx-auto mb-2 opacity-50" />
            <p>No items in your shopping list yet.</p>
            <p className="text-sm">Add items manually or import from a recipe!</p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
