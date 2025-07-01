import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.config.settings import settings
from src.ai_agent.agent import chat_with_openai, chat_with_fastmcp

class ChatRequest(BaseModel):
    message: str
    provider: str = "fastmcp"  

class ChatResponse(BaseModel):
    response: str

app = FastAPI(
    title="TFG AI Chat Service",
    version="0.1.0",
)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.message:
        raise HTTPException(status_code=400, detail="`message` is required")

    if req.provider.lower() == "openai":
        reply = chat_with_openai(req.message)
    else:
        reply = chat_with_fastmcp(req.message)

    return ChatResponse(response=reply)