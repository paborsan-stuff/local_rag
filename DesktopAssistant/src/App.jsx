import React, { useState } from 'react'
import NavBar from './components/NavBar'
import HeroSection from './components/HeroSection'
import PromptInput from './components/PromptInput'
import OutputDisplay from './components/OutputDisplay'
import ProductShowcase from './components/ProductShowcase'
import Footer from './components/Footer'

function App() {
  const [responseText, setResponseText] = useState("")

  const handleResponse = (res) => {
    setResponseText(res)
  }

  return (
    <div className="min-h-screen flex flex-col">
      <NavBar />
      <main className="flex-grow">
        <HeroSection />
        <div className="max-w-4xl mx-auto px-4 my-8">
          <PromptInput onResponse={handleResponse} />
          <OutputDisplay response={responseText} />
        </div>
        <ProductShowcase />
      </main>
      <Footer />
    </div>
  )
}

export default App
