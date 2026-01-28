"""
Structured logging configuration using structlog.
Provides correlation IDs, JSON formatting, and production-ready logging.
"""
import logging
import sys
import uuid
from typing import Any
from contextvars import ContextVar

import structlog
from structlog.typing import EventDict, WrappedLogger

from app.core.config import settings


# Context variable for request correlation ID
request_id_ctx_var: ContextVar[str] = ContextVar("request_id", default="")


def add_request_id(logger: WrappedLogger, method_name: str, event_dict: EventDict) -> EventDict:
    """Add request ID to log entries."""
    request_id = request_id_ctx_var.get()
    if request_id:
        event_dict["request_id"] = request_id
    return event_dict


def add_app_context(logger: WrappedLogger, method_name: str, event_dict: EventDict) -> EventDict:
    """Add application context to log entries."""
    event_dict["app"] = settings.APP_NAME
    event_dict["version"] = settings.APP_VERSION
    event_dict["env"] = settings.ENV
    return event_dict


def configure_logging() -> None:
    """
    Configure structured logging for the application.
    Uses JSON format in production, console format in development.
    """
    timestamper = structlog.processors.TimeStamper(fmt="iso")
    
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        timestamper,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        add_request_id,
        add_app_context,
    ]
    
    if settings.LOG_FORMAT == "json":
        renderer = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer(
            colors=not settings.is_production,
            exception_formatter=structlog.dev.rich_traceback
        )
    
    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        cache_logger_on_first_use=True,
    )
    
    formatter = structlog.stdlib.ProcessorFormatter(
        processor=renderer,
        foreign_pre_chain=shared_processors,
    )
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    handlers = [console_handler]
    
    if settings.LOG_FILE:
        file_handler = logging.FileHandler(settings.LOG_FILE)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)
    
    logging.basicConfig(
        format="%(message)s",
        handlers=handlers,
        level=getattr(logging, settings.LOG_LEVEL),
    )


def get_logger(name: str = __name__) -> structlog.stdlib.BoundLogger:
    """Get a structured logger instance."""
    return structlog.get_logger(name)


def set_request_id(request_id: str | None = None) -> str:
    """Set request ID for correlation."""
    if not request_id:
        request_id = str(uuid.uuid4())
    request_id_ctx_var.set(request_id)
    return request_id


def get_request_id() -> str:
    """Get current request ID from context."""
    return request_id_ctx_var.get("")
