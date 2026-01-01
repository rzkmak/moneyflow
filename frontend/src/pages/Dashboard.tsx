import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../api/client';
import type { DashboardStats } from '../api/client';
import MonthlyTrendChart from '../components/charts/MonthlyTrendChart';
import MerchantListChart from '../components/charts/MerchantListChart';
import DateRangeFilter from '../components/DateRangeFilter';

const Dashboard: React.FC = () => {
  const [dateRange, setDateRange] = useState<{ startDate: string; endDate: string }>({
    startDate: '',
    endDate: ''
  });

  // Initialize date range with last 90 days when component mounts
  React.useEffect(() => {
    const today = new Date();
    const ninetyDaysAgo = new Date();
    ninetyDaysAgo.setDate(today.getDate() - 90);

    const formatDate = (date: Date): string => {
      return date.toISOString().split('T')[0];
    };

    setDateRange({
      startDate: formatDate(ninetyDaysAgo),
      endDate: formatDate(today)
    });
  }, []);

  const { data: stats, isLoading, error, refetch } = useQuery<DashboardStats>({
    queryKey: ['dashboard-stats', dateRange.startDate, dateRange.endDate],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (dateRange.startDate) params.append('start_date', dateRange.startDate);
      if (dateRange.endDate) params.append('end_date', dateRange.endDate);

      const response = await fetch(`http://localhost:8000/api/transactions/stats?${params}`);
      if (!response.ok) {
        throw new Error('Failed to fetch dashboard stats');
      }
      return response.json();
    },
    refetchInterval: 5 * 60 * 1000, // Refetch every 5 minutes
  });

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-6"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-96 bg-gray-200 rounded-lg"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">Error: Failed to load data.</p>
        </div>
      </div>
    );
  }

  if (!stats) {
    return null;
  }

  // Calculate total spending from weekly trends
  const totalSpending = stats.weekly_trends.reduce(
    (sum, month) => sum + month.weeks.reduce(
      (weekSum, week) => weekSum + Object.values(week.categories).reduce((a, b) => a + b, 0),
      0
    ),
    0
  );

  const handleDateRangeChange = (startDate: string, endDate: string) => {
    setDateRange({ startDate, endDate });
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Expense Dashboard</h1>
        <p className="text-gray-600">View expense breakdown and trends</p>
      </div>

      {/* Date Range Filter */}
      <DateRangeFilter
          startDate={dateRange.startDate}
          endDate={dateRange.endDate}
          onDateRangeChange={handleDateRangeChange}
        />

      {/* Charts Grid */}
      <div className="grid grid-cols-1 gap-6">
        <MonthlyTrendChart data={stats.weekly_trends} />
      </div>

  
      {/* Category Breakdown */}
      <div className="mt-8 bg-white p-6 rounded-lg shadow-sm border">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Spending by Category</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {stats.category_spending
            .sort((a, b) => b.amount - a.amount)
            .map((category, index) => (
              <div key={category.category} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <div
                    className="w-4 h-4 rounded"
                    style={{ backgroundColor: COLORS[index % COLORS.length] }}
                  />
                  <span className="text-sm font-medium text-gray-700">
                    {category.category}
                  </span>
                </div>
                <div className="text-right">
                  <p className="text-sm font-semibold text-gray-900">
                    {new Intl.NumberFormat('ja-JP', {
                      style: 'currency',
                      currency: 'JPY',
                      minimumFractionDigits: 0,
                      maximumFractionDigits: 0,
                    }).format(category.amount)}
                  </p>
                  <p className="text-xs text-gray-500">
                    {category.percentage.toFixed(1)}% of total
                  </p>
                </div>
              </div>
            ))}
        </div>
      </div>
    </div>
  );
};

// Define COLORS constant for the category breakdown
const COLORS = [
  '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4',
  '#84cc16', '#f97316', '#ec4899', '#6366f1', '#14b8a6', '#f43f5e'
];

export default Dashboard;