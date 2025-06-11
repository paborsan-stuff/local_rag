import React, { useState } from 'react'

function PromptInput({ onResponse }) {
  const [prompt, setPrompt] = useState("")
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!prompt.trim()) return
    setLoading(true)
    try {
      const res = await fetch('/api/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
      })
      const data = await res.json()
      onResponse(data.answer)
    } catch (error) {
      onResponse("Error retrieving answer.")
    }
    setLoading(false)
  }

  return (
    <form className="mb-6" onSubmit={handleSubmit}>
      <textarea
        className="w-full border border-gray-300 p-3 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        rows="4"
        placeholder="Enter your prompt here..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
      <button
        type="submit"
        className="mt-3 px-4 py-2 bg-blue-600 text-white rounded-md"
        disabled={loading}
      >
        {loading ? "Sending..." : "Submit"}
      </button>
    </form>
  )
}

export default PromptInput
