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
      onResponse(prompt, data.answer)
    } catch (error) {
      onResponse(prompt, "Error retrieving answer.")
    }
    setPrompt("")
    setLoading(false)
  }

  return (
    <form className="mb-6" onSubmit={handleSubmit}>
      <textarea
        className="w-full bg-[#2d2d2d] text-white p-3 rounded-xl border border-gray-600 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 leading-relaxed"
        placeholder="Escribe tu mensaje..."
        value={prompt}
        onChange={(e) => {
          setPrompt(e.target.value);
          e.target.style.height = 'auto';         // reset height
          e.target.style.height = `${e.target.scrollHeight}px`; // set to scroll height
        }}
        rows={1}
      />
      <button
        type="submit"
        className="mt-3 px-4 py-2 bg-blue-600 text-white rounded-md"
        disabled={loading}
      >
        {loading ? "Sending..." : "Send"}
      </button>
    </form>
  )
}

export default PromptInput