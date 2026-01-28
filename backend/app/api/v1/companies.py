"""
Company API endpoints (version 1).
Demonstrates FastAPI with async patterns (JD requirement!).
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_db, get_logger
from app.schemas import CompanyProfileResponse, CompanyProfileListResponse
from app.services import CompanyService

logger = get_logger(__name__)
router = APIRouter()


@router.get(
    "/companies",
    response_model=CompanyProfileListResponse,
    summary="Get all companies",
    description="Retrieve all company profiles with pagination support",
    tags=["Companies"]
)
async def get_companies(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
) -> CompanyProfileListResponse:
    """
    Retrieve all company profiles (async endpoint).
    
    Args:
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
        db: Database session (injected)
        
    Returns:
        List of company profiles with total count
    """
    logger.info("get_companies_request", skip=skip, limit=limit)
    
    # Fetch companies and count (async!)
    companies = await CompanyService.get_companies(db, skip, limit)
    total = await CompanyService.get_company_count(db)
    
    response = CompanyProfileListResponse(
        companies=[CompanyProfileResponse.model_validate(c) for c in companies],
        total=total
    )
    
    logger.info("get_companies_response", count=len(companies), total=total)
    return response


@router.get(
    "/companies/{company_id}",
    response_model=CompanyProfileResponse,
    summary="Get company by ID",
    description="Retrieve a specific company profile by its ID",
    tags=["Companies"]
)
async def get_company(
    company_id: int,
    db: AsyncSession = Depends(get_db)
) -> CompanyProfileResponse:
    """
    Retrieve a specific company profile (async endpoint).
    
    Args:
        company_id: Company ID to retrieve
        db: Database session (injected)
        
    Returns:
        Company profile
        
    Raises:
        HTTPException 404: If company not found
    """
    logger.info("get_company_request", company_id=company_id)
    
    company = await CompanyService.get_company_by_id(db, company_id)
    response = CompanyProfileResponse.model_validate(company)
    
    logger.info("get_company_response", company_id=company_id)
    return response
