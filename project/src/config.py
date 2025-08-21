from __future__ import annotations
import os
from dotenv import load_dotenv

def load_environment() -> None:
    load_dotenv()

def get_api_key(name: str = 'ALPHAVANTAGE_API_KEY') -> str | None:
    return os.getenv(name)
