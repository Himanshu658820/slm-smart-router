# Semantic cache logic (Redis/Vector DB integration)
# Simple in-memory cache. Swap with Redis in production.
_cache = {}

def get_cached_response(prompt: str) -> str | None:
    return _cache.get(prompt)

def set_cached_response(prompt: str, response: str):
    _cache[prompt] = response