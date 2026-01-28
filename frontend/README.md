# Company Profile Manager - Frontend

Modern React application with TypeScript for generating financial reports through an intuitive user interface.

## What's This?

A clean, responsive web interface that lets users:
- Select companies from a dropdown
- Choose financial periods (Q1, Q2, Q3, Annual)
- Generate formatted financial reports
- Preview JSON output in the browser
- Download reports as JSON files

## Quick Start

### Prerequisites

- Node.js 18 or higher
- npm (comes with Node.js)
- Backend API running on http://localhost:8000

### Setup Steps

**1. Navigate to frontend directory**
```bash
cd frontend
```

**2. Install dependencies**
```bash
npm install
```

This will install React, TypeScript, Vite, Tailwind CSS, and other dependencies. Takes about 1-2 minutes.

**3. Start development server**
```bash
npm run dev
```

**4. Open in browser**

Visit http://localhost:3000 and you should see the application!

## Project Structure

```
frontend/
├── src/
│   ├── main.tsx               # Application entry point
│   ├── App.tsx                # Main component
│   ├── index.css              # Global styles (Tailwind)
│   ├── types/
│   │   └── index.ts           # TypeScript type definitions
│   └── utils/
│       ├── api.ts             # API client (Axios)
│       └── download.ts        # File download utility
├── public/                    # Static assets
├── index.html                 # HTML template
├── package.json               # Dependencies
├── tsconfig.json              # TypeScript config
├── vite.config.ts             # Vite configuration
├── tailwind.config.js         # Tailwind CSS config
└── README.md                  # This file
```

## Features

### User Interface
- **Responsive design** - Works on desktop, tablet, and mobile
- **Real-time validation** - Disabled submit button until form is complete
- **Loading states** - Visual feedback during API calls
- **Error handling** - Clear error messages
- **Status indicator** - Shows "3 Companies Loaded" when connected

### User Experience
- **Instant feedback** - JSON appears immediately after generation
- **Syntax highlighting** - Pretty-printed JSON output
- **One-click download** - Download button for generated reports
- **Smooth animations** - Tailwind CSS transitions

### Developer Experience
- **Type safety** - Full TypeScript coverage
- **Hot reload** - Changes appear instantly
- **Clean code** - Well-organized and commented
- **Error boundaries** - Graceful error handling

## Technology Stack

| Technology | Purpose |
|------------|---------|
| **React 18** | UI library with hooks |
| **TypeScript** | Type-safe JavaScript |
| **Vite** | Fast build tool and dev server |
| **Tailwind CSS** | Utility-first CSS framework |
| **Axios** | HTTP client for API calls |

## Available Scripts

```bash
# Start development server (with hot reload)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Type check without building
npm run type-check

# Lint code
npm run lint
```

## How It Works

### 1. Application Flow

```
User selects company + period
         ↓
Validates inputs
         ↓
Sends POST request to backend API
         ↓
Receives JSON response
         ↓
Displays formatted output
         ↓
User clicks download
         ↓
Saves as .json file
```

### 2. Component Structure

```typescript
App.tsx
├── State Management (useState hooks)
├── API Integration (useEffect)
├── Form Section
│   ├── Company Dropdown
│   ├── Period Dropdown
│   └── Generate Button
├── Output Section
│   ├── JSON Display (syntax-highlighted)
│   ├── Report Metadata
│   └── Download Button
└── Footer
```

### 3. Type Definitions

All data types are defined in `src/types/index.ts`:

```typescript
export interface CompanyProfile {
  id: number;
  company_name: string;
  legal_structure: string;
  year_end: string;
  address: string;
  // ... more fields
}

export interface ReportGenerationRequest {
  company_id: number;
  financial_period: FinancialPeriod;
}

export interface ReportGenerationResponse {
  company_name: string;
  report_type: "Interim" | "Annual";
  quarter?: string;
  // ... more fields
}
```

## API Integration

### Fetching Companies

```typescript
// src/utils/api.ts
export const fetchCompanies = async (): Promise<CompanyProfile[]> => {
  const response = await api.get<{ companies: CompanyProfile[] }>(
    '/api/v1/companies'
  );
  return response.data.companies;
};
```

### Generating Reports

```typescript
export const generateReport = async (
  request: ReportGenerationRequest
): Promise<ReportGenerationResponse> => {
  const response = await api.post<ReportGenerationResponse>(
    '/api/v1/generate-report',
    request
  );
  return response.data;
};
```

### Error Handling

