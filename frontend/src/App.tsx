import { useState, useEffect } from 'react';
import { UploadSection } from './components/UploadSection';
import { TransactionList } from './components/TransactionList';
import { TemplateDownloader } from './components/TemplateDownloader';

function App() {
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
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">
                MoneyFlow
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <TemplateDownloader />
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Upload Section */}
            <div className="lg:col-span-1">
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-lg font-medium text-gray-900 mb-4">
                  Upload CSV Files
                </h2>
                <UploadSection onUploadComplete={handleUploadComplete} />
                <div className="mt-4 text-sm text-gray-500">
                  <p className="font-medium mb-1">Supported formats:</p>
                  <ul className="list-disc list-inside space-y-1">
                    <li>PayPay CSV (UTF-8)</li>
                    <li>SMBC CSV (Shift-JIS/CP932)</li>
                    <li>Standard Template CSV</li>
                  </ul>
                </div>
              </div>
            </div>

            {/* Transaction List */}
            <div className="lg:col-span-1">
              <div className="bg-white shadow rounded-lg p-6">
                <TransactionList refreshTrigger={refreshTrigger} />
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;