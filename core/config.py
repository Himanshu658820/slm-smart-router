
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Local
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    
    # Cloud (Groq)
    cloud_api_url: str = "https://api.groq.com/openai/v1/chat/completions"
    cloud_api_key: str = ""
    cloud_model: str = "llama-3.3-70b-versatile" # Groq's fastest large model
    
    # App
    rate_limit_per_minute: int = 60

    class Config:
        env_file = ".env"

settings = Settings()