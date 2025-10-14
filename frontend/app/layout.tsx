import type React from "react"
import type { Metadata } from "next"
import { GeistSans } from "geist/font/sans"
import { GeistMono } from "geist/font/mono"
import { Analytics } from "@vercel/analytics/next"
import "./globals.css"
import { SiteNavbar } from "@/components/site-navbar"
import { Suspense } from "react"
import { ContextAwareChatbot } from "@/components/chat/context-aware-chatbot"
import { RecipeContextProvider } from "@/components/chat/recipe-context-provider"
import { ErrorBoundary } from "@/components/ui/error-boundary"
import { BottomNav } from "@/components/bottom-nav"

export const metadata: Metadata = {
  title: "v0 App",
  description: "Created with v0",
  generator: "v0.app",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className={`font-sans ${GeistSans.variable} ${GeistMono.variable}`}>
        <ErrorBoundary>
          <RecipeContextProvider>
            <Suspense fallback={<div>Loading...</div>}>
              <SiteNavbar />
              <div className="pb-16 md:pb-0">{children}</div>
              <BottomNav />
              <ContextAwareChatbot />
            </Suspense>
          </RecipeContextProvider>
        </ErrorBoundary>
        <Analytics />
      </body>
    </html>
  )
}
