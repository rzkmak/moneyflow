import { useState } from 'react';
import { UploadSection } from './components/UploadSection';
import { TransactionList } from './components/TransactionList';
import { TemplateDownloader } from './components/TemplateDownloader';
import Dashboard from './pages/Dashboard';

function App() {
  const [activeTab, setActiveTab] = useState<'transactions' | 'dashboard'>('transactions');
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleUploadComplete = () => {
    // Trigger a refresh of the transaction list
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <div className="min-h-screen bg-gray-50" style={{ border: '2px solid red' }}>
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-8">
              <h1 className="text-xl font-semibold text-gray-900">
                MoneyFlow
              </h1>
              <nav className="flex space-x-4">
                <button
                  onClick={() => setActiveTab('transactions')}
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    activeTab === 'transactions'
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  Transactions
                </button>
                <button
                  onClick={() => setActiveTab('dashboard')}
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    activeTab === 'dashboard'
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  Dashboard
                </button>
              </nav>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          {activeTab === 'transactions' && (
            <div className="space-y-6">
              {/* Upload Section */}
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-lg font-medium text-gray-900 mb-4">
                  Upload CSV Files
                </h2>
                <div className="flex justify-between items-start mb-4">
                  <UploadSection onUploadComplete={handleUploadComplete} />
                  <TemplateDownloader />
                </div>
                <div className="text-sm text-gray-500">
                  <p className="font-medium mb-1">Supported formats:</p>
                  <ul className="list-disc list-inside space-y-1">
                    <li>PayPay CSV (UTF-8)</li>
                    <li>SMBC CSV (Shift-JIS/CP932)</li>
                    <li>Standard Template CSV</li>
                  </ul>
                </div>
              </div>

              {/* Transaction List */}
              <div className="bg-white shadow rounded-lg p-6">
                <TransactionList refreshTrigger={refreshTrigger} />
              </div>
            </div>
          )}
          {activeTab === 'dashboard' && <Dashboard />}
        </div>
      </main>
    </div>
  );
}

export default App;