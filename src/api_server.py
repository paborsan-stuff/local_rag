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
    if not prompt:
        return {"error": "No prompt given."}
    top_score, retrieved_docs, llm_response, normal_chat_llm, rag_search  = answer_query(prompt)
    if rag_search:
        return {"answer": f"Document: {top_score}\n\nContent: {retrieved_docs}\n\n{llm_response}\n"}
    
    else:
        return {"answer": f"{normal_chat_llm}"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
