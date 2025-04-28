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
  useToast
} from '@chakra-ui/react';
import React, { useEffect, useState, useCallback } from 'react';
import TabGroup from './TabGroup';
import LoginButton from './LoginButton';

const Sections = () => {
  const [data, setData] = useState([]);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const toast = useToast();

  // Check authentication status
  const checkAuthStatus = useCallback(() => {
    const token = localStorage.getItem('access_token');
    setIsAuthenticated(!!token);
    return !!token;
  }, []);

  // Fetch data from Flask API
  const getData = useCallback(async () => {
    try {
      setIsLoading(true);
      const response = await fetch("http://localhost:5000/api/testdata");
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }
      const result = await response.json();
      console.log("Fetched Data:", result); 
      setData(result);
    } catch (error) {
      console.error("Error fetching data:", error);
      setError(error.message);
      
      toast({
        title: "Error fetching data",
        description: "Could not connect to the backend server. Make sure it's running.",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  }, [toast]);

  // Initial data load
  useEffect(() => {
    getData();
    checkAuthStatus();
    
    // Listen for auth state changes
    const handleStorageChange = (e) => {
      if (e.key === 'access_token') {
        checkAuthStatus();
      }
    };
    
    window.addEventListener('storage', handleStorageChange);
    
    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, [getData, checkAuthStatus]);

  return (
    <Stack>
      {error && (
        <Box bg="red.100" p={4} mb={4} borderRadius="md">
          <Text color="red.800">Error: {error}</Text>
          <Text>API may not be running. Make sure backend is started at localhost:5000</Text>
        </Box>
      )}
      
      {isLoading ? (
        <Center p={10}>
          <Spinner size="xl" color="green.500" />
        </Center>
      ) : (
        <>
          <Flex width={'100%'} alignContent={"center"} justifyContent={"center"}>
            <AvatarGroup alignContent={"center"} justifyContent={"center"} >
              <Avatar name="User 1" src="https://ui-avatars.com/api/?name=Spotify+User" size={"2xl"} />
              <Avatar name="User 2" src="https://ui-avatars.com/api/?name=Music+Friend" size={"2xl"} />
            </AvatarGroup>
          </Flex>
          <Tabs variant='enclosed' size={'lg'} width={'100%'} align='center' alignContent={"center"} position="absolute" top="50%" transform="translateY(-50%)">
            <TabList>
              <Tab>Song Comparison</Tab>
              <Tab>Music Taste</Tab>
            </TabList>
            <TabPanels>
              <TabPanel>
                <Text fontSize="xl" mb={4}>Welcome to Spotify Comparison!</Text>
                {isAuthenticated ? (
                  <Text color="green.500" fontWeight="bold">
                    You're logged in. Go to the "Music Taste" tab to see your data.
                  </Text>
                ) : (
                  <LoginButton />
                )}
              </TabPanel>
              <TabPanel bg={"gray.100"} borderRadius="md">
                {isAuthenticated ? (
                  <TabGroup />
                ) : (
                  <Center py={10}>
                    <Text>Please login first to view your music taste</Text>
                  </Center>
                )}
              </TabPanel>
            </TabPanels>
          </Tabs>
        </>
      )}
    </Stack>
  );
};

export default Sections;