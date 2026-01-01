import React, { useState, useEffect } from 'react';

interface DateRangeFilterProps {
  startDate: string;
  endDate: string;
  onDateRangeChange: (startDate: string, endDate: string) => void;
  className?: string;
}

const DateRangeFilter: React.FC<DateRangeFilterProps> = ({
  startDate,
  endDate,
  onDateRangeChange,
  className = ""
}) => {

  const handleStartDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newStartDate = e.target.value;
    let newEnd = endDate;

    // Ensure end date is not before start date
    if (endDate && newStartDate > endDate) {
      newEnd = newStartDate;
    }

    onDateRangeChange(newStartDate, newEnd);
  };

  const handleEndDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newEndDate = e.target.value;
    let newStart = startDate;

    // Ensure end date is not before start date
    if (startDate && newEndDate < startDate) {
      newStart = newEndDate;
    }

    onDateRangeChange(newStart, newEndDate);
  };

  const quickRanges = [
    { label: 'Last 7 Days', days: 7 },
    { label: 'Last 30 Days', days: 30 },
    { label: 'Last 90 Days', days: 90 },
    { label: 'Last 180 Days', days: 180 },
    { label: 'Last Year', days: 365 },
  ];

  const applyQuickRange = (days: number) => {
    const today = new Date();
    const pastDate = new Date();
    pastDate.setDate(today.getDate() - days);

    const formatDate = (date: Date): string => {
      return date.toISOString().split('T')[0];
    };

    onDateRangeChange(formatDate(pastDate), formatDate(today));
  };

  return (
    <div className={`bg-white p-4 rounded-lg shadow-sm border mb-6 ${className}`}>
      <div className="flex flex-col space-y-4">
        {/* Title */}
        <h3 className="text-lg font-semibold text-gray-800">Filter by Date Range</h3>

        {/* Quick Range Buttons */}
        <div className="flex flex-wrap gap-2">
          {quickRanges.map((range) => (
            <button
              key={range.days}
              onClick={() => applyQuickRange(range.days)}
              className="px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-md transition-colors"
            >
              {range.label}
            </button>
          ))}
        </div>

        {/* Date Input Fields */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:space-x-4 space-y-2 sm:space-y-0">
          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Start Date
            </label>
            <input
              type="date"
              value={startDate}
              onChange={handleStartDateChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              max={endDate || new Date().toISOString().split('T')[0]}
            />
          </div>

          <div className="flex items-center text-gray-500">
            <span>to</span>
          </div>

          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              End Date
            </label>
            <input
              type="date"
              value={endDate}
              onChange={handleEndDateChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              min={startDate}
              max={new Date().toISOString().split('T')[0]}
            />
          </div>
        </div>

        {/* Current Selection Display */}
        {startDate && endDate && (
          <div className="text-sm text-gray-600 mt-2">
            Showing data from {new Date(startDate).toLocaleDateString('en-US', {
              month: 'short',
              day: 'numeric',
              year: 'numeric'
            })} to {new Date(endDate).toLocaleDateString('en-US', {
              month: 'short',
              day: 'numeric',
              year: 'numeric'
            })}
          </div>
        )}
      </div>
    </div>
  );
};

export default DateRangeFilter;