```typescript
try {
  const data = await generateReport({ company_id, financial_period });
  setReportData(data);
  setError(null);
} catch (err) {
  setError('Failed to generate report. Please try again.');
  console.error('API Error:', err);
}
```

## Styling with Tailwind

The app uses Tailwind CSS for styling. Key classes used:

```css
/* Gradient background */
bg-gradient-to-br from-blue-50 to-indigo-100

/* Card styling */
bg-white rounded-xl shadow-lg

/* Button states */
bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-300

/* Responsive design */
lg:col-span-2  /* Different layout on large screens */
```

## Troubleshooting

### Development Server Issues

**Problem:** `npm run dev` fails  
**Solution:**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Backend Connection Issues

**Problem:** "Failed to fetch companies"  
**Solution:**
1. Check if backend is running: http://localhost:8000/health
2. Check browser console for CORS errors
3. Verify API URL in `src/utils/api.ts` is correct (`http://localhost:8000`)

### TypeScript Errors

**Problem:** Type errors in VS Code  
**Solution:**
```bash
# Restart TypeScript server in VS Code
# Command Palette (Cmd+Shift+P) → "TypeScript: Restart TS Server"

# Or check types manually
npm run type-check
```

### Build Issues

**Problem:** Production build fails  
**Solution:**
```bash
# Clear Vite cache
rm -rf node_modules/.vite
npm run build
```

### Port Already in Use

**Problem:** Port 3000 is taken  
**Solution:**
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Or use a different port
npm run dev -- --port 3001
```

## Making Changes

### Adding a New Field to Report

1. **Update TypeScript types** (`src/types/index.ts`):
```typescript
export interface ReportGenerationResponse {
  // ... existing fields
  new_field: string;  // Add your field
}
```

2. **Update display** (`src/App.tsx`):
```tsx
<div>
  <span className="text-gray-600">New Field:</span>
  <span>{reportData.new_field}</span>
</div>
```

### Changing Styling

All styles use Tailwind classes. To change colors:

```tsx
// Change button color from indigo to blue
className="bg-blue-600 hover:bg-blue-700"

// Change background gradient
className="bg-gradient-to-br from-green-50 to-emerald-100"
```

### Adding Validation

```typescript
const [error, setError] = useState<string | null>(null);

const handleSubmit = async () => {
  // Clear previous errors
  setError(null);
  
  // Validation
  if (!selectedCompanyId) {
    setError('Please select a company');
    return;
  }
  
  // ... rest of your logic
};
```

## Dependencies

Key packages explained:

| Package | Version | Purpose |
|---------|---------|---------|
| react | 18.x | UI library |
| react-dom | 18.x | React renderer for web |
| typescript | 5.x | Type checking |
| vite | 5.x | Build tool |
| tailwindcss | 3.x | CSS framework |
| axios | 1.x | HTTP client |
| @types/* | latest | TypeScript definitions |

## Production Build

To build for production:

```bash
# Create optimized build
npm run build

# Output will be in dist/ folder
# Files are minified and optimized

# Preview production build locally
npm run preview
```

The production build:
- Minifies JavaScript and CSS
- Optimizes images
- Removes development code
- Enables source maps
- Tree-shakes unused code

## Learning Resources

To understand the codebase:

1. **React Hooks:** https://react.dev/reference/react
2. **TypeScript:** https://www.typescriptlang.org/docs/
3. **Tailwind CSS:** https://tailwindcss.com/docs
4. **Vite:** https://vitejs.dev/guide/

## Customization Ideas

Want to make it your own?

- Change color scheme (update Tailwind config)
- Add dark mode
- Add company filtering/search
- Add export to PDF
- Add report history
- Add charts/visualizations
- Add print stylesheet

## Testing

To add tests (not included yet):

```bash
# Install testing dependencies
npm install --save-dev @testing-library/react @testing-library/jest-dom vitest

# Create test file
# src/App.test.tsx
```

## Performance Tips

The app is already fast, but you can:

1. **Lazy load components:**
```typescript
const HeavyComponent = lazy(() => import('./HeavyComponent'));
```

2. **Memoize expensive calculations:**
```typescript
const expensiveValue = useMemo(() => {
  return computeExpensiveValue(data);
}, [data]);
```

3. **Debounce API calls** (if adding search)

## Code Style

This project follows:
- **Functional components** with hooks
- **TypeScript strict mode**
- **Prettier formatting** (optional - add .prettierrc)
- **ESLint rules** (configured in vite.config.ts)

---

**Questions?** The browser console is your friend - check it for errors!

**Making changes?** The dev server has hot reload - save and see changes instantly!
