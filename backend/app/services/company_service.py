"""
Company service layer with business logic.
Demonstrates async patterns (JD requirement!).
"""
from typing import List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CompanyProfile
from app.core import raise_not_found, get_logger

logger = get_logger(__name__)


class CompanyService:
    """
    Service class for company operations.
    All methods use async/await patterns (JD requirement!).
    """
    
    @staticmethod
    async def get_companies(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[CompanyProfile]:
        """
        Retrieve all companies with pagination (async).
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of company profiles
        """
        logger.info("fetching_companies", skip=skip, limit=limit)
        
        query = select(CompanyProfile).offset(skip).limit(limit)
        result = await db.execute(query)
        companies = result.scalars().all()
        
        logger.info("companies_fetched", count=len(companies))
        return list(companies)
    
    @staticmethod
    async def get_company_count(db: AsyncSession) -> int:
        """Get total count of companies (async)."""
        query = select(func.count()).select_from(CompanyProfile)
        result = await db.execute(query)
        count = result.scalar()
        return count or 0
    
    @staticmethod
    async def get_company_by_id(
        db: AsyncSession,
        company_id: int
    ) -> CompanyProfile:
        """
        Retrieve a specific company by ID (async).
        
        Args:
            db: Database session
            company_id: Company ID to retrieve
            
        Returns:
            Company profile
            
        Raises:
            NotFoundError: If company not found
        """
        logger.info("fetching_company", company_id=company_id)
        
        query = select(CompanyProfile).where(CompanyProfile.id == company_id)
        result = await db.execute(query)
        company = result.scalar_one_or_none()
        
        if not company:
            logger.warning("company_not_found", company_id=company_id)
            raise_not_found("Company", company_id)
        
        logger.info("company_fetched", company_id=company_id, company_name=company.company_name)
        return company
