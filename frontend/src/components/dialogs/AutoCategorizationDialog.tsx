import React, { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';

// Import from the working pattern used by other components
import { apiClient } from '../../api';
import type { CategoryRuleCreate } from '../../api/client';

interface AutoCategorizationDialogProps {
  isOpen: boolean;
  onClose: () => void;
  merchant: string;
  currentCategory: string;
  onSuccess?: () => void;
}

const AutoCategorizationDialog: React.FC<AutoCategorizationDialogProps> = ({
  isOpen,
  onClose,
  merchant,
  currentCategory,
  onSuccess
}) => {
  const [keyword, setKeyword] = useState('');
  const [category, setCategory] = useState('');
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);

  const queryClient = useQueryClient();

  // Create category rule mutation
  const createRuleMutation = useMutation({
    mutationFn: async (rule: CategoryRuleCreate) => {
      const response = await fetch('http://localhost:8000/api/transactions/category-rules', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(rule),
      });

      if (!response.ok) {
        throw new Error('Failed to create category rule');
      }

      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['category-rules'] });
      onSuccess?.();
      onClose();
    },
    onError: (error) => {
      setError('Failed to create rule: ' + (error instanceof Error ? error.message : 'Unknown error'));
    }
  });

  // Common category suggestions
  const commonCategories = [
    'Food',
    'Transportation',
    'Shopping',
    'Entertainment',
    'Bills',
    'Healthcare',
    'Education',
    'Travel',
    'Gifts',
    'Others'
  ];

  const handleSuggestRules = () => {
    const merchantLower = merchant.toLowerCase();
    const suggestedRules = [];

    // Extract keywords from merchant name
    const words = merchantLower.split(/[,\s]+/).filter(word => word.length > 1);

    for (const word of words) {
      if (word.length >= 2) {
        suggestedRules.push(word);
      }
    }

    // Add the full merchant name as a suggestion
    if (merchant.length >= 3) {
      suggestedRules.push(merchant);
    }

    setSuggestions([...new Set(suggestedRules)].slice(0, 5));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!keyword.trim() || !category.trim()) {
      setError('Please enter both keyword and category');
      return;
    }

    createRuleMutation.mutate({
      keyword: keyword.trim(),
      category: category.trim()
    });
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md mx-4">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Create Auto-Categorization Rule
        </h3>

        <p className="text-sm text-gray-600 mb-4">
          Create a rule to automatically assign the "{category}" category for transactions from merchant "<span className="font-medium">{merchant}</span>"?
        </p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Keyword
            </label>
            <input
              type="text"
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
              placeholder={merchant}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
            <div className="mt-2">
              <button
                type="button"
                onClick={handleSuggestRules}
                className="text-xs text-blue-600 hover:text-blue-800"
              >
                Suggest keywords
              </button>
            </div>
            {suggestions.length > 0 && (
              <div className="mt-2">
                <p className="text-xs text-gray-500 mb-1">Suggested keywords:</p>
                <div className="flex flex-wrap gap-1">
                  {suggestions.map((suggestion, index) => (
                    <button
                      key={index}
                      type="button"
                      onClick={() => setKeyword(suggestion)}
                      className="text-xs bg-gray-100 hover:bg-gray-200 px-2 py-1 rounded"
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Category
            </label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">Select a category</option>
              {commonCategories.map((cat) => (
                <option key={cat} value={cat}>
                  {cat}
                </option>
              ))}
            </select>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-md p-3">
              <p className="text-sm text-red-600">{error}</p>
            </div>
          )}

          <div className="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={createRuleMutation.isPending}
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md disabled:opacity-50"
            >
              {createRuleMutation.isPending ? 'Creating...' : 'Create Rule'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AutoCategorizationDialog;