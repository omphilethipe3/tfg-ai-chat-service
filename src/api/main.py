from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import openai

from src.config.settings import settings
from src.ai_agent.agent import chat_with_openai, chat_with_fastmcp

class ChatRequest(BaseModel):
    message: Optional[str] = None
    provider: str = "fastmcp"  # choices: "fastmcp" or "openai"

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

    try:
        if req.provider.lower() == "openai":
            reply = chat_with_openai(req.message)
        else:
            reply = chat_with_fastmcp(req.message)
    except openai.RateLimitError:
        # Convert OpenAI rate limits into HTTP 429
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please try again later."
        )

    return ChatResponse(response=reply)