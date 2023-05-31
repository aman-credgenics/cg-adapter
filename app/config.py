import os
from functools import lru_cache

from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    asyncpg_url: PostgresDsn = PostgresDsn.build(
        scheme="postgres",
        user=os.getenv("ADAPTER_DB_USER",""),
        password=os.getenv("ADAPTER_DB_PASSWORD",""),
        host=os.getenv("ADAPTER_DB_HOST",""),
        port=os.getenv("ADAPTER_DB_PORT",""),
        path=f"/{os.getenv('ADAPTER_DB_NAME') or ''}",
    )


@lru_cache
def get_settings():
    return Settings()

print(os.getenv("ADAPTER_DB_USER",""))

settings = get_settings()