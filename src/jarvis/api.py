from __future__ import annotations

from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .ai.providers import create_provider
from .config import settings
from .memory.memory_store import MemoryStore

app = FastAPI(title=settings.app_name, version="0.1.0")
provider = create_provider(settings.provider_name, settings.google_api_key)
memory_store = MemoryStore(settings.memory_path)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User input to send to the assistant.")
    user_id: str = Field(default="default-user", description="User identity used for memory.")
    conversation_id: Optional[str] = Field(default=None, description="Optional logical conversation id.")


class ChatResponse(BaseModel):
    response: str
    provider: str
    memory: List[str]


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "app": settings.app_name,
        "provider": settings.provider_name,
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    memory = memory_store.get_memory(request.user_id)
    response_text = provider.generate_response(request.message, {"memory": memory})

    memory_store.remember(request.user_id, request.message)
    memory_store.remember(request.user_id, response_text)

    return ChatResponse(
        response=response_text,
        provider=settings.provider_name,
        memory=memory_store.get_memory(request.user_id),
    )


@app.get("/memory")
def list_memory(user_id: str = "default-user") -> dict:
    return {"user_id": user_id, "memory": memory_store.get_memory(user_id)}
