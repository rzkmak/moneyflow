import { useState, useEffect, useMemo } from 'react';
import { apiClient } from '../api';
import type { Transaction } from '../api/client';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import AutoCategorizationDialog from './dialogs/AutoCategorizationDialog';

interface TransactionListProps {
  refreshTrigger?: number;
}

export function TransactionList({ refreshTrigger }: TransactionListProps) {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalTransactions, setTotalTransactions] = useState(0);
  const [editingCategory, setEditingCategory] = useState<{transactionId: string, currentCategory: string, merchant?: string} | null>(null);
  const [newCategory, setNewCategory] = useState('');
  const [showCreateRuleDialog, setShowCreateRuleDialog] = useState(false);
  const itemsPerPage = 20;

  const queryClient = useQueryClient();

  // Update category mutation
  const updateCategoryMutation = useMutation({
    mutationFn: async ({ transactionId, category }: { transactionId: string, category: string }) => {
      return apiClient.updateTransaction(transactionId, { category });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['transactions'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard-stats'] });
      setEditingCategory(null);
      setNewCategory('');
    },
    onError: (error) => {
      alert('Failed to update category: ' + (error instanceof Error ? error.message : 'Unknown error'));
    }
  });

  // Category options for dropdown
  const categoryOptions = [
    'Uncategorized',
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

  useEffect(() => {
    loadTransactions();
  }, [currentPage, refreshTrigger]);

  const loadTransactions = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await apiClient.getTransactions(
        (currentPage - 1) * itemsPerPage,
        itemsPerPage
      );
      setTransactions(response);
      // For demo purposes, estimate total based on current page
      setTotalTransactions(currentPage * itemsPerPage);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load transactions');
    } finally {
      setLoading(false);
    }
  };

  const filteredTransactions = useMemo(() => {
    if (!searchTerm) return transactions;

    return transactions.filter(transaction =>
      transaction.merchant?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      transaction.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      transaction.source.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }, [transactions, searchTerm]);

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
    setCurrentPage(1); // Reset to first page when searching
  };

  const handlePageChange = (newPage: number) => {
    setCurrentPage(newPage);
  };

  const handleEditCategory = (transactionId: string, currentCategory: string) => {
    setEditingCategory({ transactionId, currentCategory });
    setNewCategory(currentCategory);
  };

  const handleSaveCategory = async (transactionId: string) => {
    if (!newCategory.trim()) return;

    try {
      await updateCategoryMutation.mutateAsync({ transactionId, category: newCategory.trim() });
    } catch (error) {
      // Error is already handled by mutation onError
    }
  };

  const handleCancelEdit = () => {
    setEditingCategory(null);
    setNewCategory('');
  };

  const handleCreateRuleClick = (merchant: string, currentCategory: string) => {
    setEditingCategory({
      transactionId: '',
      currentCategory,
      merchant
    });
    setShowCreateRuleDialog(true);
    setNewCategory(currentCategory);
  };

  const getCategoryColor = (category: string) => {
    const colors = {
      'Uncategorized': 'bg-gray-100 text-gray-800',
      'Food': 'bg-orange-100 text-orange-800',
      'Transportation': 'bg-blue-100 text-blue-800',
      'Shopping': 'bg-purple-100 text-purple-800',
      'Entertainment': 'bg-pink-100 text-pink-800',
      'Bills': 'bg-red-100 text-red-800',
      'Healthcare': 'bg-green-100 text-green-800',
      'Education': 'bg-indigo-100 text-indigo-800',
      'Travel': 'bg-yellow-100 text-yellow-800',
      'Gifts': 'bg-rose-100 text-rose-800',
      'Others': 'bg-slate-100 text-slate-800'
    };
    return colors[category as keyof typeof colors] || 'bg-gray-100 text-gray-800';
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('ja-JP', {
      style: 'currency',
      currency: 'JPY'
    }).format(amount);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ja-JP', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    });
  };

  const getSourceTypeColor = (sourceType: string) => {
    switch (sourceType) {
      case 'paypay':
        return 'bg-blue-100 text-blue-800';
      case 'smbc':
        return 'bg-green-100 text-green-800';
      case 'manual':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading && transactions.length === 0) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4">
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
        <h2 className="text-xl font-semibold text-gray-900">
          Transactions ({totalTransactions})
        </h2>

        <div className="relative w-full sm:w-64">
          <input
            type="text"
            placeholder="Search transactions..."
            value={searchTerm}
            onChange={handleSearch}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
          <svg
            className="absolute left-3 top-2.5 h-5 w-5 text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            />
          </svg>
        </div>
      </div>

      {filteredTransactions.length === 0 ? (
        <div className="bg-gray-50 border border-gray-200 rounded-md p-8 text-center">
          <svg
            className="mx-auto h-12 w-12 text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
          <p className="mt-2 text-sm text-gray-600">
            No transactions found
          </p>
        </div>
      ) : (
        <>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Merchant
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Category
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Description
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Source
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Amount
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredTransactions.map((transaction) => (
                  <tr key={transaction.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {formatDate(transaction.date)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {transaction.merchant || '-'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {editingCategory?.transactionId === transaction.id ? (
                        <div className="flex items-center space-x-2">
                          <select
                            value={newCategory}
                            onChange={(e) => setNewCategory(e.target.value)}
                            className="text-xs border border-gray-300 rounded px-2 py-1 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                          >
                            {categoryOptions.map((option) => (
                              <option key={option} value={option}>
                                {option}
                              </option>
                            ))}
                          </select>
                          <button
                            onClick={() => handleSaveCategory(transaction.id)}
                            disabled={updateCategoryMutation.isPending}
                            className="text-xs bg-blue-500 text-white px-2 py-1 rounded hover:bg-blue-600 disabled:opacity-50"
                          >
                            Save
                          </button>
                          <button
                            onClick={handleCancelEdit}
                            className="text-xs bg-gray-300 text-gray-700 px-2 py-1 rounded hover:bg-gray-400"
                          >
                            Cancel
                          </button>
                        </div>
                      ) : (
                        <div className="flex items-center space-x-2">
                          <span className={`px-2 py-1 text-xs font-medium rounded-full ${getCategoryColor(transaction.category || 'Uncategorized')}`}>
                            {transaction.category || 'Uncategorized'}
                          </span>
                          <>
                            <button
                              onClick={() => handleEditCategory(transaction.id, transaction.category || 'Uncategorized')}
                              className="text-xs text-blue-600 hover:text-blue-800 mr-1"
                            >
                              Edit
                            </button>
                            {transaction.merchant && (
                              <button
                                onClick={() => handleCreateRuleClick(transaction.merchant, transaction.category || 'Uncategorized')}
                                className="text-xs text-green-600 hover:text-green-800"
                                title="Create auto-categorization rule for this merchant"
                              >
                                Create Rule
                              </button>
                            )}
                          </>
                        </div>
                      )}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500">
                      {transaction.description || '-'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getSourceTypeColor(transaction.source_type)}`}>
                        {transaction.source_type}
                      </span>
                      <span className="ml-2 text-sm text-gray-500">
                        {transaction.source}
                      </span>
                    </td>
                    <td className={`px-6 py-4 whitespace-nowrap text-sm text-right font-medium ${
                      transaction.amount >= 0 ? 'text-red-600' : 'text-green-600'
                    }`}>
                      {formatCurrency(transaction.amount)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          <div className="flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3 sm:px-6">
            <div className="flex flex-1 justify-between sm:hidden">
              <button
                onClick={() => handlePageChange(currentPage - 1)}
                disabled={currentPage === 1}
                className="relative inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
              >
                Previous
              </button>
              <button
                onClick={() => handlePageChange(currentPage + 1)}
                disabled={filteredTransactions.length < itemsPerPage}
                className="ml-3 relative inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
              >
                Next
              </button>
            </div>
            <div className="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
              <div>
                <p className="text-sm text-gray-700">
                  Showing <span className="font-medium">{(currentPage - 1) * itemsPerPage + 1}</span> to{' '}
                  <span className="font-medium">
                    {Math.min(currentPage * itemsPerPage, totalTransactions)}
                  </span>{' '}
                  of <span className="font-medium">{totalTransactions}</span> results
                </p>
              </div>
              <div>
                <nav className="isolate inline-flex -space-x-px rounded-md shadow-sm" aria-label="Pagination">
                  <button
                    onClick={() => handlePageChange(currentPage - 1)}
                    disabled={currentPage === 1}
                    className="relative inline-flex items-center rounded-l-md px-2 py-2 ring-1 ring-inset ring-gray-300 bg-white text-gray-400 hover:bg-gray-50 focus:z-20 focus:outline-offset-0 disabled:opacity-50"
                  >
                    <span className="sr-only">Previous</span>
                    <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </button>
                  <button
                    onClick={() => handlePageChange(currentPage + 1)}
                    disabled={filteredTransactions.length < itemsPerPage}
                    className="relative inline-flex items-center rounded-r-md px-2 py-2 ring-1 ring-inset ring-gray-300 bg-white text-gray-400 hover:bg-gray-50 focus:z-20 focus:outline-offset-0 disabled:opacity-50"
                  >
                    <span className="sr-only">Next</span>
                    <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                    </svg>
                  </button>
                </nav>
              </div>
            </div>
          </div>
        </>
      )}

      {/* Auto Categorization Dialog */}
      <AutoCategorizationDialog
        isOpen={showCreateRuleDialog}
        onClose={() => {
          setShowCreateRuleDialog(false);
          setEditingCategory(null);
          setNewCategory('');
        }}
        merchant={editingCategory?.merchant || ''}
        currentCategory={editingCategory?.currentCategory || ''}
        onSuccess={() => {
          // Optionally refresh transactions or dashboard after rule creation
          queryClient.invalidateQueries({ queryKey: ['transactions'] });
          queryClient.invalidateQueries({ queryKey: ['dashboard-stats'] });
        }}
      />
    </div>
  );
}