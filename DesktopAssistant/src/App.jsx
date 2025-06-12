import React, { useState, useEffect } from 'react'
import NavBar from './components/NavBar'
import HeroSection from './components/HeroSection'
import PromptInput from './components/PromptInput'
import OutputDisplay from './components/OutputDisplay'
import Footer from './components/Footer'
import Sidebar from './components/Sidebar'

function App() {
  const [chatHistory, setChatHistory] = useState([])
  const [selectedFolder, setSelectedFolder] = useState(null)

  const handleResponse = (userPrompt, botResponse) => {
    setChatHistory((prev) => [
      ...prev,
      { role: 'user', text: userPrompt },
      { role: 'bot', text: botResponse },
    ])
  }

  useEffect(() => {
    const container = document.getElementById('chat-container')
    if (container) container.scrollTop = container.scrollHeight
  }, [chatHistory])

  const handleFolderSelect = async () => {
    try {
      const directoryHandle = await window.showDirectoryPicker();
      setSelectedFolder(directoryHandle);
      console.log('Carpeta seleccionada:', directoryHandle.name);
    } catch (err) {
      console.error('Error al seleccionar la carpeta:', err);
      if (err.name === 'AbortError') {
        console.log('Selección de carpeta cancelada por el usuario.');
      } else {
        alert('No se pudo acceder a la carpeta. Asegúrate de otorgar los permisos necesarios.');
      }
    }
  };

  return (
    <div className="flex h-screen text-white" style={{ backgroundColor: '#1B1C1D' }}>
      {/* 1. Sidebar fijo a la izquierda, siempre ocupa toda la pantalla */}
      <aside className="w-64 bg-gray-800 shadow-lg flex-shrink-0 h-screen">
        <Sidebar onSelectFolder={handleFolderSelect} />
      </aside>

      {/* 2. Contenedor principal con header, scrollable main y footer */}
      <div className="flex flex-col flex-grow overflow-hidden">
        <NavBar />
        <main className="flex-grow p-4 overflow-y-auto">
          <HeroSection />
          <div className="max-w-4xl mx-auto px-4 my-8">
            <OutputDisplay messages={chatHistory} />
            <PromptInput onResponse={handleResponse} />
          </div>
        </main>
        <Footer />
      </div>
    </div>
  )
}

export default App