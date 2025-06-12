import React from 'react'

const Sidebar = ({ onSelectFolder }) => {
  return (
    <aside className="w-64 bg-gray-800 p-4 shadow-lg flex-shrink-0 h-screen">
      <div className="mt-8">
        <h2 className="text-l font-bold mb-4 px-2 text-white">Explorador</h2>
        <button
          onClick={onSelectFolder}
          className="bg-blue-600 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded-md w-full text-left"
        >
          Seleccionar Carpeta Local
        </button>
        <div className="mt-4 text-gray-300">
          {/* Aquí iría el display del contenido de la carpeta */}
        </div>
      </div>
    </aside>
  )
}

export default Sidebar
