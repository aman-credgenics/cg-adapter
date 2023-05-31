from fastapi import FastAPI

from app.logging import AppLogger
from app.api.users import router as user_router
from app.ws.session import router as session_router

logger = AppLogger.__call__().get_logger()

app = FastAPI(title="CG_ADAPTER", version="0.01")

app.include_router(user_router)
app.include_router(session_router)


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")
