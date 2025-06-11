import React from 'react'

function HeroSection() {
  return (
    <section className="pt-20 pb-12 bg-gray-50">
      <div className="max-w-4xl mx-auto text-center">
        <h1 className="text-5xl font-bold mb-4">Your Intelligent Desktop Companion</h1>
        <p className="text-xl text-gray-700 mb-6">Ask anything. Get clean, fast answers.</p>
        <div className="space-x-4">
          <button className="px-6 py-2 bg-blue-600 text-white font-medium rounded-md">Try Now</button>
          <button className="px-6 py-2 bg-transparent border border-blue-600 text-blue-600 font-medium rounded-md">Learn More</button>
        </div>
      </div>
    </section>
  )
}

export default HeroSection
