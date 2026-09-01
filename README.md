# 🧠 SLM Smart Router

A cost-optimized LLM gateway that **intelligently routes prompts** between a local Small Language Model (SLM via Ollama) and a cloud LLM (Groq) — saving API costs by handling simple requests locally.

---

## ⚡ How It Works

```
User Prompt
    │
    ▼
[Streamlit UI] ──HTTP──▶ [FastAPI Backend :8000]
                               │
                    ┌──────────┼──────────┐
                    ▼          ▼          ▼
              [Cache]    [Router]    [Session]
                              │
               ┌──────────────┴──────────────┐
               ▼                             ▼
        LOCAL (Ollama)               CLOUD (Groq)
        qwen2.5:7b               qwen/qwen3-8b-27b
```

### Routing Logic

| Condition | Route |
|---|---|
| Prompt > 300 characters | ☁️ CLOUD |
| Contains keywords: *analyze, debug, implement, architecture, summarize…* | ☁️ CLOUD |
| Conversation history > 8 turns | ☁️ CLOUD |
| Prompt ≤ 20 chars or simple pattern (*hi, thanks, yes…*) | 🏠 LOCAL |
| Everything else (ambiguous) | 🏠 LOCAL |

If the primary route **fails**, it automatically **falls back** to the other route.

---

## 🛠️ Tech Stack

- **Backend:** FastAPI + Uvicorn
- **Local LLM:** Ollama → `qwen2.5:7b`
- **Cloud LLM:** Groq API → `qwen/qwen3-8b-27b`
- **UI:** Streamlit
- **HTTP Client:** httpx (async)
- **Validation:** Pydantic v2

---

## 📦 Installation

### 1. Clone & install dependencies

```bash
git clone https://github.com/your-username/slm-smart-router.git
cd slm-smart-router
pip install -r requirements.txt
```

### 2. Install & start Ollama with Qwen

```bash
# Install Ollama from https://ollama.com
ollama pull qwen2.5:7b
ollama serve
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Local LLM (Ollama)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b

# Cloud LLM (Groq)
CLOUD_API_URL=https://api.groq.com/openai/v1/chat/completions
CLOUD_API_KEY=your_groq_api_key_here
CLOUD_MODEL=qwen/qwen3-8b-27b

# App Settings
RATE_LIMIT_PER_MINUTE=60
```

> Get a free Groq API key at [console.groq.com](https://console.groq.com)

---

## 🚀 Running the App

You need **two terminals** — one for the backend, one for the UI.

### Terminal 1 — FastAPI Backend

```bash
python main.py
```

Server starts at → **http://localhost:8000**
- Swagger docs → http://localhost:8000/docs
- Health check → http://localhost:8000/health

### Terminal 2 — Streamlit Chat UI

```bash
streamlit run ui/app.py
```

UI opens at → **http://localhost:8501**

---

## 🔌 API Reference

### `POST /generate`

```json
{
  "prompt": "Explain the difference between TCP and UDP",
  "session_id": "optional-uuid",
  "force_route": "LOCAL | CLOUD | null"
}
```

**Response:**

```json
{
  "response": "TCP is connection-oriented...",
  "route_used": "CLOUD",
  "latency_ms": 843.21,
  "cached": false,
  "session_id": "abc-123"
}
```

### `GET /health`

```json
{ "status": "healthy", "service": "slm-smart-router" }
```

---

## 📁 Project Structure

```
slm-smart-router/
├── main.py                  # FastAPI app entry point
├── core/
│   ├── config.py            # Settings (pydantic-settings)
│   ├── router.py            # Routing decision logic
│   └── orchestrator.py      # Full request pipeline
├── api/
│   ├── routes.py            # API endpoints
│   ├── schemas.py           # Pydantic request/response models
│   └── dependencies.py      # Auth dependency injection
├── services/
│   ├── local_service.py     # Ollama client (Qwen local)
│   ├── cloud_service.py     # Groq client (Qwen cloud)
│   ├── cache_service.py     # In-memory prompt cache
│   └── session_service.py   # Conversation history store
├── middleware/
│   └── rate_limit.py        # 60 req/min sliding window
├── telemetry/
│   └── logger.py            # Structured JSON logging
├── ui/
│   └── app.py               # Streamlit chat interface
├── .env                     # Your secrets (git-ignored)
├── .env.example             # Template for .env
└── requirements.txt
```

---

## 🔮 Roadmap

- [ ] Semantic caching (vector similarity instead of exact match)
- [ ] Redis-backed session + cache persistence
- [ ] Streaming responses (SSE)
- [ ] Token-count based routing
- [ ] Dashboard with routing analytics