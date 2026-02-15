"""
Rate Limiting Middleware
"""
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import time
from collections import defaultdict
from typing import Dict, List, Tuple
import asyncio

from ..config.settings import settings

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiting middleware"""
    
    def __init__(self, app):
        super().__init__(app)
        # Store: client_id -> [(timestamp, request_count)]
        self.request_log: Dict[str, List[float]] = defaultdict(list)
        self.lock = asyncio.Lock()
    
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for non-API routes
        if not request.url.path.startswith("/api/v1/"):
            return await call_next(request)
        
        # Skip rate limiting for health endpoint
        if request.url.path == "/api/v1/health":
            return await call_next(request)
        
        # Get client identifier (API key or IP)
        client_id = getattr(request.state, 'client_id', None)
        if not client_id:
            # Fallback to IP address if no API key
            client_id = request.client.host
        
        async with self.lock:
            # Clean old requests
            current_time = time.time()
            window_start = current_time - settings.RATE_LIMIT_PERIOD
            self.request_log[client_id] = [
                ts for ts in self.request_log[client_id] 
                if ts > window_start
            ]
            
            # Check rate limit
            if len(self.request_log[client_id]) >= settings.RATE_LIMIT_REQUESTS:
                raise HTTPException(
                    status_code=429,
                    detail=f"Rate limit exceeded. Max {settings.RATE_LIMIT_REQUESTS} requests per {settings.RATE_LIMIT_PERIOD} seconds"
                )
            
            # Log this request
            self.request_log[client_id].append(current_time)
        
        # Add rate limit headers
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(settings.RATE_LIMIT_REQUESTS)
        response.headers["X-RateLimit-Remaining"] = str(
            settings.RATE_LIMIT_REQUESTS - len(self.request_log[client_id])
        )
        response.headers["X-RateLimit-Reset"] = str(int(window_start + settings.RATE_LIMIT_PERIOD))
        
        return response