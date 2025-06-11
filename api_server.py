from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from rag import answer_query

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/ask")
async def ask(request: Request):
    body = await request.json()
    prompt = body.get("prompt")
    # El prompt recibido proviene de la UI en DesktopAssistant/src/components/PromptInput.jsx
    if not prompt:
        return {"error": "No se proporcionó prompt."}
    answer = answer_query(prompt)
    return {"answer": answer}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
