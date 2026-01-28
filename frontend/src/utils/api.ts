import axios from 'axios';
import type { CompanyProfile, ReportGenerationRequest, ReportGenerationResponse } from '../types';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fetchCompanies = async (): Promise<CompanyProfile[]> => {
  const response = await api.get<{ companies: CompanyProfile[] }>('/api/v1/companies');
  return response.data.companies;
};

export const generateReport = async (
  request: ReportGenerationRequest
): Promise<ReportGenerationResponse> => {
  const response = await api.post<ReportGenerationResponse>(
    '/api/v1/generate-report',
    request
  );
  return response.data;
};

export default api;
