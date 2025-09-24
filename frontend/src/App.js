import React, { useState } from 'react';
import CustomerPage from './pages/CustomerPage';
import ManagerPage from './pages/ManagerPage';

function App() {
  const [page, setPage] = useState('customer');

  return (
    <>
      <div className="flex justify-center gap-4 my-4">
        <button onClick={() => setPage('customer')} className="px-4 py-2 bg-primary text-white rounded">Customer</button>
        <button onClick={() => setPage('manager')} className="px-4 py-2 bg-primary text-white rounded">Manager</button>
      </div>
      {page === 'customer' ? <CustomerPage /> : <ManagerPage />}
    </>
  );
}

export default App;
