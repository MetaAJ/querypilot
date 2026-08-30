"""Application configuration."""

from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, Field


class Settings(BaseModel):
    database_path: Path = Field(default=Path("data/querypilot.db"), alias="QUERYPILOT_DATABASE")

    model_config = {"populate_by_name": True}


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
