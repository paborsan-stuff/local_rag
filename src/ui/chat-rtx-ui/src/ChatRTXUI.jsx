import React, { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function ChatRTXUI() {
  const [selectedOption, setSelectedOption] = useState("option1");
  const [systemPath, setSystemPath] = useState("");
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");

  const handleRadioChange = (value) => {
    setSelectedOption(value);
  };

  const handlePathChange = (e) => {
    setSystemPath(e.target.value);
  };

  const handleSubmit = () => {
    fetch('/api/rag', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt: prompt })
    })
    .then(res => res.json())
    .then(data => {
      setResponse(data.response);
    })
    .catch(error => console.error("Error:", error));
  };

  return (
    <div className="w-full max-w-md p-8">
      <h1 className="text-2xl font-semibold mb-4">Buscar con RAG</h1>
      <input 
         className="w-full border border-gray-300 p-2 rounded mb-4"
         type="text" 
         placeholder="Ingresa tu prompt" 
         value={prompt} 
         onChange={(e) => setPrompt(e.target.value)} />
      <button 
         className="w-full bg-blue-500 text-white p-2 rounded mb-4" 
         onClick={handleSubmit}>
         Enviar
      </button>
      {response && (
        <div className="p-4 border border-gray-200 rounded">
          Respuesta: {response}
        </div>
      )}
    </div>
  );
}
