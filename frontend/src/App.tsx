import { useState, useEffect } from 'react';
import { fetchCompanies, generateReport } from './utils/api';
import { downloadJSON } from './utils/download';
import type { CompanyProfile, FinancialPeriod, ReportGenerationResponse } from './types';

function App() {
  const [companies, setCompanies] = useState<CompanyProfile[]>([]);
  const [selectedCompanyId, setSelectedCompanyId] = useState<number | null>(null);
  const [selectedPeriod, setSelectedPeriod] = useState<FinancialPeriod | null>(null);
  const [reportData, setReportData] = useState<ReportGenerationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loadingCompanies, setLoadingCompanies] = useState(true);

  useEffect(() => {
    const loadCompanies = async () => {
      try {
        setLoadingCompanies(true);
        const data = await fetchCompanies();
        setCompanies(data);
        setError(null);
      } catch (err) {
        setError('Failed to load companies. Please ensure the backend is running at http://localhost:8000');
        console.error('Error loading companies:', err);
      } finally {
        setLoadingCompanies(false);
      }
    };
    loadCompanies();
  }, []);

  const handleGenerateReport = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedCompanyId || !selectedPeriod) {
      setError('Please select both a company and a financial period.');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const data = await generateReport({
        company_id: selectedCompanyId,
        financial_period: selectedPeriod,
        include_metadata: false
      });
      setReportData(data);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to generate report');
      console.error('Error generating report:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    if (!reportData) return;
    const timestamp = new Date().toISOString().split('T')[0];
    const filename = `report_${reportData.company_name.replace(/\s+/g, '_')}_${reportData.quarter || 'annual'}_${timestamp}.json`;
    downloadJSON(reportData, filename);
  };

  const handleClear = () => {
    setReportData(null);
    setSelectedCompanyId(null);
    setSelectedPeriod(null);
    setError(null);
  };

  if (loadingCompanies) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading companies...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-10">
          <h1 className="text-4xl font-bold text-gray-900 mb-3">
            Company Profile Manager
          </h1>
          <p className="text-lg text-gray-600">
            Financial Report Input Validator & Generator
          </p>
          <p className="text-sm text-gray-500 mt-2">
            Assignment 2 - Python + FastAPI + Pydantic Solution
          </p>
          <div className="mt-4 inline-flex items-center px-4 py-2 bg-blue-100 rounded-full">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse mr-2"></div>
            <span className="text-sm text-blue-800 font-medium">
              {companies.length} Companies Loaded
            </span>
          </div>
        </div>

        {error && (
          <div className="mb-6 bg-red-50 border-l-4 border-red-500 p-4 rounded-lg">
            <div className="flex items-center">
              <svg className="w-5 h-5 text-red-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              <p className="text-red-800">{error}</p>
            </div>
          </div>
        )}

        {!reportData ? (
          <div className="bg-white rounded-xl shadow-xl p-8">
            <form onSubmit={handleGenerateReport}>
              <div className="mb-6">
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Which company are you preparing the report for? *
                </label>
                <select
                  value={selectedCompanyId || ''}
                  onChange={(e) => setSelectedCompanyId(Number(e.target.value))}
                  disabled={loading}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100"
                  required
                >
                  <option value="">-- Select a company --</option>
                  {companies.map((company) => (
                    <option key={company.id} value={company.id}>
                      {company.company_name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="mb-6">
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  What financial period are we reporting? *
                </label>
                <select
                  value={selectedPeriod || ''}
                  onChange={(e) => setSelectedPeriod(e.target.value as FinancialPeriod)}
                  disabled={loading}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100"
                  required
                >
                  <option value="">-- Select a period --</option>
                  <option value="Q1">Q1 (Quarter 1)</option>
                  <option value="Q2">Q2 (Quarter 2)</option>
                  <option value="Q3">Q3 (Quarter 3)</option>
                  <option value="Annual">Annual (Full Year)</option>
                </select>
              </div>

              <button
                type="submit"
                disabled={!selectedCompanyId || !selectedPeriod || loading}
                className="w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-bold py-4 px-6 rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-lg"
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    Generating Report...
                  </>
                ) : (
                  <>
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    Generate Report
                  </>
                )}
              </button>
            </form>
          </div>
        ) : (
          <div className="mt-8 bg-white rounded-lg shadow-lg border border-gray-200 overflow-hidden">
            <div className="bg-gradient-to-r from-blue-600 to-blue-700 px-6 py-4">
              <h2 className="text-xl font-bold text-white">Generated Report Output</h2>
              <p className="text-blue-100 text-sm mt-1">Structured JSON ready for downstream processing</p>
            </div>
            
            <div className="p-6">
              <div className="bg-gray-900 rounded-lg p-4 overflow-x-auto">
                <pre className="text-green-400 text-sm font-mono">
                  {JSON.stringify(reportData, null, 2)}
                </pre>
              </div>

              <div className="flex gap-3 mt-4">
                <button
                  onClick={handleDownload}
                  className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200 flex items-center justify-center gap-2"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                  </svg>
                  Download JSON
                </button>
                
                <button
                  onClick={handleClear}
                  className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-3 px-6 rounded-lg transition-colors duration-200"
                >
                  Generate New Report
                </button>
              </div>

              <div className="mt-6 grid grid-cols-2 gap-4 pt-4 border-t border-gray-200">
                <div>
                  <p className="text-xs text-gray-500 uppercase tracking-wide">Report Type</p>
                  <p className="text-sm font-semibold text-gray-900 mt-1">{reportData.report_type}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500 uppercase tracking-wide">Period End</p>
                  <p className="text-sm font-semibold text-gray-900 mt-1">{reportData.reporting_period_end}</p>
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="mt-8 text-center text-sm text-gray-500">
          <p>Invictus FullStack Developer Technical Work Sample - Assignment 2</p>
          <p className="mt-1">Python + FastAPI + Pydantic + React + TypeScript</p>
          <p className="mt-1 text-xs">By Ishmeet Singh Arora</p>
        </div>
      </div>
    </div>
  );
}

export default App;
