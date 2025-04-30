import config from '../config';
import { 
  Box, 
  Spinner,
  Center,
  useToast,
  Container,
  Heading,
  Text
} from '@chakra-ui/react';
import React, { useEffect, useState, useCallback } from 'react';
import TabGroup from './TabGroup';
import LoginButton from './LoginButton';

const Sections = () => {
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userData, setUserData] = useState({
    player1: { saved: false, name: null, picture: null },
    player2: { saved: false, name: null, picture: null }
  });
  const toast = useToast();

  // Check authentication status
  const checkAuthStatus = useCallback(() => {
    const token = localStorage.getItem('access_token');
    setIsAuthenticated(!!token);
    return !!token;
  }, []);

  // Fetch user data if authenticated
  const fetchUserData = useCallback(async () => {
    if (!checkAuthStatus()) return;
    
    setIsLoading(true);
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(config.API_URL +'/api/user_status', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (!response.ok) {
        throw new Error('Failed to fetch user data');
      }
      
      const data = await response.json();
      setUserData(data);
    } catch (error) {
      console.error('Error fetching user data:', error);
      setError(error.message);
      
      toast({
        title: 'Error',
        description: 'Failed to load user data. Please try again.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  }, [checkAuthStatus, toast]);

  // Initial setup
  useEffect(() => {
    checkAuthStatus();
    fetchUserData();
    
    // Listen for auth state changes
    const handleStorageChange = (e) => {
      if (e.key === 'access_token') {
        const isAuth = checkAuthStatus();
        if (isAuth) {
          fetchUserData();
        }
      }
    };
    
    window.addEventListener('storage', handleStorageChange);
    
    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, [checkAuthStatus, fetchUserData]);

  // Poll for user status updates every 10 seconds when we're waiting for both users
  useEffect(() => {
    let interval;
    
    if (isAuthenticated && (!userData.player1.saved || !userData.player2.saved)) {
      interval = setInterval(() => {
        fetchUserData();
      }, 10000);
    }
    
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isAuthenticated, userData, fetchUserData]);

  return (
    <Container maxW="1200px" py={6}>
      {error && (
        <Box bg="red.100" p={4} mb={4} borderRadius="md">
          <Text color="red.800">Error: {error}</Text>
          <Text>Please check if the backend API is running at localhost:5000</Text>
        </Box>
      )}
      
      {/* Display just the My Music content without tabs */}
      <Box mt={4}>
        <Heading size="lg" mb={6} textAlign="center">
          Your Top Music{/* {userData?.player1?.name ? `${userData.player1.name}'s Top Music` : 'Your Top Music'} */}
        </Heading>
        
        {isLoading ? (
          <Center py={10}>
            <Spinner size="xl" color="green.500" />
          </Center>
        ) : isAuthenticated ? (
          <Box>
            <TabGroup />
          </Box>
        ) : (
          <Center py={10} flexDirection="column">
            <Text fontSize="lg" mb={4}>Please login to view your music</Text>
            <LoginButton />
          </Center>
        )}
      </Box>
    </Container>
  );
};

export default Sections;