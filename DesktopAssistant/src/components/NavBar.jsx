import React from 'react'

function NavBar() {
  return (
    <nav className="fixed top-0 left-0 right-0 bg-white border-b border-gray-200 z-50">
      <div className="max-w-7xl mx-auto px-4 flex justify-between items-center h-16">
        <div className="flex-1 flex justify-center">
          <span className="font-semibold text-xl">DesktopAssistant</span>
        </div>
        <div className="hidden md:flex space-x-8">
          <a href="#" className="text-gray-600 hover:text-gray-900">Home</a>
          <a href="#" className="text-gray-600 hover:text-gray-900">Features</a>
          <a href="#" className="text-gray-600 hover:text-gray-900">Docs</a>
        </div>
      </div>
    </nav>
  )
}

export default NavBar
