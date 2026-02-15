"""
Main FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time
import logging

from .config.settings import settings
from .routes import health, projects, weave, evolve, audit

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time-MS"] = str(round(process_time * 1000, 2))
    return response

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(projects.router, prefix="/api/v1", tags=["projects"])
app.include_router(weave.router, prefix="/api/v1", tags=["weave"])
app.include_router(evolve.router, prefix="/api/v1", tags=["evolve"])
app.include_router(audit.router, prefix="/api/v1", tags=["audit"])

# Root endpoint
@app.get("/")
async def root():
    return {
        "name": settings.API_TITLE,
        "version": settings.API_VERSION,
        "status": "operational",
        "docs": "/docs",
        "endpoints": {
            "health": "GET /api/v1/health",
            "projects": "GET /api/v1/projects",
            "projects_by_name": "GET /api/v1/projects/{name}",
            "weave": "POST /api/v1/weave",
            "evolve": "POST /api/v1/evolve",
            "audit": "POST /api/v1/audit"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.loom.api.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )