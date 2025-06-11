import React from 'react'

function Footer() {
  return (
    <footer className="bg-white border-t border-gray-200">
      <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        <div className="flex space-x-4">
          <a href="#" className="text-gray-600 hover:text-gray-900">Privacy</a>
          <a href="#" className="text-gray-600 hover:text-gray-900">Terms</a>
          <a href="#" className="text-gray-600 hover:text-gray-900">Support</a>
        </div>
        <span className="text-gray-600 text-sm">© 2025 DesktopAssistant</span>
      </div>
    </footer>
  )
}

export default Footer
