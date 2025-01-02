"use client"

import { useState, useEffect } from "react"
import Image from "next/image"
import { Star, StarHalf } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import BookDetailCard from "./BookDetailCard"

type Book = {
  unique_id: string;
  Title: string;
  Subject: string;
  Description: string;
  content: string;
  rating: number;
  book_collection: string;
  csv_file: string;
  image?: string;
  LibrariansSummary?: string;
  PositiveCharacters?: string;
  NegativeCharacters?: string;
};

type TopBooksCardProps = {
  selectedCategory: string | null
}

export default function TopBooksCard({ selectedCategory }: TopBooksCardProps) {
  const [books, setBooks] = useState<Book[]>([])
  const [selectedBook, setSelectedBook] = useState<Book | null>(null)

  useEffect(() => {
    setSelectedBook(null)

    if (selectedCategory) {
      fetchBooks(selectedCategory)
    } else {
      setBooks([])
    }
  }, [selectedCategory])

  async function fetchBooks(category: string) {
    try {
      const response = await fetch(
        `http://localhost:5001/api/books?category=${encodeURIComponent(category)}`
      )
      const data = await response.json()
      console.log("Fetched books:", data.books)
      setBooks(data.books || [])
    } catch (error) {
      console.error("Error fetching books:", error)
      setBooks([])
    }
  }

  const categoryColors: Record<string, string> = {
    Animals: "from-red-100 to-red-200",
    Friendship: "from-yellow-100 to-yellow-200",
    Family: "from-green-100 to-green-200",
    Adventure: "from-blue-100 to-blue-200",
    "Fantasy and Imagination": "from-purple-100 to-purple-200",
    "Life Lessons": "from-pink-100 to-pink-200",
  }

  const backgroundGradient = selectedCategory
    ? categoryColors[selectedCategory] || "from-blue-100 to-purple-100"
    : "from-blue-100 to-purple-100"

  if (selectedBook) {
    return (
      <BookDetailCard 
        book={selectedBook} 
        onBack={() => setSelectedBook(null)} 
      />
    )
  }

  return (
    <Card className={`w-full max-w-4xl mx-auto bg-gradient-to-br ${backgroundGradient} shadow-xl border-2 border-gray-200 rounded-xl overflow-hidden`}>
      <CardHeader className="text-center">
        <CardTitle className="text-3xl font-bold text-purple-600">
          Top 10 {selectedCategory ? `${selectedCategory} Books` : "Books"}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[600px] pr-4">
          {books.map((book, index) => {
            // Fallback to a placeholder image if `book.image` is missing or empty
            const imageSrc = book.image && book.image.trim() !== ""
              ? book.image
              : "/placeholder.png?height=120&width=80"

            return (
              <div
                key={book.unique_id}
                className="flex items-start space-x-4 mb-6 bg-white bg-opacity-60 p-4 rounded-lg cursor-pointer hover:bg-opacity-80 transition-colors duration-200"
                onClick={() => setSelectedBook(book)}
              >
                <div className="flex-shrink-0">
                  <Image
                    src={ imageSrc || "/placeholder.png" }
                    alt={`Cover of ${book.Title}`}
                    width={80}
                    height={120}
                    className="rounded-md shadow-md"
                  />
                </div>
                <div className="flex-grow">
                  <h3 className="text-xl font-semibold text-gray-800">
                    {index + 1}. {book.Title}
                  </h3>

                  {/* Subject label */}
                  <p className="mt-1 font-semibold text-gray-800">
                    Subject: <span className="font-normal text-gray-600">{book.Subject}</span>
                  </p>

                  {/* Short summary label */}
                  <p className="mt-2 font-semibold text-gray-800">
                    Summary:
                  </p>
                  <p className="text-sm text-gray-700">
                    {book.Description}
                  </p>

                  {/* Rating (5-star logic) */}
                  <div className="flex items-center mt-2">
                    {[...Array(5)].map((_, i) => (
                      <span key={i}>
                        {book.rating >= i + 1 ? (
                          <Star className="w-4 h-4 text-yellow-400 fill-current" />
                        ) : book.rating > i ? (
                          <StarHalf className="w-4 h-4 text-yellow-400 fill-current" />
                        ) : (
                          <Star className="w-4 h-4 text-gray-300" />
                        )}
                      </span>
                    ))}
                    <span className="ml-2 text-sm text-gray-600">
                      {Number(book.rating).toFixed(1)}
                    </span>
                  </div>
                </div>
              </div>
            )
          })}
        </ScrollArea>
      </CardContent>
    </Card>
  )
}
