# Company Profile Manager & Report Generator

A full-stack web application for generating financial reports with dynamic company and period selection. Built as a demonstration of modern web development practices using Python, FastAPI, React, and TypeScript.

## What Does This Do?

This application helps you generate financial reports for companies by:
- Selecting a company from a dropdown list
- Choosing a financial period (Q1, Q2, Q3, or Annual)
- Generating a properly formatted JSON report
- Downloading the report for your records

Simple, clean, and effective.

## Live Demo

Once you start the servers:
- **Frontend:** http://localhost:3000 (the app you interact with)
- **API Documentation:** http://localhost:8000/docs (interactive API testing)
- **Health Check:** http://localhost:8000/health

## Quick Start

### Prerequisites

Before you begin, make sure you have:
- **Python 3.11+** installed ([Download here](https://www.python.org/downloads/))
- **Node.js 18+** and npm installed ([Download here](https://nodejs.org/))
- A terminal/command line
- 5 minutes of your time

### Installation & Setup

**Step 1: Clone the repository**
```bash
git clone <your-repo-url>
cd assignment2
```

**Step 2: Start the Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python seed_data.py
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Step 3: Start the Frontend** (in a new terminal)
```bash
cd frontend
npm install
npm run dev
```

**Step 4: Open Your Browser**

Visit http://localhost:3000 and you're ready to go!

## Sample Data

The application comes pre-loaded with three companies:

| Company | Industry | Location | Year-End |
|---------|----------|----------|----------|
| **Alpine Resource Technologies Ltd.** | Technology | Calgary, AB | December 31 |
| **Novex Health Systems Inc.** | Healthcare | Toronto, ON | March 31 |
| **Stratos Retail Group Corp.** | Retail | Vancouver, BC | December 31 |

## Features

### For Users
- Clean, intuitive interface
- Real-time report generation
- JSON download functionality
- Visual report preview
- Responsive design

### For Developers
- RESTful API with FastAPI
- Type-safe with Pydantic & TypeScript
- Async/await patterns throughout
- Comprehensive error handling
- Auto-generated API documentation
- SQLite database (no setup required)

## Project Structure

```
assignment2/
├── README.md                 ← You are here
├── backend/                  ← Python/FastAPI backend
│   ├── README.md            ← Backend documentation
│   ├── app/
│   │   ├── main.py          ← Application entry point
│   │   ├── core/            ← Configuration & utilities
│   │   ├── models/          ← Database models
│   │   ├── schemas/         ← Request/response validation
│   │   ├── services/        ← Business logic
│   │   └── api/v1/          ← API endpoints
│   ├── requirements.txt
│   └── seed_data.py         ← Database initialization
└── frontend/                 ← React/TypeScript frontend
    ├── README.md            ← Frontend documentation
    ├── src/
    │   ├── App.tsx          ← Main component
    │   ├── types/           ← TypeScript definitions
    │   └── utils/           ← API client & helpers
    └── package.json
```

## Technology Stack

**Backend:**
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation using Python type hints
- **SQLAlchemy** - SQL toolkit with async support
- **SQLite** - Lightweight database (no installation needed)

**Frontend:**
- **React 18** - UI library
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **Vite** - Fast build tool

## Documentation

- **Backend API:** See [backend/README.md](backend/README.md)
- **Frontend:** See [frontend/README.md](frontend/README.md)
- **API Docs:** http://localhost:8000/docs (when backend is running)

## Testing the Application

### Using the Web Interface
1. Open http://localhost:3000
2. Select a company (e.g., "Stratos Retail Group Corp.")
3. Select a period (e.g., "Q2 (Quarter 2)")
4. Click "Generate Report"
5. View the JSON output
6. Click "Download JSON" to save

### Using the API Directly
```bash
# Get all companies
curl http://localhost:8000/api/v1/companies

# Generate a report
curl -X POST http://localhost:8000/api/v1/generate-report \
  -H "Content-Type: application/json" \
  -d '{
    "company_id": 3,
    "financial_period": "Q2"
  }'
```

### Using Interactive API Docs
Visit http://localhost:8000/docs for a Swagger UI interface where you can test all endpoints interactively.

## Common Issues & Solutions

**Problem:** Backend won't start - "ModuleNotFoundError"  
**Solution:** Make sure you activated the virtual environment: `source venv/bin/activate`

**Problem:** Frontend can't connect to backend  
**Solution:** Ensure backend is running on port 8000 and check http://localhost:8000/health

**Problem:** Port 8000 already in use  
**Solution:** Kill the process using the port:
```bash
# Mac/Linux
lsof -ti:8000 | xargs kill -9

# Or use a different port
python -m uvicorn app.main:app --reload --port 8001
```

**Problem:** Database not found  
**Solution:** Run the seed script: `python seed_data.py` from the backend directory

## Learning Resources

This project demonstrates:
- RESTful API design
- Async Python programming
- React state management
- TypeScript type safety
- Database operations with SQLAlchemy
- Frontend-backend integration

## API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/api/v1/companies` | List all companies |
| GET | `/api/v1/companies/{id}` | Get specific company |
| POST | `/api/v1/generate-report` | Generate financial report |
| GET | `/docs` | Interactive API documentation |

## What Makes This Different?

Unlike typical CRUD applications, this project showcases:
- **Business logic** - Date calculations for fiscal periods
- **Data validation** - Pydantic models with constraints
- **Type safety** - Full TypeScript + Python type hints
- **Production patterns** - Service layer, error handling, logging
- **Developer experience** - Hot reload, interactive docs, clear structure

## Questions?

Check out the detailed documentation:
- Backend questions? See [backend/README.md](backend/README.md)
- Frontend questions? See [frontend/README.md](frontend/README.md)
- API usage? Visit http://localhost:8000/docs

## License

This is a demonstration project created for educational purposes.

---

**Built by:** Ishmeet Singh Arora  
**Stack:** Python • FastAPI • Pydantic • React • TypeScript • SQLAlchemy  
**Purpose:** Demonstration of full-stack development with modern technologies
