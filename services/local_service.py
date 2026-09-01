# Ollama client handler
import httpx
import json
from core.config import settings
from typing import List, AsyncGenerator

async def call_local_llm(messages: List[dict]) -> str:
    """Calls the local Ollama /api/chat endpoint (non-streaming)."""
    url = f"{settings.ollama_base_url}/api/chat"
    payload = {
        "model": settings.ollama_model,
        "messages": messages,
        "stream": False
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("message", {}).get("content", "")

async def call_local_llm_stream(messages: List[dict]) -> AsyncGenerator[str, None]:
    """Streams response chunks from the local Ollama /api/chat endpoint."""
    url = f"{settings.ollama_base_url}/api/chat"
    payload = {
        "model": settings.ollama_model,
        "messages": messages,
        "stream": True
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        async with client.stream("POST", url, json=payload) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line:
                    data = json.loads(line)
                    chunk = data.get("message", {}).get("content", "")
                    if chunk:
                        yield chunk
                    if data.get("done"):
                        break