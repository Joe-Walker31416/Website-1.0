import { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Background from './Components/Background';
import LoginPage from './Components/LoginPage';
import Sections from './Components/Sections';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check for token in URL params (after Spotify redirect)
    const params = new URLSearchParams(window.location.search);
    const token = params.get('access_token');
    
    if (token) {
      // Save token and set authenticated
      localStorage.setItem('access_token', token);
      setIsAuthenticated(true);
      // Clean up URL
      window.history.replaceState({}, document.title, '/');
    } else {
      // Check if token exists in localStorage
      const storedToken = localStorage.getItem('access_token');
      if (storedToken) {
        setIsAuthenticated(true);
      }
    }
    setIsLoading(false);
  }, []);
  
  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <Router>
      <Routes>
        <Route 
          path="/login" 
          element={isAuthenticated ? <Navigate to="/" /> : <LoginPage />} 
        />
        <Route 
          path="/" 
          element={isAuthenticated ? <Background /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/sections" 
          element={isAuthenticated ? <Sections /> : <Navigate to="/login" />} 
        />
      </Routes>
    </Router>
  );
}

export default App;