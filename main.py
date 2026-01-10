from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager
import logging
from typing import Dict, Any

from api.endpoints import router as api_router
from api.security import verify_auth, get_current_user
from core.sovereign import SovereignEngine
from config.settings import Settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = Settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing Rahl AI System...")
    app.state.rahl_engine = SovereignEngine()
    app.state.rahl_engine.initialize()
    logger.info("Rahl AI System Ready")
    yield
    logger.info("Shutting down Rahl AI System...")
    app.state.rahl_engine.shutdown()

app = FastAPI(
    title="Rahl AI API",
    description="Personal Sovereign Intelligence System",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1", dependencies=[Depends(verify_auth)])

@app.get("/")
async def root():
    return {
        "status": "operational",
        "system": "Rahl AI",
        "version": "1.0.0",
        "principle": "Absolute Sovereign Execution"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "compliance": "absolute"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
