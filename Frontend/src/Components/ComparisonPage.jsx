import config from '../config';
import { useEffect, useState, useCallback, useRef } from 'react';
import { 
  Box, 
  Flex, 
  Heading, 
  Text, 
  SimpleGrid, 
  Card, 
  CardBody, 
  Avatar, 
  Tabs, 
  TabList, 
  Tab, 
  TabPanels, 
  TabPanel, 
  Progress, 
  Stat, 
  StatLabel, 
  StatNumber, 
  StatHelpText, 
  StatGroup,
  Stack,
  Divider,
  Image,
  Button,
  Center,
  VStack,
  HStack,
  Badge,
  Spinner,
  useToast
} from '@chakra-ui/react';

// Custom hook for setInterval with React
const useInterval = (callback, delay) => {
  const savedCallback = useRef();

  // Remember the latest callback
  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  // Set up the interval
  useEffect(() => {
    function tick() {
      savedCallback.current();
    }
    if (delay !== null) {
      const id = setInterval(tick, delay);
      return () => clearInterval(id);
    }
  }, [delay]);
};

const ComparisonPage = () => {
  const [comparison, setComparison] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [userStatus, setUserStatus] = useState({
    player1: { saved: false, name: null, picture: null },
    player2: { saved: false, name: null, picture: null }
  });
  const toast = useToast();

  // Memoize fetch functions so they can be used in useEffect dependencies
  const fetchUserStatus = useCallback(async () => {
    try {
      const response = await fetch(config.API_URL +'/api/user_status', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      
      if (!response.ok) {
        throw new Error('Failed to fetch user status');
      }
      
      const data = await response.json();
      console.log("User status data:", data);
      setUserStatus(data);
      return data;
    } catch (error) {
      console.error('Error fetching user status:', error);
      setError(error.message);
      return null;
    }
  }, []);

  // Fetch comparison data
  const fetchComparison = useCallback(async () => {
    try {
      setIsLoading(true);
      const response = await fetch(config.API_URL +'/api/comparison', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      
      if (!response.ok) {
        throw new Error('Failed to fetch comparison data');
      }
      
      const data = await response.json();
      setComparison(data);
      setIsLoading(false);
    } catch (error) {
      console.error('Error fetching comparison:', error);
      setError(error.message);
      setIsLoading(false);
    }
  }, []);

  // Reset a specific player
  const resetPlayer = async (playerId) => {
    try {
      const response = await fetch(config.API_URL + `/api/reset/${playerId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      
      if (!response.ok) {
        throw new Error('Failed to reset player');
      }
      
      await fetchUserStatus();
      // Reset comparison data if one user is reset
      setComparison(null);
      
      toast({
        title: "Player Reset",
        description: `Player ${playerId} data has been reset.`,
        status: "success",
        duration: 3000,
        isClosable: true,
      });
    } catch (error) {
      console.error('Error resetting player:', error);
      toast({
        title: "Reset Failed",
        description: error.message,
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    }
  };

  // Handle login for a specific player
  const handleLogin = (playerId) => {
    const apiUrl = import.meta.env.VITE_API_URL || 'https://your-backend-url.onrender.com';
    window.location.href = `${apiUrl}/api/login/${playerId}`;
  };
  
  // Check for status updates more frequently when waiting for users
  useInterval(() => {
    if (!userStatus.player1.saved || !userStatus.player2.saved) {
      fetchUserStatus();
    }
  }, 5000);

  // Initial load
  useEffect(() => {
    const initPage = async () => {
      const status = await fetchUserStatus();
      
      // If both users are logged in, fetch comparison data
      if (status && status.player1.saved && status.player2.saved) {
        fetchComparison();
      } else {
        setIsLoading(false);
      }
    };
    
    initPage();
    
    // Listen for changes from auth redirects
    const handleStorageChange = () => {
      fetchUserStatus();
    };
    
    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, [fetchUserStatus, fetchComparison]);

  // When both users become logged in, fetch comparison
  useEffect(() => {
    if (userStatus.player1.saved && userStatus.player2.saved && !comparison) {
      fetchComparison();
    }
  }, [userStatus, comparison, fetchComparison]);

  const renderUserCard = (player, playerId) => (
    <Card maxW="sm" mx="auto" boxShadow="md" borderWidth="1px" overflow="hidden">
      <Box bg="green.500" h="8px" w="100%" />
      <CardBody>
        <Center flexDirection="column">
          {player.saved ? (
            <>
              <Avatar 
                size="2xl" 
                name={player.name} 
                src={player.picture} 
                mb={4} 
                border="4px solid"
                borderColor="green.500"
              />
              <Heading size="md" mb={2}>{player.name}</Heading>
              <Badge colorScheme="green" mb={4} fontSize="0.8em" px={2} py={1}>CONNECTED</Badge>
              <Button colorScheme="red" size="sm" onClick={() => resetPlayer(playerId)} mt={2}>
                Reset User
              </Button>
            </>
          ) : (
            <>
              <Avatar 
                size="2xl" 
                mb={4} 
                bg="gray.200"
                icon={<Text fontSize="4xl" color="gray.400">?</Text>}
              />
              <Heading size="md" mb={2}>Player {playerId}</Heading>
              <Badge colorScheme="red" mb={4} fontSize="0.8em" px={2} py={1}>NOT CONNECTED</Badge>
              <Button 
                colorScheme="green" 
                onClick={() => handleLogin(playerId)}
                size="md"
                borderRadius="full"
                px={6}
              >
                Login with Spotify
              </Button>
            </>
          )}
        </Center>
      </CardBody>
    </Card>
  );

  const renderScoreCard = (title, score, color = "green") => (
    <Stat 
      p={4} 
      borderRadius="md" 
      boxShadow="sm" 
      borderWidth="1px" 
      borderColor={`${color}.200`}
      bg={`${color}.50`}
    >
      <StatLabel fontSize="lg">{title}</StatLabel>
      <StatNumber fontSize="3xl">{score}%</StatNumber>
      <Progress 
        value={score} 
        colorScheme={color} 
        size="sm" 
        mt={2} 
        borderRadius="full"
      />
    </Stat>
  );

  // If there's an error, show the error message
  if (error) {
    return (
      <Box p={8} textAlign="center">
        <Heading mb={4} color="red.500">Error</Heading>
        <Text fontSize="xl">{error}</Text>
        <Button mt={4} colorScheme="blue" onClick={() => window.location.reload()}>
          Retry
        </Button>
      </Box>
    );
  }

  return (
    <Box p={6} maxW="1200px" mx="auto">
      <Heading mb={8} textAlign="center">Spotify Music Taste Comparison</Heading>
      
      {/* User Cards */}
      <SimpleGrid columns={{ base: 1, md: 2 }} spacing={10} mb={10}>
        {renderUserCard(userStatus.player1, 1)}
        {renderUserCard(userStatus.player2, 2)}
      </SimpleGrid>
      
      {isLoading && (
        <Center py={10}>
          <VStack>
            <Spinner size="xl" color="green.500" thickness="4px" speed="0.65s" />
            <Text mt={4}>Loading comparison data...</Text>
          </VStack>
        </Center>
      )}
      
      {!isLoading && !comparison && userStatus.player1.saved && userStatus.player2.saved && (
        <Center py={10}>
          <VStack>
            <Text fontSize="xl">Ready to compare music tastes!</Text>
            <Button mt={4} colorScheme="green" onClick={fetchComparison}>
              Generate Comparison
            </Button>
          </VStack>
        </Center>
      )}
      
      {!isLoading && !(userStatus.player1.saved && userStatus.player2.saved) && (
        <Center py={10}>
          <VStack>
            <Text fontSize="xl">Please connect both Spotify accounts to compare music tastes</Text>
          </VStack>
        </Center>
      )}
      
      {/* Comparison Results */}
      {!isLoading && comparison && (
        <Box mt={6}>
          <Tabs variant="enclosed" isFitted colorScheme="green">
            <TabList>
              <Tab>Short Term (4 weeks)</Tab>
              <Tab>Medium Term (6 months)</Tab>
              <Tab>Long Term (Years)</Tab>
            </TabList>
            
            <TabPanels>
              {/* Short Term Results */}
              <TabPanel>
                <Box borderWidth="1px" borderRadius="lg" overflow="hidden" p={5}>
                  <Heading size="lg" mb={4} textAlign="center">Short Term Compatibility: {comparison.short_term.finalScore}%</Heading>
                  
                  <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={5} mb={6}>
                    {renderScoreCard("Top Songs Similarity", comparison.short_term.topSongsScore, "purple")}
                    {renderScoreCard("Genre Similarity", comparison.short_term.genresScore, "blue")}
                    {renderScoreCard("Era Similarity", comparison.short_term.erasScore, "orange")}
                  </SimpleGrid>
                  
                  <Divider my={6} />
                  
                  {/* Top Shared Song */}
                  <VStack spacing={4} mb={8}>
                    <Heading size="md">Top Shared Song</Heading>
                    <HStack spacing={4} p={4} borderWidth="1px" borderRadius="md" w="full" maxW="md" mx="auto">
                      <Image 
                        boxSize="80px"
                        borderRadius="md"
                        src={comparison.short_term.topSong.image || "https://via.placeholder.com/80"}
                        alt={comparison.short_term.topSong.name}
                        fallbackSrc="https://via.placeholder.com/80"
                      />
                      <Box>
                        <Text fontWeight="bold">{comparison.short_term.topSong.name}</Text>
                        <Text color="gray.600">{comparison.short_term.topSong.artists_name}</Text>
                      </Box>
                    </HStack>
                  </VStack>
                </Box>
              </TabPanel>
              
              {/* Medium Term Results */}
              <TabPanel>
                <Box borderWidth="1px" borderRadius="lg" overflow="hidden" p={5}>
                  <Heading size="lg" mb={4} textAlign="center">Medium Term Compatibility: {comparison.medium_term.finalScore}%</Heading>
                  
                  <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={5} mb={6}>
                    {renderScoreCard("Top Songs Similarity", comparison.medium_term.topSongsScore, "purple")}
                    {renderScoreCard("Genre Similarity", comparison.medium_term.genresScore, "blue")}
                    {renderScoreCard("Era Similarity", comparison.medium_term.erasScore, "orange")}
                  </SimpleGrid>
                  
                  <Divider my={6} />
                  
                  {/* Top Shared Song */}
                  <VStack spacing={4} mb={8}>
                    <Heading size="md">Top Shared Song</Heading>
                    <HStack spacing={4} p={4} borderWidth="1px" borderRadius="md" w="full" maxW="md" mx="auto">
                      <Image 
                        boxSize="80px"
                        borderRadius="md"
                        src={comparison.medium_term.topSong.image || "https://via.placeholder.com/80"}
                        alt={comparison.medium_term.topSong.name}
                        fallbackSrc="https://via.placeholder.com/80"
                      />
                      <Box>
                        <Text fontWeight="bold">{comparison.medium_term.topSong.name}</Text>
                        <Text color="gray.600">{comparison.medium_term.topSong.artists_name}</Text>
                      </Box>
                    </HStack>
                  </VStack>
                </Box>
              </TabPanel>
              
              {/* Long Term Results */}
              <TabPanel>
                <Box borderWidth="1px" borderRadius="lg" overflow="hidden" p={5}>
                  <Heading size="lg" mb={4} textAlign="center">Long Term Compatibility: {comparison.long_term.finalScore}%</Heading>
                  
                  <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={5} mb={6}>
                    {renderScoreCard("Top Songs Similarity", comparison.long_term.topSongsScore, "purple")}
                    {renderScoreCard("Genre Similarity", comparison.long_term.genresScore, "blue")}
                    {renderScoreCard("Era Similarity", comparison.long_term.erasScore, "orange")}
                  </SimpleGrid>
                  
                  <Divider my={6} />
                  
                  {/* Top Shared Song */}
                  <VStack spacing={4} mb={8}>
                    <Heading size="md">Top Shared Song</Heading>
                    <HStack spacing={4} p={4} borderWidth="1px" borderRadius="md" w="full" maxW="md" mx="auto">
                      <Image 
                        boxSize="80px"
                        borderRadius="md"
                        src={comparison.long_term.topSong.image || "https://via.placeholder.com/80"}
                        alt={comparison.long_term.topSong.name}
                        fallbackSrc="https://via.placeholder.com/80"
                      />
                      <Box>
                        <Text fontWeight="bold">{comparison.long_term.topSong.name}</Text>
                        <Text color="gray.600">{comparison.long_term.topSong.artists_name}</Text>
                      </Box>
                    </HStack>
                  </VStack>
                </Box>
              </TabPanel>
            </TabPanels>
          </Tabs>
        </Box>
      )}
    </Box>
  );
};

export default ComparisonPage;