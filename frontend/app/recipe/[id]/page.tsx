import { RecipeDetailClient } from "./recipe-detail-client"

export default function RecipeDetailPage({ params }: { params: { id: string } }) {
  return <RecipeDetailClient recipeId={params.id} />
}
