from enum import Enum
from typing import Optional

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMProvider(str, Enum):
    OPENAI = "openai"
    OPENROUTER = "openrouter"
    GEMINI = "gemini"
    HUGGINGFACE = "huggingface"
    AZURE = "azure"


class DBProvider(str, Enum):
    MONGODB = "mongodb"
    SQLITE = "sqlite"
    JSON = "json"
    INMEMORY = "inmemory"


class Setting(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # LLM Configuration
    LLM_PROVIDER: LLMProvider = LLMProvider.AZURE
    LLM_TEMPERATURE: float = 0.2

    # Tools configuration
    TOOL_CALL_LIMIT: int = 3

    # Memory configuration
    NUM_HISTORY_RUNS: int = 3

    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"

    # OpenRouter
    OPENROUTER_API_KEY: Optional[str] = None
    OPENROUTER_MODEL: str = "openai/gpt-oss-20b:free"

    # Gemini
    GOOGLE_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-1.5-flash"

    # HuggingFace
    HUGGINGFACE_API_KEY: Optional[str] = None
    HUGGINGFACE_MODEL: str = "meta-llama/Meta-Llama-3-8B-Instruct"

    # Azure OpenAI
    AZURE_API_KEY: Optional[str] = None
    AZURE_ENDPOINT: Optional[str] = None
    AZURE_DEPLOYMENT: Optional[str] = None
    AZURE_MODEL: str = "gpt-4o-mini"
    AZURE_API_VERSION: str = "2024-10-21"

    # Database
    DB_PROVIDER: DBProvider = DBProvider.SQLITE
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB: str = "chat_history"
    SQLITE_FILE: str = "chat_history.db"
    JSON_FILE: str = "chat_history"

    @field_validator("LLM_PROVIDER", mode="before")
    @classmethod
    def normalize_provider(cls, value):
        if isinstance(value, str):
            return value.strip().lower()
        return value

    @field_validator("DB_PROVIDER", mode="before")
    @classmethod
    def normalize_db_provider(cls, value):
        if isinstance(value, str):
            return value.strip().lower()
        return value
