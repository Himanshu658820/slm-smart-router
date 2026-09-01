# OpenAI/Groq client handler
import httpx
import json
from core.config import settings
from typing import List, AsyncGenerator

async def call_cloud_llm(messages: List[dict]) -> str:
    """Calls the Groq API (OpenAI-compatible, non-streaming)."""
    headers = {
        "Authorization": f"Bearer {settings.cloud_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": settings.cloud_model,
        "messages": messages,
        "temperature": 0.7
    }
    # Groq is extremely fast, but we keep a 60s timeout for safety
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(settings.cloud_api_url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

async def call_cloud_llm_stream(messages: List[dict]) -> AsyncGenerator[str, None]:
    """Streams response chunks from the Groq API (SSE format)."""
    headers = {
        "Authorization": f"Bearer {settings.cloud_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": settings.cloud_model,
        "messages": messages,
        "temperature": 0.7,
        "stream": True
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        async with client.stream("POST", settings.cloud_api_url, headers=headers, json=payload) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data_str = line[6:]
                    if data_str.strip() == "[DONE]":
                        break
                    try:
                        data = json.loads(data_str)
                        delta = data["choices"][0]["delta"].get("content", "")
                        if delta:
                            yield delta
                    except (json.JSONDecodeError, KeyError, IndexError):
                        continue