import './App.css';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './Authentication/Login';
import Dashboard from './Dashboard/Dashboard';
import CreateUser from './Users/CreateUser';
import { useAuthStore } from './Store/useAuthStore';
import ProtectedRoute from './Authentication/ProtectedRoute';

function App() {
  const token = useAuthStore((s) => s.accessToken);

  return (
    // <Router>
      <Routes>
        <Route path="/login" element={token ? <Navigate to="/dashboard" /> : <Login />} />
        <Route path="/dashboard" element={
  <ProtectedRoute>
     <Dashboard />
  </ProtectedRoute>
} />
        {/* <Route path="/dashboard" element={token ? <Dashboard /> : <Navigate to="/login" />} /> */}
        <Route path="/create-user" element={token ? <CreateUser /> : <Navigate to="/login" />} />
        <Route path="*" element={<Navigate to={token ? "/dashboard" : "/login"} />} />
      </Routes>
    // </Router>
  );
}

export default App;
