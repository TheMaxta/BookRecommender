// frontend/app/page.tsx
"use client"

import FavoriteSubjectCard from "@/components/FavoriteSubjectCard"

export default function HomePage() {
  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-8">
      <FavoriteSubjectCard />
    </main>
  )
}
