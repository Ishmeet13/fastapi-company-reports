"""
Custom exceptions and error handling for production robustness.
"""
from typing import Any
from fastapi import status
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standard error response model."""
    error: str
    message: str
    details: dict[str, Any] | None = None
    request_id: str | None = None


class AppException(Exception):
    """Base exception for application-specific errors."""
    
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: dict[str, Any] | None = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class DatabaseError(AppException):
    """Exception for database-related errors."""
    def __init__(self, message: str = "Database operation failed", details: dict[str, Any] | None = None):
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR, details)


class NotFoundError(AppException):
    """Exception for resource not found errors."""
    def __init__(self, resource: str, identifier: Any):
        super().__init__(
            f"{resource} not found",
            status.HTTP_404_NOT_FOUND,
            {"resource": resource, "identifier": identifier}
        )


class ValidationError(AppException):
    """Exception for validation errors."""
    def __init__(self, message: str, field: str | None = None, details: dict[str, Any] | None = None):
        error_details = details or {}
        if field:
            error_details["field"] = field
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_ENTITY, error_details)


class BusinessLogicError(AppException):
    """Exception for business logic errors."""
    def __init__(self, message: str, details: dict[str, Any] | None = None):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, details)


def raise_not_found(resource: str, identifier: Any) -> None:
    """Raise NotFoundError with standardized message."""
    raise NotFoundError(resource, identifier)


def raise_validation_error(message: str, field: str | None = None, details: dict[str, Any] | None = None) -> None:
    """Raise ValidationError with details."""
    raise ValidationError(message, field, details)
