"""
SQLAlchemy database models.
All models use type hints and follow Python best practices.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func

from app.core.database import Base


class CompanyProfile(Base):
    """
    Company Profile model representing static company data.
    """
    
    __tablename__ = "company_profiles"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Company identification
    company_name = Column(String(255), nullable=False, unique=True, index=True)
    legal_structure = Column(String(50), nullable=False)
    
    # Fiscal information
    year_end = Column(String(50), nullable=False, comment="Format: 'Month Day'")
    
    # Location information
    address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    province = Column(String(50), nullable=False)
    postal_code = Column(String(20), nullable=False)
    
    # Additional information
    industry = Column(String(100), nullable=True, index=True)
    description = Column(Text, nullable=True)
    
    # Audit fields
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self) -> str:
        return f"<CompanyProfile(id={self.id}, company_name='{self.company_name}')>"
    
    @property
    def full_address(self) -> str:
        """Get formatted full address."""
        return f"{self.address}, {self.city}, {self.province} {self.postal_code}"
