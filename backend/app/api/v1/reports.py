"""
Report generation API endpoints (version 1).
Handles financial report generation with dynamic inputs.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_db, get_logger
from app.schemas import ReportGenerationRequest, ReportGenerationResponse
from app.services import ReportService

logger = get_logger(__name__)
router = APIRouter()


@router.post(
    "/generate-report",
    response_model=ReportGenerationResponse,
    summary="Generate financial report",
    description="Generate structured report output combining company data with reporting period",
    tags=["Reports"]
)
async def generate_report(
    request: ReportGenerationRequest,
    db: AsyncSession = Depends(get_db)
) -> ReportGenerationResponse:
    """
    Generate financial report output (async endpoint).
    
    Combines static company profile data with dynamic user selections
    (company and financial period) to generate a structured JSON output
    ready for downstream processing.
    
    Business Logic:
    - Fetches company data from database
    - Calculates reporting_period_end based on:
      * Company's fiscal year_end (e.g., "December 31")
      * Selected quarter (Q1/Q2/Q3/Annual)
    - Determines report_type (Interim for Q1-Q3, Annual for Annual)
    - Quarter field is included only for Interim reports
    
    Args:
        request: Report generation request containing:
            - company_id: ID of the company
            - financial_period: Q1, Q2, Q3, or Annual
            - include_metadata: Optional flag for extended output
        db: Database session (injected)
        
    Returns:
        Structured report data containing:
        - company_name: Official company name
        - report_type: "Interim" or "Annual"
        - quarter: Quarter identifier (only for Interim)
        - year_end: Fiscal year end date
        - reporting_period_end: Calculated reporting date
        - address: Complete company address
        - Optional: industry, legal_structure, generated_at
        
    Raises:
        HTTPException 404: If company not found
        HTTPException 422: If validation fails
        
    Example Request:
        ```json
        {
            "company_id": 3,
            "financial_period": "Q2",
            "include_metadata": false
        }
        ```
        
    Example Response:
        ```json
        {
            "company_name": "Stratos Retail Group Corp.",
            "report_type": "Interim",
            "quarter": "Q2",
            "year_end": "December 31",
            "reporting_period_end": "June 30, 2024",
            "address": "123 Example Street, Vancouver, BC"
        }
        ```
    """
    logger.info(
        "generate_report_request",
        company_id=request.company_id,
        financial_period=request.financial_period,
        include_metadata=request.include_metadata
    )
    
    # Generate report using service layer (async!)
    report = await ReportService.generate_report(db, request)
    
    logger.info(
        "generate_report_response",
        company_id=request.company_id,
        company_name=report.company_name,
        report_type=report.report_type
    )
    
    return report
