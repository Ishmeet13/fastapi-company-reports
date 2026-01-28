# Company Profile Manager - Backend API

FastAPI-based REST API for generating financial reports with async database operations and comprehensive validation.

## What's Inside?

This backend provides:
- **Company management** - CRUD operations for company profiles
- **Report generation** - Dynamic financial report creation with date calculations
- **Data validation** - Pydantic models ensuring data integrity
- **Async operations** - Non-blocking database queries
- **Auto documentation** - Swagger UI and ReDoc

## Quick Start

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- 5 minutes

### Setup Steps

**1. Navigate to backend directory**
```bash
cd backend
```

**2. Create virtual environment**
```bash
python -m venv venv
```

**3. Activate virtual environment**
```bash
# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

**4. Install dependencies**
```bash
pip install -r requirements.txt
```

This installs:
- FastAPI - Web framework
- Uvicorn - ASGI server
- SQLAlchemy - ORM with async support
- Pydantic - Data validation
- And more...

**5. Initialize database**
```bash
python seed_data.py
```

This creates a SQLite database and adds 3 sample companies.

**6. Start the server**
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The `--reload` flag enables hot-reloading for development.

### Verify It's Working

Visit these URLs in your browser:
- **API Root:** http://localhost:8000/
- **Health Check:** http://localhost:8000/health
- **Interactive Docs:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── main.py                    
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py             
│   │   ├── database.py            
│   │   ├── logging.py             
│   │   └── exceptions.py          
│   ├── models/
│   │   ├── __init__.py
│   │   └── company.py             
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── company.py             
│   ├── services/
│   │   ├── __init__.py
│   │   ├── company_service.py     
│   │   └── report_service.py      
│   └── api/
│       └── v1/
│           ├── __init__.py
│           ├── companies.py       
│           └── reports.py         
├── data/
│   └── company_profiles.db        
├── requirements.txt               
├── seed_data.py                   
├── .env.example                   
└── README.md                      
```

## API Endpoints

### Companies

**Get All Companies**
```bash
GET /api/v1/companies

Response:
{
  "companies": [...],
  "total": 3
}
```

**Get Company by ID**
```bash
GET /api/v1/companies/{id}

Response:
{
  "id": 1,
  "company_name": "Alpine Resource Technologies Ltd.",
  "legal_structure": "Ltd.",
  "year_end": "December 31",
  ...
}
```

### Reports

**Generate Financial Report**
```bash
POST /api/v1/generate-report
Content-Type: application/json

Request:
{
  "company_id": 3,
  "financial_period": "Q2"
}

Response:
{
  "company_name": "Stratos Retail Group Corp.",
  "report_type": "Interim",
  "quarter": "Q2",
  "year_end": "December 31",
  "reporting_period_end": "June 30, 2025",
  "address": "123 Example Street, Vancouver, BC",
  "industry": "Retail",
  "legal_structure": "Corp.",
  "generated_at": "2026-01-27T12:04:51.526075"
}
```

### System

**Health Check**
```bash
GET /health

Response:
{
  "status": "healthy",
  "version": "2.0.0",
  "timestamp": "2026-01-27T12:04:51",
  "database": "connected",
  "uptime_seconds": 123.45
}
```

## Testing with curl

```bash
# Get all companies
curl http://localhost:8000/api/v1/companies

# Get specific company
curl http://localhost:8000/api/v1/companies/1

# Generate Q2 report for company 3
curl -X POST http://localhost:8000/api/v1/generate-report \
  -H "Content-Type: application/json" \
  -d '{"company_id": 3, "financial_period": "Q2"}'

# Check health
curl http://localhost:8000/health
```

## Key Technical Features

### 1. Async/Await Throughout
All database operations use async/await for non-blocking I/O:

```python
async def get_company_by_id(
    db: AsyncSession, 
    company_id: int
) -> CompanyProfile:
    query = select(CompanyProfile).where(CompanyProfile.id == company_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()
```

### 2. Pydantic Validation
Request/response validation with type safety:

```python
class ReportGenerationRequest(BaseModel):
    company_id: int = Field(..., gt=0, description="Company ID")
    financial_period: Literal["Q1", "Q2", "Q3", "Annual"]
```

