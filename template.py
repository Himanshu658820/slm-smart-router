from pathlib import Path

# Project root
PROJECT_NAME = "slm-smart-router"

# Folder structure
folders = [
    "core",
    "services",
    "api",
    "middleware",
    "telemetry",
    "ui",
]

# Files to create
files = {
    "core/config.py": "# Env vars, model configs, Redis/DB connection strings\n",
    "core/router.py": '# Decision logic ONLY: Evaluates prompt -> returns "LOCAL" or "CLOUD"\n',
    "core/orchestrator.py": "# Execution pipeline: Cache checks, Session loading, Fallback logic, Telemetry\n",

    "services/local_service.py": "# Ollama client handler\n",
    "services/cloud_service.py": "# OpenAI/Gemini client handler\n",
    "services/cache_service.py": "# Semantic cache logic (Redis/Vector DB integration)\n",
    "services/session_service.py": "# Conversation history management (Redis/Postgres)\n",

    "api/routes.py": "# FastAPI endpoints (/generate, /health, /feedback)\n",
    "api/schemas.py": "# Pydantic models\n",
    "api/dependencies.py": "# FastAPI dependencies for Auth, Rate Limiting, DB/Cache session injection\n",

    "middleware/rate_limit.py": "# Security & Traffic control (IP whitelisting, rate limiting)\n",

    "telemetry/logger.py": "# Structured JSON logging\n",
    "telemetry/metrics.py": "# Latency tracking, P50/P95 calculations, Prometheus integration\n",

    "ui/app.py": "# Streamlit/Gradio UI for testing\n",

    "main.py": "# FastAPI app initialization & middleware registration\n",
    "requirements.txt": "",
    ".env.example": "",
    "README.md": "",
}


def create_project():
    root = Path(PROJECT_NAME)

    # Create directories
    for folder in folders:
        (root / folder).mkdir(parents=True, exist_ok=True)

    # Create files
    for file_path, content in files.items():
        file = root / file_path
        file.parent.mkdir(parents=True, exist_ok=True)

        if not file.exists():
            file.write_text(content, encoding="utf-8")

    print(f"\nProject created successfully: {root.resolve()}\n")

    # Print structure
    print(f"{PROJECT_NAME}/")
    print("│")

    for i, folder in enumerate(folders):
        is_last_folder = i == len(folders) - 1
        folder_prefix = "└── " if is_last_folder else "├── "

        print(f"{folder_prefix}{folder}/")

        folder_files = [
            Path(path).name
            for path in files
            if Path(path).parent.as_posix() == folder
        ]

        for j, filename in enumerate(folder_files):
            file_prefix = "    └── " if j == len(folder_files) - 1 else "    ├── "
            print(f"{file_prefix}{filename}")

    # Root files
    print("│")
    root_files = [
        Path(path).name
        for path in files
        if len(Path(path).parts) == 1
    ]

    for i, filename in enumerate(root_files):
        prefix = "└── " if i == len(root_files) - 1 else "├── "
        print(f"{prefix}{filename}")


if __name__ == "__main__":
    create_project()