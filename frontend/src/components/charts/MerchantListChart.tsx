import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

interface TopMerchant {
  merchant: string;
  amount: number;
  count: number;
}

interface MerchantListChartProps {
  data: TopMerchant[];
  limit?: number;
}

const MerchantListChart: React.FC<MerchantListChartProps> = ({ data, limit = 10 }) => {
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('ja-JP', {
      style: 'currency',
      currency: 'JPY',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const displayData = data.slice(0, limit);

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-3 border border-gray-200 shadow-lg rounded-md">
          <p className="text-sm font-medium text-gray-900">{data.merchant}</p>
          <p className="text-sm text-blue-600">
            {`Total Spending: ${formatCurrency(data.amount)}`}
          </p>
          <p className="text-sm text-gray-500">
            {`Transactions: ${data.count}`}
          </p>
        </div>
      );
    }
    return null;
  };

  const truncateMerchantName = (name: string, maxLength: number = 15) => {
    if (name.length <= maxLength) return name;
    return name.substring(0, maxLength) + '...';
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow-sm border">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">
        Top Merchants by Spending {limit}
      </h3>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={displayData}
            layout="horizontal"
            margin={{ top: 5, right: 30, left: 60, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis
              type="number"
              stroke="#666"
              tick={{ fontSize: 12 }}
              tickFormatter={(value) => `${(value / 1000).toFixed(0)}k`}
            />
            <YAxis
              type="category"
              dataKey="merchant"
              stroke="#666"
              tick={{ fontSize: 12 }}
              tickFormatter={(value) => truncateMerchantName(value)}
              width={80}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar
              dataKey="amount"
              fill="#10b981"
              radius={[0, 4, 4, 0]}
              name="Spending"
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default MerchantListChart;