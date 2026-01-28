"""
FastAPI Main Application
Production-ready ML Engineering solution for Company Profile Manager
"""
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime

from app.core import (
    settings,
    configure_logging,
    get_logger,
    set_request_id,
    init_db,
    close_db,
    AppException,
)
from app.api.v1 import companies, reports
from app.schemas import HealthCheckResponse

# Configure structured logging
configure_logging()
logger = get_logger(__name__)

# Track application start time
start_time = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    # Startup
    logger.info("application_starting", env=settings.ENV)
    await init_db()
    logger.info("application_started")
    
    yield
    
    # Shutdown
    logger.info("application_shutting_down")
    await close_db()
    logger.info("application_stopped")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production-ready Company Profile Manager API with Python + FastAPI + Pydantic",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request ID middleware
@app.middleware("http")
async def add_request_id_middleware(request: Request, call_next):
    """Add correlation ID to all requests."""
    request_id = request.headers.get("X-Request-ID") or set_request_id()
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


# Exception handlers
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    """Handle application exceptions."""
    logger.error(
        "application_exception",
        error=exc.message,
        status_code=exc.status_code,
        details=exc.details
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "details": exc.details,
        }
    )


# Include routers
app.include_router(
    companies.router,
    prefix=settings.API_V1_PREFIX,
    tags=["Companies"]
)
app.include_router(
    reports.router,
    prefix=settings.API_V1_PREFIX,
    tags=["Reports"]
)


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENV,
        "docs": "/docs",
        "health": "/health",
        "message": "Company Profile Manager API - Python + FastAPI + Pydantic"
    }


# Health check endpoint
@app.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring."""
    uptime = time.time() - start_time
    
    return HealthCheckResponse(
        status="healthy",
        version=settings.APP_VERSION,
        timestamp=datetime.utcnow(),
        database="connected",
        uptime_seconds=uptime
    )
