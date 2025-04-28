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
  useToast
} from '@chakra-ui/react';

const TabGroup = () => {
  const [data, setData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const toast = useToast();

  const getData = useCallback(async () => {
    try {
      setIsLoading(true);
      const token = localStorage.getItem('access_token');
      
      if (!token) {
        setIsLoading(false);
        return; // Don't attempt to fetch without a token
      }
      
      const response = await fetch("http://localhost:5000/api/card_data", {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (!response.ok) {
        throw new Error(`Error fetching data: ${response.status}`);
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
        title: "Error fetching data",
        description: error.message,
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    }
  }, [toast]);

  // Initial data fetch
  useEffect(() => {
    getData();
  }, [getData]);

  // Listen for auth state changes
  useEffect(() => {
    const checkToken = () => {
      const token = localStorage.getItem('access_token');
      if (token && data.length === 0) {
        getData();
      }
    };
    
    // Check immediately and then set up a periodic check
    checkToken();
    
    // Set up event listener for storage changes
    window.addEventListener('storage', checkToken);
    
    // Also check every 30 seconds in case the token was just added
    const interval = setInterval(checkToken, 30000);
    
    return () => {
      window.removeEventListener('storage', checkToken);
      clearInterval(interval);
    };
  }, [getData, data.length]);

  if (isLoading) {
    return (
      <Center h="300px">
        <Spinner size="xl" color="green.500" />
      </Center>
    );
  }

  if (error) {
    return (
      <Center h="300px">
        <Text color="red.500">Error loading data. Please try again.</Text>
      </Center>
    );
  }

  if (data.length === 0) {
    return (
      <Center h="300px">
        <Text>No data available. Please login to see your top tracks.</Text>
      </Center>
    );
  }

  return (
    <Flex width={'100%'}>
      <Box p={4} width={"50%"}>
        <SimpleGrid columns={3} spacing={4}>
          {data.slice(0, 9).map((song, i) => (
            <Card key={i} width="100%" height="100%" align="center" justify="center">
              <CardBody>
                <Text fontSize="xl" fontWeight="bold">{i+1}.</Text>
                <Image 
                  src={song[2]} 
                  alt={song[0]} 
                  height="100px" 
                  fallbackSrc="https://via.placeholder.com/100"
                />
                <Text fontSize="md" fontWeight="bold" mt={2} noOfLines={1}>{song[0]}</Text>
                <Text fontSize="sm" color="gray.500" noOfLines={1}>{song[1]}</Text>
              </CardBody>
            </Card>
          ))}
        </SimpleGrid>
      </Box>
      <Divider orientation='vertical' height={"100%"} width={"1px"} color={"blackAlpha.100"} />
      <Box p={4} width={"50%"}>
        <SimpleGrid columns={3} spacing={4}>
          {Array.from({ length: 9 }, (_, i) => (
            <Card key={i} width="100%" height="150px" align="center" justify="center">
              <CardBody>
                <Text fontSize="xl" fontWeight="bold">Card {i + 1}</Text>
              </CardBody>
            </Card>
          ))}
        </SimpleGrid>
      </Box>
    </Flex>
  );
};

export default TabGroup;