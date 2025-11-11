import os

from pydantic import BaseModel


class Settings(BaseModel):
    """Application settings loaded from environment variables."""

    llm_model: str = os.getenv("LLM_MODEL", "llama3.1:8b")
    embed_model: str = os.getenv(
        "EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )
    index_dir: str = os.getenv("INDEX_DIR", "var/index")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    # ClinicalTrials.gov API
    ctgov_api_base: str = os.getenv("CTGOV_API_BASE", "https://clinicaltrials.gov/api/v2")
    ctgov_page_size: int = int(os.getenv("CTGOV_PAGE_SIZE", "100"))
    ctgov_timeout_s: int = int(os.getenv("CTGOV_TIMEOUT_S", "30"))


settings = Settings()
