import React, { useState } from "react";
import Image from "next/image";
import { Star, StarHalf, ArrowLeft, Send } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import ReactMarkdown from 'react-markdown';

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

type BookDetailCardProps = {
  book: Book;
  onBack: () => void;
};

const parseCharacterString = (characters?: string): string[] => {
  if (!characters) return [];
  try {
    // Remove square brackets and split by comma
    const cleanStr = characters.replace(/[\[\]']/g, '');
    return cleanStr.split(',').map(char => char.trim());
  } catch (error) {
    console.error('Error parsing characters:', error);
    return [];
  }
};


const BookDetailCard = ({ book, onBack }: BookDetailCardProps) => {
  const [question, setQuestion] = useState("");
  const [chat, setChat] = useState<{ role: "user" | "assistant"; content: string }[]>([]);

  
  const handleAskQuestion = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    // Add user message to chat
    const newChat = [...chat, { role: "user" as const, content: question }];
    setChat(newChat);
    setQuestion("");

    try {
      const response = await fetch('http://localhost:5001/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          unique_id: book.unique_id,
          messages: newChat,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();
      setChat(prev => [...prev, data.message]);
      
    } catch (error) {
      console.error('Error getting response:', error);
      setChat(prev => [...prev, {
        role: 'assistant',
        content: 'I apologize, but I encountered an error processing your question. Please try again.'
      }]);
    }
  };

  const imageSrc = book.image && book.image.trim() !== ""
    ? book.image
    : "/placeholder.png?height=200&width=140";

  // Custom styles for markdown content
  const markdownStyles = {
    p: 'text-gray-800 mb-4',
    h1: 'text-2xl font-bold mb-4 text-gray-900',
    h2: 'text-xl font-bold mb-3 text-gray-900',
    h3: 'text-lg font-bold mb-2 text-gray-900',
    ul: 'list-disc pl-6 mb-4',
    ol: 'list-decimal pl-6 mb-4',
    li: 'mb-1 text-gray-800',
    blockquote: 'border-l-4 border-gray-300 pl-4 italic my-4',
    code: 'bg-gray-100 rounded px-1 py-0.5',
    pre: 'bg-gray-100 rounded p-4 my-4 overflow-x-auto'
  };

  return (
    <Card className="w-full max-w-4xl mx-auto bg-gradient-to-br from-blue-100 to-purple-100 shadow-xl border-2 border-gray-200 rounded-xl overflow-hidden">
      <CardHeader className="text-center relative">
        <Button 
          variant="ghost" 
          className="absolute left-4 top-4"
          onClick={onBack}
        >
          <ArrowLeft className="mr-2 h-4 w-4" /> Back
        </Button>
        <CardTitle className="text-3xl font-bold text-purple-600">
          {book.Title}
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Title and Rating Section */}
        <div className="flex items-center justify-between">
          <div className="text-lg font-semibold text-gray-700">
            Subject: {book.Subject}
          </div>
          <div className="flex items-center">
            {[...Array(5)].map((_, i) => (
              <span key={i}>
                {book.rating >= i + 1 ? (
                  <Star className="w-5 h-5 text-yellow-400 fill-current" />
                ) : book.rating > i ? (
                  <StarHalf className="w-5 h-5 text-yellow-400 fill-current" />
                ) : (
                  <Star className="w-5 h-5 text-gray-300" />
                )}
              </span>
            ))}
            <span className="ml-2 text-lg text-gray-600">
              {Number(book.rating).toFixed(1)}
            </span>
          </div>
        </div>

        {/* Image and Description Section */}
        <div className="flex space-x-6">
          <div className="flex-shrink-0">
            <Image
              src={imageSrc}
              alt={`Cover of ${book.Title}`}
              width={140}
              height={200}
              className="rounded-md shadow-md"
            />
          </div>

          <div className="flex-1">
            <p className="font-semibold text-gray-800 mb-2">
              Brief Summary of The Book:
            </p>
            <p className="text-gray-700">{book.Description}</p>
          </div>
        </div>

        {/* AI Librarian Opinion Section - Full Width */}
        <div className="w-full bg-white bg-opacity-50 rounded-lg p-6">
          <h4 className="text-xl font-bold text-indigo-600 mb-4">
            The AI Librarian's Recommendation:
          </h4>
          <div className="prose prose-sm max-w-none">
            <ReactMarkdown
              components={{
                p: ({ children }) => <p className={markdownStyles.p}>{children}</p>,
                h1: ({ children }) => <h1 className={markdownStyles.h1}>{children}</h1>,
                h2: ({ children }) => <h2 className={markdownStyles.h2}>{children}</h2>,
                h3: ({ children }) => <h3 className={markdownStyles.h3}>{children}</h3>,
                ul: ({ children }) => <ul className={markdownStyles.ul}>{children}</ul>,
                ol: ({ children }) => <ol className={markdownStyles.ol}>{children}</ol>,
                li: ({ children }) => <li className={markdownStyles.li}>{children}</li>,
                blockquote: ({ children }) => <blockquote className={markdownStyles.blockquote}>{children}</blockquote>,
                code: ({ children }) => <code className={markdownStyles.code}>{children}</code>,
                pre: ({ children }) => <pre className={markdownStyles.pre}>{children}</pre>,
              }}
            >
              {book.LibrariansSummary || "No AI Librarians opinion available yet. (Future feature placeholder)"}
            </ReactMarkdown>
          </div>
        </div>


        {/* Heroes and Villains Section */}
        <div className="w-full flex gap-4">
          {/* Heroes Panel */}
          <div className="flex-1 bg-green-100 bg-opacity-70 rounded-lg p-4">
            <h4 className="text-xl font-bold text-green-700 mb-3">Heroes:</h4>
            <ul className="list-disc pl-4">
              {parseCharacterString(book.PositiveCharacters)?.map((hero, index) => (
                <li key={index} className="text-gray-700 mb-1">
                  {hero}
                </li>
              )) || <li className="text-gray-500 italic">No heroes listed</li>}
            </ul>
          </div>

          {/* Villains Panel */}
          <div className="flex-1 bg-red-100 bg-opacity-70 rounded-lg p-4">
            <h4 className="text-xl font-bold text-red-700 mb-3">Villains:</h4>
            <ul className="list-disc pl-4">
              {parseCharacterString(book.NegativeCharacters)?.map((villain, index) => (
                <li key={index} className="text-gray-700 mb-1">
                  {villain}
                </li>
              )) || <li className="text-gray-500 italic">No villains listed</li>}
            </ul>
          </div>
        </div>        
        
        {/* Chat Section */}
        <div className="bg-white bg-opacity-60 p-4 rounded-lg">
          <h3 className="text-xl font-semibold mb-4">
            Ask about this book
          </h3>
          <ScrollArea className="h-60 mb-4">
            <div
                className={`mb-4 text-left`}
            >
              <span
                className="inline-block p-2 rounded-lg bg-green-100">
                  Welcome, reader! 📚 I know everything about {book.Title} and I'm excited to explore it with you. Ask me anything!
                </span>            
            </div>
            {chat.map((message, index) => (
              <div 
                key={index} 
                className={`mb-4 ${message.role === "user" ? "text-right" : "text-left"}`}
              >
                <span 
                  className={`inline-block p-2 rounded-lg ${
                    message.role === "user" ? "bg-blue-100" : "bg-green-100"
                  }`}
                >
                  {message.content}
                </span>
              </div>
            ))}
          </ScrollArea>
          <form onSubmit={handleAskQuestion} className="flex space-x-2">
            <Input
              type="text"
              placeholder="Ask a question about the book..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              className="flex-grow"
            />
            <Button type="submit">
              <Send className="h-4 w-4 mr-2" /> Ask
            </Button>
          </form>
        </div>
      </CardContent>
    </Card>
  );
};

export default BookDetailCard;