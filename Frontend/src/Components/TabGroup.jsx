import React, { useEffect, useState, useCallback } from 'react';
import { 
  Flex,  
  Text,  
  Card, 
  CardBody, 
  SimpleGrid, 
  Box, 
  Divider,
  Image,
  Spinner,
  Center,
  useToast,
  Heading,
  Avatar,
  VStack,
  HStack,
  Button
} from '@chakra-ui/react';

const TabGroup = () => {
  const [data, setData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [userData, setUserData] = useState({
    player1: { saved: false, name: null, picture: null },
    player2: { saved: false, name: null, picture: null }
  });
  const toast = useToast();

  // Fetch user data
  const fetchUserData = useCallback(async () => {
    try {
      const token = localStorage.getItem('access_token');
      
      if (!token) return;
      
      const response = await fetch("http://localhost:5000/api/user_status", {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        const result = await response.json();
        setUserData(result);
      }
    } catch (error) {
      console.error("Error fetching user data:", error);
    }
  }, []);

  // Fetch music data
  const getData = useCallback(async () => {
    const response = await fetch("http://localhost:5000/api/card_data", {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    console.log("Response status:", response.status);
    const result = await response.json();
    console.log("API Response:", result);
    
    try {
      setIsLoading(true);
      const token = localStorage.getItem('access_token');
      
      if (!token) {
        setIsLoading(false);
        return; // Don't attempt to fetch without a token
      }
      
      // First try the card_data endpoint
      let response = await fetch("http://localhost:5000/api/card_data", {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      // If that fails, fall back to the testdata endpoint
      if (!response.ok) {
        response = await fetch("http://localhost:5000/api/testdata");
        
        if (!response.ok) {
          throw new Error(`Error fetching data: ${response.status}`);
        }
      }
      
      const result = await response.json();
      console.log("Fetched Data:", result); 
      setData(result);
      setIsLoading(false);
    } catch (error) {
      console.error("Error fetching data:", error);
      setError(error.message);
      setIsLoading(false);
      
      toast({
        title: "Error fetching music data",
        description: error.message,
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    }
  }, [toast]);

  // Fetch both user data and music data
  const fetchAllData = useCallback(() => {
    fetchUserData();
    getData();
  }, [fetchUserData, getData]);

  // Initial data fetch
  useEffect(() => {
    fetchAllData();
  }, [fetchAllData]);

  // Listen for auth state changes
  useEffect(() => {
    const handleAuthChange = () => {
      const token = localStorage.getItem('access_token');
      if (token) {
        fetchAllData();
      }
    };
    
    window.addEventListener('storage', handleAuthChange);
    return () => window.removeEventListener('storage', handleAuthChange);
  }, [fetchAllData]);

  // Handle login for player 2
  const handleLoginPlayer2 = () => {
    window.location.href = `http://localhost:5000/api/login/2`;
  };

  if (isLoading) {
    return (
      <Center h="300px">
        <Spinner size="xl" color="green.500" />
      </Center>
    );
  }

  if (error) {
    return (
      <Center h="300px" flexDirection="column">
        <Text color="red.500" mb={4}>Error loading music data</Text>
        <Text fontSize="sm">Details: {error}</Text>
      </Center>
    );
  }

  if (data.length === 0) {
    return (
      <Center h="300px">
        <Text>No music data available. Please login with Spotify to see your top tracks.</Text>
      </Center>
    );
  }

  return (
    <Flex width="100%" direction={{ base: "column", md: "row" }}>
      <Box p={4} width={{ base: "100%", md: "50%" }}>
        <Card mb={6} p={4} boxShadow="md">
          <CardBody>
            <Center flexDirection="column">
              {userData.player1.saved ? (
                <VStack spacing={3}>
                  <Avatar 
                    size="xl" 
                    name={userData.player1.name} 
                    src={userData.player1.picture} 
                    mb={2}
                  />
                  <Heading size="md">{userData.player1.name}</Heading>
                  <Text color="gray.600">Player 1</Text>
                </VStack>
              ) : (
                <VStack spacing={3}>
                  <Avatar size="xl" mb={2} />
                  <Heading size="md">Player 1</Heading>
                  <Text color="gray.600">Not logged in</Text>
                </VStack>
              )}
            </Center>
          </CardBody>
        </Card>
        
        <Heading size="md" mb={4} textAlign="center">Your Top Tracks</Heading>
        <SimpleGrid columns={{ base: 1, sm: 2, md: 3 }} spacing={4}>
          {data.slice(0, 9).map((song, i) => (
            <Card key={i} width="100%" height="100%" align="center" justify="center" boxShadow="md">
              <CardBody>
                <Text fontSize="xl" fontWeight="bold" mb={2}>{i+1}.</Text>
                <Image 
                  src={Array.isArray(song) ? song[2] : song.image} 
                  alt={Array.isArray(song) ? song[0] : song.name} 
                  height="100px" 
                  objectFit="cover"
                  borderRadius="md"
                  fallbackSrc="https://via.placeholder.com/100"
                  mb={2}
                />
                <Text fontSize="md" fontWeight="bold" mt={2} noOfLines={1}>
                  {Array.isArray(song) ? song[0] : song.name}
                </Text>
                <Text fontSize="sm" color="gray.500" noOfLines={1}>
                  {Array.isArray(song) ? song[1] : song.artists_name}
                </Text>
              </CardBody>
            </Card>
          ))}
        </SimpleGrid>
      </Box>
      
      <Divider orientation={{ base: 'horizontal', md: 'vertical' }} 
               height={{ md: "auto" }} 
               width={{ base: "100%", md: "1px" }} 
               mx={{ md: 4 }}
               my={{ base: 4, md: 0 }}
               color="gray.200" />
      
      <Box p={4} width={{ base: "100%", md: "50%" }}>
        <Card mb={6} p={4} boxShadow="md">
          <CardBody>
            <Center flexDirection="column">
              {userData.player2.saved ? (
                <VStack spacing={3}>
                  <Avatar 
                    size="xl" 
                    name={userData.player2.name} 
                    src={userData.player2.picture} 
                    mb={2}
                  />
                  <Heading size="md">{userData.player2.name}</Heading>
                  <Text color="gray.600">Player 2</Text>
                </VStack>
              ) : (
                <VStack spacing={3}>
                  <Avatar size="xl" mb={2} />
                  <Heading size="md">Player 2</Heading>
                  <Text color="gray.600">Not logged in</Text>
                  {userData.player1.saved && (
                    <Button 
                      colorScheme="green" 
                      onClick={handleLoginPlayer2}
                      size="sm"
                      mt={2}
                    >
                      Login Player 2
                    </Button>
                  )}
                </VStack>
              )}
            </Center>
          </CardBody>
        </Card>
        
        <Heading size="md" mb={4} textAlign="center">
          {userData.player2.saved ? `${userData.player2.name}'s Top Tracks` : "Friend's Top Tracks"}
        </Heading>
        <SimpleGrid columns={{ base: 1, sm: 2, md: 3 }} spacing={4}>
          {userData.player2.saved ? (
            // If player 2 is logged in, their tracks would appear here
            // You would need to fetch and display player 2's tracks
            [...Array(9)].map((_, i) => (
              <Card key={i} width="100%" height="150px" align="center" justify="center" boxShadow="md" bg="blue.50">
                <CardBody display="flex" alignItems="center" justifyContent="center">
                  <Text fontSize="md" color="blue.600">Track {i+1}</Text>
                </CardBody>
              </Card>
            ))
          ) : (
            // Placeholder cards when player 2 is not logged in
            [...Array(9)].map((_, i) => (
              <Card key={i} width="100%" height="150px" align="center" justify="center" boxShadow="md" bg="gray.50">
                <CardBody display="flex" alignItems="center" justifyContent="center">
                  <Text fontSize="md" color="gray.500">Login Player 2 to view</Text>
                </CardBody>
              </Card>
            ))
          )}
        </SimpleGrid>
      </Box>
    </Flex>
  );
};

export default TabGroup;