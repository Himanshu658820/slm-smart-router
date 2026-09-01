# Conversation history management (Redis/Postgres)
# Simple in-memory session store. Swap with Redis/Postgres in production.
_sessions = {}

def get_session_history(session_id: str) -> list[dict]:
    return _sessions.get(session_id, [])

def save_to_session(session_id: str, role: str, content: str):
    if session_id not in _sessions:
        _sessions[session_id] = []
    _sessions[session_id].append({"role": role, "content": content})
    # Keep only last 10 turns to prevent context overflow
    _sessions[session_id] = _sessions[session_id][-10:]

def delete_session(session_id: str):
    """Removes a session and all its conversation history."""
    _sessions.pop(session_id, None)