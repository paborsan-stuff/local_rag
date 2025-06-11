import React from 'react'

function OutputDisplay({ response }) {
  return (
    <div className="p-4 border border-gray-300 rounded-md min-h-[100px] bg-white">
      {response ? (
        <p>{response}</p>
      ) : (
        <p className="text-gray-500">The answer will appear here.</p>
      )}
    </div>
  )
}

export default OutputDisplay
