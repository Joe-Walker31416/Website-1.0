import { useEffect, useState, useCallback } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Box, ChakraProvider, Spinner, Center, useToast } from '@chakra-ui/react';
import Background from './Components/Background';
import LoginPage from './Components/LoginPage';
import Sections from './Components/Sections';
import ComparisonPage from './Components/ComparisonPage';
import Navbar from './Components/Navbar';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  
  // Check for authentication
  const checkAuth = useCallback(() => {
    // Check for token in URL params (after Spotify redirect)
    const params = new URLSearchParams(window.location.search);
    const token = params.get('access_token');
    
    if (token) {
      // Save token and set authenticated
      localStorage.setItem('access_token', token);
      setIsAuthenticated(true);
      // Clean up URL
      window.history.replaceState({}, document.title, '/');
      // Dispatch storage event so other components know about the auth change
      window.dispatchEvent(new Event('storage'));
    } else {
      // Check if token exists in localStorage
      const storedToken = localStorage.getItem('access_token');
      if (storedToken) {
        setIsAuthenticated(true);
      }
    }
    setIsLoading(false);
  }, []);
  
  useEffect(() => {
    checkAuth();
    
    // Listen for storage changes to update auth state
    const handleStorageChange = () => {
      const token = localStorage.getItem('access_token');
      setIsAuthenticated(!!token);
    };
    
    window.addEventListener('storage', handleStorageChange);
    
    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, [checkAuth]);
  
  if (isLoading) {
    return (
      <Center height="100vh">
        <Spinner size="xl" color="green.500" thickness="4px" />
      </Center>
    );
  }

  return (
    <Router>
      {isAuthenticated && <Navbar setIsAuthenticated={setIsAuthenticated} />}
      <Box pt={isAuthenticated ? "70px" : 0}>
        <Routes>
          <Route 
            path="/login" 
            element={isAuthenticated ? <Navigate to="/compare" /> : <LoginPage />} 
          />
          <Route 
            path="/" 
            element={isAuthenticated ? <Navigate to="/compare" /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/sections" 
            element={isAuthenticated ? <Sections /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/compare" 
            element={isAuthenticated ? <ComparisonPage /> : <Navigate to="/login" />}
          />
        </Routes>
      </Box>
    </Router>
  );
}

export default App;