import Link from "next/link"
import { Button } from "@/components/ui/button"
import { SuggestedRecipes } from "@/components/suggested-recipes"
import { HomePageClient } from "./home-client"

export default function HomePage() {
  return (
    <main className="mx-auto max-w-6xl px-4 py-10">
      <section className="grid gap-8 md:grid-cols-2 md:items-center">
        <div className="space-y-4">
          <h1 className="text-pretty text-3xl font-semibold leading-tight md:text-4xl">
            Generate smarter recipes from whatever's in your kitchen
          </h1>
          <p className="text-pretty text-foreground/70">
            Describe ingredients, diets, time, or calories. We'll help you find or create the perfect recipe.
          </p>
          <div className="flex items-center gap-3">
            <Link href="/search">
              <Button>Start Generating</Button>
            </Link>
            <Link href="/search">
              <Button variant="outline">Browse Ideas</Button>
            </Link>
          </div>
          <ul className="mt-4 grid gap-2 text-sm text-foreground/70 md:grid-cols-2">
            <li>• Dietary options: Vegan, Vegetarian, Gluten-Free</li>
            <li>• Filters: Time and calories</li>
            <li>• Save favorites to your collection</li>
            <li>• Quick, responsive, and accessible</li>
          </ul>
        </div>
        <div className="rounded-lg border p-4">
          <img
            src="/assorted-healthy-recipes-grid.jpg"
            alt="Assorted healthy recipes"
            className="h-auto w-full rounded-md object-cover"
          />
        </div>
      </section>
      <section className="mt-12">
        <h2 className="mb-4 text-xl font-semibold">Popular Categories</h2>
        <div className="grid gap-3 sm:grid-cols-2 md:grid-cols-4">
          {["Breakfast", "High-Protein", "Vegan", "Quick Dinners"].map((c) => (
            <Link
              key={c}
              href="/search"
              className="rounded-lg border p-4 transition-colors hover:bg-accent hover:text-accent-foreground"
            >
              <div className="text-pretty">{c}</div>
            </Link>
          ))}
        </div>
      </section>
      <section className="mt-12">
        <HomePageClient />
      </section>
    </main>
  )
}
