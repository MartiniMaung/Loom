"""
Main FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import time
import logging
from pathlib import Path

from .config.settings import settings
from .routes import health, projects, weave, evolve, audit, admin
from .middleware.auth import APIKeyMiddleware
from .middleware.rate_limit import RateLimitMiddleware

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

# Custom middlewares (order matters!)
if settings.ENABLE_API_KEYS:
    app.add_middleware(APIKeyMiddleware)

if settings.RATE_LIMIT_ENABLED:
    app.add_middleware(RateLimitMiddleware)

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
app.include_router(admin.router, prefix="/api/v1", tags=["admin"])

# Serve static files
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    logger.info(f"Serving static files from {static_dir}")

# Dashboard route
@app.get("/dashboard", include_in_schema=False)
async def get_dashboard():
    """Serve the dashboard HTML"""
    dashboard_path = static_dir / "index.html"
    if dashboard_path.exists():
        return FileResponse(dashboard_path)
    return {"error": "Dashboard not found"}

# Root endpoint
@app.get("/")
async def root():
    return {
        "name": settings.API_TITLE,
        "version": settings.API_VERSION,
        "status": "operational",
        "docs": "/docs",
        "dashboard": "/dashboard",
        "authentication": "API Key required (except /health, /docs, /dashboard)",
        "rate_limiting": f"{settings.RATE_LIMIT_REQUESTS} requests per {settings.RATE_LIMIT_PERIOD}s",
        "demo_key": "POST /api/v1/auth/demo",
        "admin": "/api/v1/admin/keys (admin token required)",
        "endpoints": {
            "health": "GET /api/v1/health (public)",
            "projects": "GET /api/v1/projects (auth required)",
            "weave": "POST /api/v1/weave (auth required)",
            "evolve": "POST /api/v1/evolve (auth required)",
            "audit": "POST /api/v1/audit (auth required)",
            "auth_demo": "POST /api/v1/auth/demo (public)",
            "admin_keys": "POST/GET/DELETE /api/v1/admin/keys (admin token required)"
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