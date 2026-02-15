"""
Health check endpoint
"""
from fastapi import APIRouter
from datetime import datetime
import os

from ..config.settings import settings

router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.API_VERSION,
        "timestamp": datetime.now().isoformat(),
        "knowledge_graph": "present" if os.path.exists(settings.PROJECTS_DATA_PATH) else "missing"
    }