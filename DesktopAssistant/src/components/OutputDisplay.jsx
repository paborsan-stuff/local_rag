import React from 'react'

function OutputDisplay({ messages }) {
  return (
    <div
      id="chat-container"
      className="flex-grow overflow-y-auto px-4 py-6 space-y-4 scroll-smooth"
      style={{ backgroundColor: '#1B1C1D' }}
    >
      {messages.length === 0 && (
        <p className="text-gray-400 text-center">What are we searching today?</p>
      )}

      {messages.map((msg, idx) => (
        <div
          key={idx}
          className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
        >
          {msg.role === 'bot' && (
            <div className="mr-2 mt-1">
              <span className="text-blue-400">🫆</span>
            </div>
          )}
          <div
            className={`px-5 py-3 max-w-[75%] text-base leading-relaxed font-light rounded-2xl whitespace-pre-line shadow-sm ${
              msg.role === 'user'
                ? 'bg-[#2d2d2d] text-white ml-auto'
                : 'bg-[#1f1f1f] text-white mr-auto'
            }`}
          >
            {msg.text}
          </div>
        </div>
      ))}
    </div>
  )
}

export default OutputDisplay