"""
Database seeding script for sample companies.
Run this to populate the database with the 3 required companies.
"""
import asyncio
import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import AsyncSessionLocal, init_db
from app.models import CompanyProfile


async def seed_companies():
    """Seed database with sample companies."""
    
    # Initialize database
    await init_db()
    
    companies_data = [
        {
            "company_name": "Alpine Resource Technologies Ltd.",
            "legal_structure": "Ltd.",
            "year_end": "December 31",
            "address": "450 Mountain View Drive",
            "city": "Calgary",
            "province": "AB",
            "postal_code": "T2P 3B8",
            "industry": "Technology",
            "description": "Resource management technology solutions"
        },
        {
            "company_name": "Novex Health Systems Inc.",
            "legal_structure": "Inc.",
            "year_end": "March 31",
            "address": "789 Healthcare Boulevard",
            "city": "Toronto",
            "province": "ON",
            "postal_code": "M5H 2Y3",
            "industry": "Healthcare",
            "description": "Healthcare technology and systems"
        },
        {
            "company_name": "Stratos Retail Group Corp.",
            "legal_structure": "Corp.",
            "year_end": "December 31",
            "address": "123 Example Street",
            "city": "Vancouver",
            "province": "BC",
            "postal_code": "V6B 2W9",
            "industry": "Retail",
            "description": "Retail operations and management"
        }
    ]
    
    async with AsyncSessionLocal() as session:
        try:
            for data in companies_data:
                company = CompanyProfile(**data)
                session.add(company)
            await session.commit()
            print(f"✅ Seeded {len(companies_data)} companies successfully!")
        except Exception as e:
            print(f"❌ Error seeding database: {e}")
            await session.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(seed_companies())
