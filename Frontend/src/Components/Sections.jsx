import { 
  Flex, 
  Tabs, 
  Tab, 
  TabList, 
  TabPanel, 
  TabPanels, 
  AvatarGroup, 
  Avatar, 
  Stack, 
  Text, 
  Box, 
  Spinner,
  Center,
  useToast,
  Button,
  Heading,
  Container
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
      const response = await fetch('http://localhost:5000/api/user_status', {
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

  const handleLogin = () => {
    window.location.href = 'http://localhost:5000/login';
  };

  return (
    <Container maxW="1200px" py={6}>
      {error && (
        <Box bg="red.100" p={4} mb={4} borderRadius="md">
          <Text color="red.800">Error: {error}</Text>
          <Text>Please check if the backend API is running at localhost:5000</Text>
        </Box>
      )}
      
      <Tabs variant="enclosed" size="lg" colorScheme="green" isLazy>
        <TabList>
          <Tab>Music Comparison</Tab>
          <Tab>My Music</Tab>
        </TabList>
        
        <TabPanels>
          {/* Music Comparison Tab */}
          <TabPanel>
            <Box textAlign="center" py={10}>
              <Heading size="xl" mb={6}>Compare Your Music Taste</Heading>
              <AvatarGroup size="xl" max={2} mb={6} spacing="-1rem">
                {userData.player1.saved && (
                  <Avatar 
                    name={userData.player1.name} 
                    src={userData.player1.picture} 
                    bg="green.500"
                    boxSize="100px"
                    border="3px solid white"
                  />
                )}
                {userData.player2.saved ? (
                  <Avatar 
                    name={userData.player2.name} 
                    src={userData.player2.picture} 
                    bg="blue.500"
                    boxSize="100px"
                    border="3px solid white"
                  />
                ) : (
                  <Avatar 
                    name="Friend" 
                    src="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png" 
                    bg="gray.400"
                    boxSize="100px"
                    border="3px solid white"
                  />
                )}
              </AvatarGroup>
              
              <Text fontSize="lg" mb={6}>
                {userData.player1.saved && userData.player2.saved ? (
                  `Both users are logged in! Compare ${userData.player1.name} and ${userData.player2.name}'s music tastes.`
                ) : isAuthenticated ? (
                  "You're logged in! Now invite a friend to compare your music tastes."
                ) : (
                  "Login with Spotify to compare your music taste with friends."
                )}
              </Text>
              
              {isAuthenticated ? (
                <Button 
                  as="a" 
                  href="/compare" 
                  colorScheme="green" 
                  size="lg"
                >
                  Go to Comparison Page
                </Button>
              ) : (
                <LoginButton />
              )}
            </Box>
          </TabPanel>
          
          {/* My Music Tab */}
          <TabPanel bg="gray.50" borderRadius="md">
            {isLoading ? (
              <Center py={10}>
                <Spinner size="xl" color="green.500" />
              </Center>
            ) : isAuthenticated ? (
              <Box>
                <Heading size="md" mb={4} textAlign="center">
                  {userData?.player1?.name ? `${userData.player1.name}'s Top Music` : 'Your Top Music'}
                </Heading>
                <TabGroup />
              </Box>
            ) : (
              <Center py={10} flexDirection="column">
                <Text fontSize="lg" mb={4}>Please login to view your music</Text>
                <LoginButton />
              </Center>
            )}
          </TabPanel>
        </TabPanels>
      </Tabs>
    </Container>
  );
};

export default Sections;