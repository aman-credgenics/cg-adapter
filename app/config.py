import os
from functools import lru_cache

from pydantic import BaseSettings, PostgresDsn
from dotenv import load_dotenv

load_dotenv() 

class Settings(BaseSettings):
    asyncpg_url: PostgresDsn = PostgresDsn.build(
        scheme="postgresql+asyncpg",
        user=os.getenv("ADAPTER_DB_USER",""),
        password=os.getenv("ADAPTER_DB_PASSWORD",""),
        host=os.getenv("ADAPTER_DB_HOST",""),
        port=os.getenv("ADAPTER_DB_PORT",""),
        path=f"/{os.getenv('ADAPTER_DB_NAME') or ''}",
    )
    ari_ws = { 
        'connection': {
            'base_url': os.getenv("ARI_URI",""),
            'username': os.getenv("ARI_USERNAME",""),
            'password': os.getenv("ARI_PASSWORD","")},
        'reconnection_delay': os.getenv("ARI_RECONNECTION_DELAY_MS",10),
        'startup_connection_tries': os.getenv("ARI_STARTUP_CONNECTION_TRIES",1),
        'startup_connection_delay': os.getenv("ARI_STARTUP_CONNECTION_DELAY_MS",10),
        'apps': os.getenv("ARI_APPS", ""),
    }

    # class Config:
    #     fields = {
    #         'asyncpg_url': {
    #             'env': 'my_auth_key',
    #         },
    #         'redis_dsn': {
    #             'env': ['service_redis_dsn', 'redis_url']
    #         }
    #     }


@lru_cache
def get_settings():
    return Settings(_env_file='.env', _env_file_encoding='utf-8')

print(os.getenv("ADAPTER_DB_USER",""))

settings = get_settings()

