# FastAPI endpoints (/generate, /health, /feedback)
from fastapi import APIRouter, Depends
from api.schemas import GenerateRequest, GenerateResponse
from core.orchestrator import process_request
from api.dependencies import verify_api_key

router = APIRouter()

@router.post("/generate", response_model=GenerateResponse, dependencies=[Depends(verify_api_key)])
async def generate(req: GenerateRequest):
    return await process_request(req)

@router.get("/health")
async def health():
    return {"status": "healthy", "service": "slm-smart-router"}