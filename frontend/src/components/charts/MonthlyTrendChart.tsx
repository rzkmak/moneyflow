import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

interface MonthlyTrendData {
  month: string;
  categories: Record<string, number>;
}

interface MonthlyTrendChartProps {
  data: MonthlyWeeklyTrend[];
}

interface MonthlyWeeklyTrend {
  month: string;
  weeks: WeeklyTrendData[];
}

interface WeeklyTrendData {
  week: string;
  week_label: string;
  categories: Record<string, number>;
}

const MonthlyTrendChart: React.FC<MonthlyTrendChartProps> = ({ data }) => {
  const COLORS = [
    '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4',
    '#84cc16', '#f97316', '#ec4899', '#6366f1', '#14b8a6', '#f43f5e'
  ];

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('ja-JP', {
      style: 'currency',
      currency: 'JPY',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const total = payload.reduce((sum: number, entry: any) => sum + entry.value, 0);
      return (
        <div className="bg-white p-3 border border-gray-200 shadow-lg rounded-md max-w-xs">
          <p className="text-sm font-medium text-gray-900 mb-1">{label}</p>
          <p className="text-sm text-gray-600 mb-1">{`Total: ${formatCurrency(total)}`}</p>
          <div className="space-y-1">
            {payload.map((entry: any, index: number) => (
              <div key={index} className="flex items-center justify-between text-xs">
                <div className="flex items-center space-x-2">
                  <div
                    className="w-3 h-3 rounded-sm"
                    style={{ backgroundColor: entry.color }}
                  />
                  <span className="text-gray-700">{entry.name}</span>
                </div>
                <span className="font-medium text-gray-900">{formatCurrency(entry.value)}</span>
              </div>
            ))}
          </div>
        </div>
      );
    }
    return null;
  };

  // Transform data to monthly totals with category breakdowns
  const monthlyData = data.map(monthData => {
    const result: any = {
      month: monthData.month,
      label: monthData.month
    };

    // Aggregate all categories across all weeks in the month
    const categoryTotals: Record<string, number> = {};

    monthData.weeks.forEach(weekData => {
      Object.entries(weekData.categories).forEach(([category, amount]) => {
        categoryTotals[category] = (categoryTotals[category] || 0) + amount;
      });
    });

    // Sort categories by amount for consistent stacking order
    const sortedCategories = Object.entries(categoryTotals)
      .sort(([,a], [,b]) => b - a);

    sortedCategories.forEach(([category, amount]) => {
      result[category] = amount;
    });

    // Calculate total for the month
    result.total = Object.values(categoryTotals).reduce((sum: number, amount: number) => sum + amount, 0);

    return result;
  });

  // Get all unique categories for the legend
  const allCategories = Array.from(
    new Set(data.flatMap(monthData =>
      monthData.weeks.flatMap(weekData => Object.keys(weekData.categories))
    ))
  );

  return (
    <div className="bg-white p-4 rounded-lg shadow-sm border">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Monthly Spending Trends</h3>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={monthlyData}
            margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis
              dataKey="label"
              stroke="#666"
              tick={{ fontSize: 12 }}
            />
            <YAxis
              type="number"
              stroke="#666"
              tick={{ fontSize: 12 }}
              tickFormatter={(value) => `${(value / 1000).toFixed(0)}k`}
            />
            <Tooltip content={<CustomTooltip />} />
            {allCategories.map((category, index) => (
              <Bar
                key={category}
                dataKey={category}
                stackId="a"
                fill={COLORS[index % COLORS.length]}
                name={category}
              />
            ))}
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="mt-4 flex flex-wrap gap-2 justify-center">
        {allCategories.map((category, index) => (
          <div key={category} className="flex items-center space-x-1 text-xs">
            <div
              className="w-3 h-3 rounded-sm"
              style={{ backgroundColor: COLORS[index % COLORS.length] }}
            />
            <span className="text-gray-700">{category}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MonthlyTrendChart;