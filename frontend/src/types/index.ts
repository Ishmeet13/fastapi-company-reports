export interface CompanyProfile {
  id: number;
  company_name: string;
  legal_structure: string;
  year_end: string;
  address: string;
  city: string;
  province: string;
  postal_code: string;
  industry?: string;
  description?: string;
}

export type FinancialPeriod = "Q1" | "Q2" | "Q3" | "Annual";

export interface ReportGenerationRequest {
  company_id: number;
  financial_period: FinancialPeriod;
  include_metadata?: boolean;
}

export interface ReportGenerationResponse {
  company_name: string;
  report_type: "Interim" | "Annual";
  quarter?: string;
  year_end: string;
  reporting_period_end: string;
  address: string;
  industry?: string;
  legal_structure?: string;
}
