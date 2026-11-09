import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Settings:
    app_name: str = os.getenv("JARVIS_APP_NAME", "JARVIS AI")
    provider_name: str = os.getenv("JARVIS_PROVIDER", "mock").lower()
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    memory_path: Path = Path(os.getenv("JARVIS_MEMORY_PATH", "./data/memory.json")).resolve()


settings = Settings()
