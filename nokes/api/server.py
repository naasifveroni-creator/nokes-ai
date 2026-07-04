"""FastAPI server for Nokes"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from nokes import __version__
from nokes.core.engine import NokesEngine
from nokes.models.chat import ChatRequest, ChatResponse, AnalysisRequest, HealthResponse
from nokes.api.config import get_settings


# Global Nokes instance
nokes_engine = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown"""
    # Startup
    global nokes_engine
    settings = get_settings()
    nokes_engine = NokesEngine(
        llm_provider=settings.llm_provider,
        model=settings.llm_model,
        enable_memory=settings.enable_memory,
    )
    logger.info("Nokes server started")
    yield
    # Shutdown
    logger.info("Nokes server shutdown")


def create_app() -> FastAPI:
    """Create and configure FastAPI app"""
    app = FastAPI(
        title="Nokes AI",
        description="Advanced AI Assistant API",
        version=__version__,
        lifespan=lifespan,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routes
    @app.get("/health")
    async def health_check() -> HealthResponse:
        """Health check endpoint"""
        return HealthResponse(version=__version__)

    @app.post("/chat")
    async def chat(request: ChatRequest) -> ChatResponse:
        """Chat endpoint"""
        if not nokes_engine:
            raise HTTPException(status_code=500, detail="Engine not initialized")

        try:
            response = await nokes_engine.chat(
                message=request.message,
                system_prompt=request.system_prompt,
                use_memory=request.use_memory,
            )
            return response
        except Exception as e:
            logger.error(f"Chat error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/analyze")
    async def analyze(request: AnalysisRequest) -> dict:
        """Text analysis endpoint"""
        if not nokes_engine:
            raise HTTPException(status_code=500, detail="Engine not initialized")

        try:
            result = await nokes_engine.analyze_text(
                text=request.text,
                analysis_type=request.analysis_type,
            )
            return result
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/reset")
    async def reset():
        """Reset conversation state"""
        if nokes_engine:
            nokes_engine.clear_history()
            return {"status": "reset"}
        raise HTTPException(status_code=500, detail="Engine not initialized")

    return app


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    app = create_app()
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower(),
    )
