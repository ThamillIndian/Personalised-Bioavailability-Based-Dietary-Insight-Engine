"use client"

import { RatingWidget } from "./rating-widget"

/**
 * Demo component showing different rating widget configurations
 * This can be used to test both autosave and save button modes
 */
export function RatingWidgetDemo() {
  return (
    <div className="space-y-8 p-6">
      <div>
        <h3 className="mb-4 text-lg font-semibold">Rating Widget Demo</h3>
        
        <div className="grid gap-6 md:grid-cols-2">
          {/* Autosave Mode (Default) */}
          <div className="rounded-lg border p-4">
            <h4 className="mb-2 font-medium">Autosave Mode (Default)</h4>
            <p className="mb-4 text-sm text-muted-foreground">
              Ratings are automatically saved after 1 second of inactivity
            </p>
            <RatingWidget 
              recipeId="demo-recipe-autosave" 
              enableAutosave={true}
              showSaveButton={false}
            />
          </div>

          {/* Save Button Mode */}
          <div className="rounded-lg border p-4">
            <h4 className="mb-2 font-medium">Save Button Mode</h4>
            <p className="mb-4 text-sm text-muted-foreground">
              Ratings are saved only when you click the Save button
            </p>
            <RatingWidget 
              recipeId="demo-recipe-save-button" 
              enableAutosave={false}
              showSaveButton={true}
            />
          </div>

          {/* Hybrid Mode */}
          <div className="rounded-lg border p-4">
            <h4 className="mb-2 font-medium">Hybrid Mode</h4>
            <p className="mb-4 text-sm text-muted-foreground">
              Both autosave AND save button available
            </p>
            <RatingWidget 
              recipeId="demo-recipe-hybrid" 
              enableAutosave={true}
              showSaveButton={true}
            />
          </div>

          {/* No Save Mode */}
          <div className="rounded-lg border p-4">
            <h4 className="mb-2 font-medium">No Save Mode</h4>
            <p className="mb-4 text-sm text-muted-foreground">
              Ratings are only saved to localStorage, not to server
            </p>
            <RatingWidget 
              recipeId="demo-recipe-no-save" 
              enableAutosave={false}
              showSaveButton={false}
            />
          </div>
        </div>
      </div>

      <div className="rounded-lg bg-blue-50 p-4">
        <h4 className="mb-2 font-medium text-blue-900">How it works:</h4>
        <ul className="space-y-1 text-sm text-blue-800">
          <li>• <strong>Autosave:</strong> Automatically saves to backend after 1 second delay</li>
          <li>• <strong>Save Button:</strong> Manual save with visual feedback</li>
          <li>• <strong>User ID:</strong> Automatically generated and stored in localStorage</li>
          <li>• <strong>Local Storage:</strong> Ratings persist across browser sessions</li>
          <li>• <strong>API:</strong> Sends data to <code>/api/v1/favorites/ratings</code></li>
          <li>• <strong>Error Handling:</strong> Graceful fallback if backend is unavailable</li>
        </ul>
      </div>
    </div>
  )
}

