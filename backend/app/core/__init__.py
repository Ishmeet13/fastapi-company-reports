"""
Core application functionality.
"""
from app.core.config import settings
from app.core.logging import get_logger, configure_logging, set_request_id
from app.core.database import get_db, init_db, close_db
from app.core.exceptions import (
    AppException,
    DatabaseError,
    NotFoundError,
    ValidationError,
    BusinessLogicError,
    raise_not_found,
    raise_validation_error,
)

__all__ = [
    "settings",
    "get_logger",
    "configure_logging",
    "set_request_id",
    "get_db",
    "init_db",
    "close_db",
    "AppException",
    "DatabaseError",
    "NotFoundError",
    "ValidationError",
    "BusinessLogicError",
    "raise_not_found",
    "raise_validation_error",
]
