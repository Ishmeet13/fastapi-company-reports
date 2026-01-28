"""
Report generation service with business logic.
Handles date calculations and report formatting.
"""
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import ReportGenerationRequest, ReportGenerationResponse
from app.services.company_service import CompanyService
from app.core import get_logger

logger = get_logger(__name__)


class ReportService:
    """
    Service class for report generation operations.
    Handles all report-related business logic.
    """
    
    @staticmethod
    def parse_year_end(year_end: str) -> tuple[int, int]:
        """Parse year_end string to extract month and day."""
        date_obj = datetime.strptime(year_end, "%B %d")
        return date_obj.month, date_obj.day
    
    @staticmethod
    def calculate_reporting_period_end(year_end: str, quarter: str) -> str:
        """
        Calculate reporting period end date based on fiscal year end and quarter.
        
        Business Logic:
        - Annual: Returns the fiscal year end date
        - Q1: Fiscal year end + 3 months
        - Q2: Fiscal year end + 6 months
        - Q3: Fiscal year end + 9 months
        
        Args:
            year_end: Company's fiscal year end (e.g., "December 31")
            quarter: Financial period (Q1, Q2, Q3, or Annual)
            
        Returns:
            Formatted reporting period end date (e.g., "June 30, 2024")
        """
        logger.debug("calculating_reporting_period", year_end=year_end, quarter=quarter)
        
        # Use current year for calculation
        current_year = 2024
        
        # Parse year end month and day
        year_end_month, year_end_day = ReportService.parse_year_end(year_end)
        
        # Create year end date
        year_end_date = datetime(current_year, year_end_month, year_end_day)
        
        # Calculate reporting date based on quarter
        if quarter == "Annual":
            reporting_date = year_end_date
        elif quarter == "Q1":
            reporting_date = year_end_date + relativedelta(months=3)
        elif quarter == "Q2":
            reporting_date = year_end_date + relativedelta(months=6)
        elif quarter == "Q3":
            reporting_date = year_end_date + relativedelta(months=9)
        else:
            raise ValueError(f"Invalid quarter: {quarter}")
        
        # Format as "Month Day, Year"
        formatted_date = reporting_date.strftime("%B %d, %Y")
        
        logger.debug(
            "reporting_period_calculated",
            year_end=year_end,
            quarter=quarter,
            reporting_period_end=formatted_date
        )
        
        return formatted_date
    
    @staticmethod
    def format_full_address(address: str, city: str, province: str) -> str:
        """Format complete address from components."""
        return f"{address}, {city}, {province}"
    
    @staticmethod
    async def generate_report(
        db: AsyncSession,
        request: ReportGenerationRequest
    ) -> ReportGenerationResponse:
        """
        Generate financial report output (async).
        
        This method:
        1. Fetches company data from database
        2. Calculates reporting period end date
        3. Determines report type (Interim vs Annual)
        4. Formats all data according to specification
        
        Args:
            db: Database session
            request: Report generation request
            
        Returns:
            Structured report data
            
        Raises:
            NotFoundError: If company not found
        """
        logger.info(
            "generating_report",
            company_id=request.company_id,
            financial_period=request.financial_period
        )
        
        # Fetch company profile (async!)
        company = await CompanyService.get_company_by_id(db, request.company_id)
        
        # Determine report type
        report_type = "Annual" if request.financial_period == "Annual" else "Interim"
        
        # Calculate reporting period end
        reporting_period_end = ReportService.calculate_reporting_period_end(
            company.year_end,
            request.financial_period
        )
        
        # Format address
        full_address = ReportService.format_full_address(
            company.address,
            company.city,
            company.province
        )
        # Build base response
        response_data = {
            "company_name": company.company_name,
            "report_type": report_type,
            "year_end": company.year_end,
            "reporting_period_end": reporting_period_end,
            "address": full_address,
            "industry": company.industry,              # ← ADD THIS
            "legal_structure": company.legal_structure, # ← ADD THIS
            "generated_at": datetime.utcnow(),          # ← ADD THIS
        }

        # Add quarter field only for interim reports
        if report_type == "Interim":
            response_data["quarter"] = request.financial_period
        # # Build base response
        # response_data = {
        #     "company_name": company.company_name,
        #     "report_type": report_type,
        #     "year_end": company.year_end,
        #     "reporting_period_end": reporting_period_end,
        #     "address": full_address,
        # }
        
        # # Add quarter field only for interim reports
        # if report_type == "Interim":
        #     response_data["quarter"] = request.financial_period
        
        # # Add optional metadata if requested
        # if request.include_metadata:
        #     response_data["industry"] = company.industry
        #     response_data["legal_structure"] = company.legal_structure
        #     response_data["generated_at"] = datetime.utcnow()
        
        logger.info(
            "report_generated",
            company_id=request.company_id,
            company_name=company.company_name,
            report_type=report_type
        )
        
        return ReportGenerationResponse(**response_data)
