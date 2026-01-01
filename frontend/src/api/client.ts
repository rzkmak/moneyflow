const API_BASE_URL = 'http://localhost:8000';

export interface Transaction {
  id: string;
  date: string;
  amount: number;
  merchant?: string;
  description?: string;
  category?: string;
  source: string;
  source_type: 'paypay' | 'smbc' | 'manual';
  created_at: string;
}

export interface TransactionUpdate {
  category: string;
}

// Dashboard Stats interfaces
export interface WeeklyTrendData {
  week: string;
  week_label: string;
  categories: Record<string, number>;
}

export interface MonthlyWeeklyTrend {
  month: string;
  weeks: WeeklyTrendData[];
}

export interface SourceBreakdown {
  source: string;
  amount: number;
  percentage: number;
}

export interface TopMerchant {
  merchant: string;
  amount: number;
  count: number;
}

export interface CategorySpending {
  category: string;
  amount: number;
  percentage: number;
}

export interface DashboardStats {
  weekly_trends: MonthlyWeeklyTrend[];
  source_breakdown: SourceBreakdown[];
  top_merchants: TopMerchant[];
  category_spending: CategorySpending[];
}

// Category Rule interfaces
export interface CategoryRule {
  id: string;
  keyword: string;
  category: string;
  created_at: string;
}

export interface CategoryRuleCreate {
  keyword: string;
  category: string;
}

export interface UploadSummary {
  imported: number;
  skipped: number;
  message: string;
}

export interface ApiResponse<T> {
  data: T;
}

export class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  async updateTransaction(transactionId: string, update: TransactionUpdate): Promise<Transaction> {
    const response = await fetch(`${this.baseUrl}/api/transactions/${transactionId}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(update),
    });

    if (!response.ok) {
      throw new Error(`Failed to update transaction: ${response.statusText}`);
    }

    return response.json();
  }

  async uploadFile(file: File): Promise<UploadSummary> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${this.baseUrl}/api/transactions/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.statusText}`);
    }

    return response.json();
  }

  async getTransactions(skip: number = 0, limit: number = 100): Promise<Transaction[]> {
    const response = await fetch(
      `${this.baseUrl}/api/transactions/?skip=${skip}&limit=${limit}`
    );

    if (!response.ok) {
      throw new Error(`Failed to fetch transactions: ${response.statusText}`);
    }

    return response.json();
  }

  async downloadTemplate(): Promise<Blob> {
    const response = await fetch(`${this.baseUrl}/api/transactions/template`);

    if (!response.ok) {
      throw new Error(`Failed to download template: ${response.statusText}`);
    }

    return response.blob();
  }
}

export const apiClient = new ApiClient();