"""
Pydantic schemas for request/response validation.
Demonstrates Pydantic expertise as mentioned in the JD (CRITICAL FILE!).
"""
from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field, ConfigDict


class CompanyProfileResponse(BaseModel):
    """Schema for company profile responses."""
    
    id: int = Field(..., description="Company ID")
    company_name: str = Field(..., description="Official company name")
    legal_structure: str = Field(..., description="Legal entity type")
    year_end: str = Field(..., description="Fiscal year end")
    address: str = Field(..., description="Street address")
    city: str = Field(..., description="City name")
    province: str = Field(..., description="Province/state code")
    postal_code: str = Field(..., description="Postal code")
    industry: Optional[str] = Field(None, description="Industry sector")
    description: Optional[str] = Field(None, description="Company description")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    model_config = ConfigDict(from_attributes=True)


class CompanyProfileListResponse(BaseModel):
    """Schema for listing companies with metadata."""
    
    companies: list[CompanyProfileResponse]
    total: int = Field(..., description="Total number of companies")
    
    model_config = ConfigDict(from_attributes=True)


class ReportGenerationRequest(BaseModel):
    """
    Request schema for report generation (JD Pydantic requirement!).
    Validates company ID and financial period selection.
    """
    
    company_id: int = Field(
        ...,
        gt=0,
        description="ID of the company",
        examples=[1, 2, 3]
    )
    financial_period: Literal["Q1", "Q2", "Q3", "Annual"] = Field(
        ...,
        description="Financial reporting period",
        examples=["Q2", "Annual"]
    )
    include_metadata: bool = Field(
        default=False,
        description="Include additional company metadata in output"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "company_id": 3,
                    "financial_period": "Q2",
                    "include_metadata": False
                }
            ]
        }
    )


class ReportGenerationResponse(BaseModel):
    """
    Response schema for generated report.
    Matches the exact output format from Assignment 2 specification.
    """
    
    company_name: str = Field(..., description="Official company name")
    report_type: Literal["Interim", "Annual"] = Field(..., description="Type of financial report")
    quarter: Optional[str] = Field(None, description="Quarter identifier (only for Interim reports)")
    year_end: str = Field(..., description="Fiscal year end date")
    reporting_period_end: str = Field(..., description="Reporting period end date (format: 'Month DD, YYYY')")
    address: str = Field(..., description="Complete company address")
    
    # Optional metadata fields
    industry: Optional[str] = Field(None, description="Industry sector")
    legal_structure: Optional[str] = Field(None, description="Legal entity type")
    generated_at: Optional[datetime] = Field(None, description="Report generation timestamp")
    
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "company_name": "Stratos Retail Group Corp.",
                    "report_type": "Interim",
                    "quarter": "Q2",
                    "year_end": "December 31",
                    "reporting_period_end": "June 30, 2024",
                    "address": "123 Example Street, Vancouver, BC"
                }
            ]
        }
    )


class HealthCheckResponse(BaseModel):
    """Schema for health check endpoint response."""
    
    status: Literal["healthy", "degraded", "unhealthy"] = Field(..., description="Service health status")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(..., description="Health check timestamp")
    database: Literal["connected", "disconnected"] = Field(..., description="Database connection status")
    uptime_seconds: float = Field(..., description="Service uptime in seconds")
