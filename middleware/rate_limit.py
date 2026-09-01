# Security & Traffic control (IP whitelisting, rate limiting)
from fastapi import Request, HTTPException
import time

_rate_limits = {}

async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    current_time = time.time()
    
    # Clean old entries (older than 1 minute)
    if client_ip in _rate_limits:
        _rate_limits[client_ip] = [t for t in _rate_limits[client_ip] if current_time - t < 60]
    else:
        _rate_limits[client_ip] = []
        
    if len(_rate_limits[client_ip]) >= 60: # 60 requests per minute
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
    _rate_limits[client_ip].append(current_time)
    
    response = await call_next(request)
    return response