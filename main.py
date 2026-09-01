# FastAPI app initialization & middleware registration
from fastapi import FastAPI
from middleware.rate_limit import rate_limit_middleware
from api.routes import router

app = FastAPI(
    title="SLM Smart Router",
    description="Cost-optimized routing between Local SLMs and Cloud LLMs",
    version="1.0.0"
)

# Add Middleware
app.middleware("http")(rate_limit_middleware)

# Include Routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)