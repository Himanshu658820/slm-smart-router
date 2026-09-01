# Execution pipeline: Cache checks, Session loading, Fallback logic, Telemetry
import time
import uuid
from core.router import decide_route
from services import local_service, cloud_service, cache_service, session_service
from telemetry.logger import log_request
from api.schemas import GenerateRequest, GenerateResponse
from fastapi import HTTPException

async def process_request(req: GenerateRequest) -> GenerateResponse:
    start_time = time.time()
    session_id = req.session_id or str(uuid.uuid4())
    
    # 1. Check Cache
    cached_response = cache_service.get_cached_response(req.prompt)
    if cached_response and not req.force_route:
        latency = (time.time() - start_time) * 1000
        log_request(req.prompt, "CACHE", latency)
        return GenerateResponse(
            response=cached_response, route_used="CACHE", 
            latency_ms=latency, cached=True, session_id=session_id
        )
        
    # 2. Load Session History
    history = session_service.get_session_history(session_id)
    messages = history + [{"role": "user", "content": req.prompt}]
    
    # 3. Route Decision
    target_route = req.force_route or decide_route(req.prompt, history)
    
    # 4. Execute with Fallback
    response_text = ""
    actual_route = target_route
    
    try:
        if target_route == "LOCAL":
            response_text = await local_service.call_local_llm(messages)
        else:
            response_text = await cloud_service.call_cloud_llm(messages)
    except Exception as primary_error:
        # Fallback logic: If primary fails, try the other
        print(f"[Orchestrator] {target_route} failed: {primary_error}. Falling back.")
        actual_route = "CLOUD" if target_route == "LOCAL" else "LOCAL"
        try:
            if actual_route == "LOCAL":
                response_text = await local_service.call_local_llm(messages)
            else:
                response_text = await cloud_service.call_cloud_llm(messages)
        except Exception as fallback_error:
            print(f"[Orchestrator] Fallback {actual_route} also failed: {fallback_error}")
            raise HTTPException(
                status_code=503,
                detail=(
                    f"Both routes failed. "
                    f"PRIMARY ({target_route}): {str(primary_error)[:120]}. "
                    f"FALLBACK ({actual_route}): {str(fallback_error)[:120]}."
                )
            )

    # 5. Save Session & Cache
    session_service.save_to_session(session_id, "user", req.prompt)
    session_service.save_to_session(session_id, "assistant", response_text)
    cache_service.set_cached_response(req.prompt, response_text)
    
    # 6. Telemetry
    latency = (time.time() - start_time) * 1000
    log_request(req.prompt, actual_route, latency)
    
    return GenerateResponse(
        response=response_text, route_used=actual_route, 
        latency_ms=latency, cached=False, session_id=session_id
    )