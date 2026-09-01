# Structured JSON logging
import logging
import json

# Setup basic structured JSON logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("slm_router")

def log_request(prompt: str, route: str, latency_ms: float):
    log_data = {
        "event": "request_processed",
        "prompt_preview": prompt[:50] + "..." if len(prompt) > 50 else prompt,
        "route": route,
        "latency_ms": round(latency_ms, 2)
    }
    logger.info(json.dumps(log_data))