### 3. Service Layer Pattern
Business logic separated from API routes:

```
API Routes → Services → Database
```

### 4. Error Handling
Custom exceptions with detailed error responses:

```python
{
  "error": "NotFoundError",
  "message": "Company not found",
  "details": {"resource": "Company", "identifier": 999}
}
```

### 5. Structured Logging
JSON-formatted logs with correlation IDs:

```python
logger.info(
    "generating_report",
    company_id=request.company_id,
    financial_period=request.financial_period
)
```

## Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```bash
# Application
APP_NAME=Company Profile Manager API
ENV=development
DEBUG=True

# Database
DATABASE_URL=sqlite+aiosqlite:///./data/company_profiles.db

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=console
```

### Settings Class

All configuration is managed through Pydantic Settings:

```python
# app/core/config.py
class Settings(BaseSettings):
    APP_NAME: str = "Company Profile Manager API"
    ENV: Literal["development", "staging", "production"]
    DEBUG: bool = False
    ...
```

## Database Schema

### CompanyProfile Model

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key (auto-increment) |
| company_name | String(255) | Official company name (unique) |
| legal_structure | String(50) | Ltd., Inc., Corp., etc. |
| year_end | String(50) | Fiscal year end (e.g., "December 31") |
| address | String(255) | Street address |
| city | String(100) | City name |
| province | String(50) | Province/state code |
| postal_code | String(20) | Postal/ZIP code |
| industry | String(100) | Industry sector (nullable) |
| description | Text | Company description (nullable) |
| created_at | DateTime | Record creation timestamp |
| updated_at | DateTime | Last update timestamp |

## Troubleshooting

### Virtual Environment Issues

**Problem:** Commands not found after activation  
**Solution:** 
```bash
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Database Issues

**Problem:** `sqlite3.OperationalError: unable to open database file`  
**Solution:**
```bash
mkdir -p data
python seed_data.py
```

**Problem:** Want to reset the database  
**Solution:**
```bash
rm -rf data
mkdir data
python seed_data.py
```

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'app'`  
**Solution:** Make sure you're running from the backend directory and virtual environment is activated.

### Port Issues

**Problem:** `Address already in use`  
**Solution:**
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
python -m uvicorn app.main:app --reload --port 8001
```

## Development Tools

### Interactive API Testing

Visit http://localhost:8000/docs for Swagger UI where you can:
- See all available endpoints
- Test APIs directly in the browser
- View request/response schemas
- Generate code samples

### Database Inspection

To inspect the SQLite database:

```bash
# Using sqlite3 CLI
sqlite3 data/company_profiles.db

# View tables
.tables

# View company data
SELECT * FROM company_profiles;

# Exit
.quit
```

### Hot Reload

The server automatically reloads when you change code files. Watch the console for:
```
INFO: Detected file change in 'app/...'
INFO: Reloading...
```

## Dependencies

Key packages and their purposes:

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | 0.115.0 | Web framework |
| uvicorn | 0.32.1 | ASGI server |
| sqlalchemy | 2.0.36 | ORM with async support |
| aiosqlite | 0.20.0 | Async SQLite driver |
| pydantic | 2.10.3 | Data validation |
| pydantic-settings | 2.6.1 | Settings management |
| structlog | 24.1.0 | Structured logging |
| python-dateutil | 2.8.2 | Date calculations |

See `requirements.txt` for the complete list.

## Learning Resources

To understand the codebase better:

1. **FastAPI Tutorial:** https://fastapi.tiangolo.com/tutorial/
2. **Pydantic Docs:** https://docs.pydantic.dev/
3. **SQLAlchemy Async:** https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
4. **Python Type Hints:** https://docs.python.org/3/library/typing.html

## Next Steps

Want to extend the application? Try:

- Add more companies
- Implement company creation/update endpoints
- Add authentication
- Add more report types
- Implement filtering and searching
- Add unit tests with pytest

## Code Style

This project follows:
- **PEP 8** - Python style guide
- **Type hints** - 100% coverage
- **Docstrings** - For all public functions
- **Async/await** - For all I/O operations

---

**Questions?** Check the interactive docs at http://localhost:8000/docs

**Need help?** The error messages are detailed - read them carefully!
