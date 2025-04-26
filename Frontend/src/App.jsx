import { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Background from './Components/Background';
import LoginPage from './Components/LoginPage';
import Sections from './Components/Sections'; // Import the Sections component

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const token = params.get('access_token');
    
    if (token) {
      localStorage.setItem('access_token', token);
      setIsAuthenticated(true);
      window.history.replaceState({}, document.title, '/'); // clean up URL
    } else {
      const stored = localStorage.getItem('access_token');
      setIsAuthenticated(!!stored);
    }
  }, []);
  
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route 
          path="/" 
          element={isAuthenticated ? <Background /> : <Navigate to="/login" />} 
        />
        <Route path="/sections" element={<Sections />} />
      </Routes>
    </Router>
  );
}

export default App;