"use client"

import { useState } from "react"
import { Book, Users, Home, Compass, Wand2, Lightbulb, Send } from 'lucide-react'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import TopBooksCard from "./TopBooksCard"

const subjects = [
  { name: "Animals", icon: Book },
  { name: "Friendship", icon: Users },
  { name: "Family", icon: Home },
  { name: "Adventure", icon: Compass },
  { name: "Fantasy and Imagination", icon: Wand2 },
  { name: "Life Lessons", icon: Lightbulb },
]

const colors = [
  "bg-red-400",
  "bg-yellow-400",
  "bg-green-400",
  "bg-blue-400",
  "bg-purple-400",
  "bg-pink-400",
]

export default function FavoriteSubjectCard() {
  // State to track selected subject, can be string or null
  const [selectedSubject, setSelectedSubject] = useState<string | null>(null)

  // Toggles selection: if clicked subject is already selected, unselect it
  const handleSubjectClick = (subject: string) => {
    setSelectedSubject(prev => prev === subject ? null : subject)
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (selectedSubject) {
      console.log("Submitted subject:", selectedSubject)
      alert(`You selected: ${selectedSubject}`)
    } else {
      alert("Please select a favorite subject!")
    }
  }

  return (
    <div className="space-y-8">
      <Card className="w-full max-w-4xl mx-auto bg-gradient-to-br from-blue-100 to-purple-100 shadow-xl border-2 border-gray-200 rounded-xl overflow-hidden">
        <CardHeader className="text-center">
          <CardTitle className="text-4xl font-bold text-purple-600">What Do You Love to Read?</CardTitle>
          <CardDescription className="text-xl text-blue-600">Click on your favorite subject!</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit}>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              {subjects.map((subject, index) => {
                const Icon = subject.icon
                const isSelected = selectedSubject === subject.name
                return (
                  <Button
                    key={subject.name}
                    type="button"
                    onClick={() => handleSubjectClick(subject.name)}
                    className={`
                      h-24 text-lg font-semibold transition-all transform hover:scale-105 
                      ${colors[index]} 
                      ${isSelected
                        ? "ring-4 ring-yellow-300 shadow-lg"
                        : selectedSubject ? "brightness-90" : ""
                      }
                    `}
                  >
                    <div className="flex flex-col items-center space-y-2">
                      <Icon size={32} />
                      <span>{subject.name}</span>
                    </div>
                  </Button>
                )
              })}
            </div>
          </form>
        </CardContent>
        <CardFooter className="flex justify-center">
          <Button
            type="submit"
            onClick={handleSubmit}
            className="mt-4 bg-green-500 hover:bg-green-600 text-white text-xl py-6 px-8 rounded-full shadow-lg transform transition-all hover:scale-105"
          >
            <Send className="mr-2 h-6 w-6" /> Submit My Choice!
          </Button>
        </CardFooter>
      </Card>
      
      <TopBooksCard selectedCategory={selectedSubject} />
    </div>
  )
}
