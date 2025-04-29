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
  Button,
  Tabs,
  TabList,
  Tab,
  TabPanels,
  TabPanel,
  Badge,
  AspectRatio
} from '@chakra-ui/react';

const TabGroup = () => {
  const [userData, setUserData] = useState({
    player1: { saved: false, name: null, picture: null },
    player2: { saved: false, name: null, picture: null }
  });
  const [player1Tracks, setPlayer1Tracks] = useState({
    short: [],
    medium: [],
    long: []
  });
  const [player2Tracks, setPlayer2Tracks] = useState({
    short: [],
    medium: [],
    long: []
  });
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const toast = useToast();

  // Fetch user status
  const fetchUserStatus = useCallback(async () => {
    try {
      const token = localStorage.getItem('access_token');
      
      if (!token) {
        setIsLoading(false);
        return;
      }
      
      const response = await fetch("http://localhost:5000/api/user_status", {
        headers: {
          'Authorization': `Bearer ${token}`
        },
        credentials: 'include'
      });
      
      if (response.ok) {
        const result = await response.json();
        console.log("User status data:", result);
        setUserData(result);
        return result;
      } else {
        throw new Error("Failed to fetch user status");
      }
    } catch (error) {
      console.error("Error fetching user data:", error);
      setError("Failed to load user data");
      return null;
    }
  }, []);

  // Fetch comparison data which contains both users' track information
  const fetchComparisonData = useCallback(async () => {
    try {
      const token = localStorage.getItem('access_token');
      
      if (!token) return null;
      
      const response = await fetch("http://localhost:5000/api/comparison", {
        headers: {
          'Authorization': `Bearer ${token}`
        },
        credentials: 'include'
      });
      
      if (response.ok) {
        const data = await response.json();
        console.log("Comparison data:", data);
        return data;
      } else {
        console.error("Failed to fetch comparison data:", response.status);
        return null;
      }
    } catch (error) {
      console.error("Error fetching comparison data:", error);
      return null;
    }
  }, []);

  // Use the data from api/user_status and /api/save_data endpoints
  const loadUserData = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      // Fetch user status first
      const status = await fetchUserStatus();
      if (!status) {
        setIsLoading(false);
        return;
      }
      
      // If both users are logged in, try to fetch comparison data to get track information
      if (status.player1.saved && status.player2.saved) {
        const comparisonData = await fetchComparisonData();
        
        if (comparisonData) {
          // Extract track data for both players from different time ranges
          setPlayer1Tracks({
            short: comparisonData.short_term?.tracks?.player1 || [],
            medium: comparisonData.medium_term?.tracks?.player1 || [],
            long: comparisonData.long_term?.tracks?.player1 || []
          });
          
          setPlayer2Tracks({
            short: comparisonData.short_term?.tracks?.player2 || [],
            medium: comparisonData.medium_term?.tracks?.player2 || [],
            long: comparisonData.long_term?.tracks?.player2 || []
          });
        } else {
          // If comparison data fetch fails, try direct API calls to get individual player data
          await fetchDirectUserData();
        }
      } else {
        // If only one user is logged in, fetch their data directly
        await fetchDirectUserData();
      }
    } catch (error) {
      console.error("Error loading user data:", error);
      setError("Failed to load user data: " + error.message);
    } finally {
      setIsLoading(false);
    }
  }, [fetchUserStatus, fetchComparisonData]);

  // Direct fetch of user tracks from saved session data
  const fetchDirectUserData = useCallback(async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) return;
      
      // Try using the routes.py endpoint for each player
      if (userData.player1.saved) {
        // Player 1 data - short term
        const shortResponse = await fetch("http://localhost:5000/api/tracks/1/short", {
          headers: { 'Authorization': `Bearer ${token}` },
        });
        
        // Player 1 data - medium term
        const mediumResponse = await fetch("http://localhost:5000/api/tracks/1/medium", {
          headers: { 'Authorization': `Bearer ${token}` },
        });
        
        // Player 1 data - long term
        const longResponse = await fetch("http://localhost:5000/api/tracks/1/long", {
          headers: { 'Authorization': `Bearer ${token}` },
        });
        
        if (shortResponse.ok && mediumResponse.ok && longResponse.ok) {
          const shortData = await shortResponse.json();
          const mediumData = await mediumResponse.json();
          const longData = await longResponse.json();
          
          setPlayer1Tracks({
            short: shortData || [],
            medium: mediumData || [],
            long: longData || []
          });
        } else {
          // Fallback to test data if API endpoints aren't available
          await fetchTestData(1);
        }
      }
      
      if (userData.player2.saved) {
        // Similar requests for player 2
        const shortResponse = await fetch("http://localhost:5000/api/tracks/2/short", {
          headers: { 'Authorization': `Bearer ${token}` },
        });
        
        const mediumResponse = await fetch("http://localhost:5000/api/tracks/2/medium", {
          headers: { 'Authorization': `Bearer ${token}` },
        });
        
        const longResponse = await fetch("http://localhost:5000/api/tracks/2/long", {
          headers: { 'Authorization': `Bearer ${token}` },
        });
        
        if (shortResponse.ok && mediumResponse.ok && longResponse.ok) {
          const shortData = await shortResponse.json();
          const mediumData = await mediumResponse.json();
          const longData = await longResponse.json();
          
          setPlayer2Tracks({
            short: shortData || [],
            medium: mediumData || [],
            long: longData || []
          });
        } else {
          // Fallback to test data if API endpoints aren't available
          await fetchTestData(2);
        }
      }
    } catch (error) {
      console.error("Error fetching direct user data:", error);
      // Fall back to test data
      await fetchTestData(1);
      await fetchTestData(2);
    }
  }, [userData]);

  // Fallback to test data
  const fetchTestData = useCallback(async (playerId) => {
    try {
      const response = await fetch("http://localhost:5000/api/testdata");
      if (response.ok) {
        const testData = await response.json();
        // Convert test data format to match expected format
        const formattedData = testData.map(item => {
          if (Array.isArray(item)) {
            return {
              name: item[0],
              artists_name: item[1] || "Unknown Artist",
              image: item[2] || null
            };
          }
          return item;
        });
        
        // Use the test data as a fallback
        if (playerId === 1) {
          setPlayer1Tracks({
            short: formattedData,
            medium: formattedData,
            long: formattedData
          });
        } else {
          setPlayer2Tracks({
            short: formattedData,
            medium: formattedData,
            long: formattedData
          });
        }
      }
    } catch (error) {
      console.error(`Error fetching test data for Player ${playerId}:`, error);
    }
  }, []);

  // Initial data loading
  useEffect(() => {
    loadUserData();
  }, [loadUserData]);

  // Listen for auth changes
  useEffect(() => {
    const handleStorageChange = () => {
      const token = localStorage.getItem('access_token');
      if (token) {
        loadUserData();
      }
    };
    
    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, [loadUserData]);

  // Handle login for player 2
  const handleLoginPlayer2 = () => {
    window.location.href = `http://localhost:5000/api/login/2`;
  };

  // Component to display a single track
  const TrackCard = ({ track, rank, isTopTrack = false }) => (
    <Card 
      height="100%" 
      boxShadow="md" 
      borderRadius="lg" 
      overflow="hidden"
      transition="transform 0.3s"
      _hover={{ transform: 'translateY(-5px)', boxShadow: 'lg' }}
    >
      <Box position="relative">
        <AspectRatio ratio={1}>
          {track.image ? (
            <Image 
              src={track.image} 
              alt={track.name || "Track image"} 
              objectFit="cover"
              fallback={
                <Box bg="gray.200" display="flex" alignItems="center" justifyContent="center">
                  <Text fontSize="sm" color="gray.600">{track.name || "Unknown Track"}</Text>
                </Box>
              }
            />
          ) : (
            <Box bg="gray.200" display="flex" alignItems="center" justifyContent="center">
              <Text fontSize="sm" color="gray.600">{track.name || "Unknown Track"}</Text>
            </Box>
          )}
        </AspectRatio>
        <Badge 
          position="absolute" 
          top="8px" 
          left="8px" 
          colorScheme={rank === 1 ? "green" : "gray"} 
          fontSize={isTopTrack ? "xl" : "md"}
          px="2"
          py="1"
          borderRadius="full"
        >
          #{rank}
        </Badge>
      </Box>
      
      <CardBody p={3}>
        <VStack align="start" spacing={1}>
          <Text 
            fontWeight="bold" 
            fontSize={isTopTrack ? "xl" : "md"} 
            noOfLines={1}
          >
            {track.name || "Unknown Track"}
          </Text>
          <Text 
            color="gray.600" 
            fontSize={isTopTrack ? "md" : "sm"} 
            noOfLines={1}
          >
            {track.artists_name || "Unknown Artist"}
          </Text>
        </VStack>
      </CardBody>
    </Card>
  );

  // Component to display tracks for a specific time period
  const TrackTimeDisplay = ({ tracks, title }) => {
    console.log("Track time display data:", title, tracks);
    
    // Ensure we have at least 10 tracks to display
    const displayTracks = tracks?.slice(0, 10) || [];
    
    // Pad with empty tracks if less than 10
    while (displayTracks.length < 10) {
      displayTracks.push({ name: "No track data", artists_name: "", image: "" });
    }
    
    const topTrack = displayTracks[0];
    const otherTracks = displayTracks.slice(1, 10);
    
    return (
      <Box>
        <Heading size="md" mb={4} textAlign="center">{title}</Heading>
        
        {/* Top track highlighted */}
        <Box mb={6}>
          {topTrack && (
            <TrackCard track={topTrack} rank={1} isTopTrack={true} />
          )}
        </Box>
        
        {/* 3x3 grid of other tracks */}
        <SimpleGrid columns={{ base: 1, sm: 2, md: 3 }} spacing={4}>
          {otherTracks.map((track, index) => (
            <TrackCard 
              key={index} 
              track={track} 
              rank={index + 2} 
              isTopTrack={false} 
            />
          ))}
        </SimpleGrid>
      </Box>
    );
  };

  // Component to display user profile card
  const UserProfileCard = ({ userData, isPlayer2 = false }) => (
    <Card mb={6} p={4} boxShadow="md">
      <CardBody>
        <Center flexDirection="column">
          {userData.saved ? (
            <VStack spacing={3}>
              <Avatar 
                size="xl" 
                name={userData.name} 
                src={userData.picture} 
                mb={2}
              />
              <Heading size="md">{userData.name}</Heading>
              <Text color="gray.600">{isPlayer2 ? "Player 2" : "Player 1"}</Text>
            </VStack>
          ) : (
            <VStack spacing={3}>
              <Avatar size="xl" mb={2} />
              <Heading size="md">{isPlayer2 ? "Player 2" : "Player 1"}</Heading>
              <Text color="gray.600">Not logged in</Text>
              {!isPlayer2 || userData.player1?.saved ? (
                <Button 
                  colorScheme="green" 
                  onClick={isPlayer2 ? handleLoginPlayer2 : null}
                  size="sm"
                  mt={2}
                >
                  {isPlayer2 ? "Login Player 2" : "Login"}
                </Button>
              ) : null}
            </VStack>
          )}
        </Center>
      </CardBody>
    </Card>
  );

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

  return (
    <Flex width="100%" direction={{ base: "column", md: "row" }}>
      {/* Player 1 Section */}
      <Box p={4} width={{ base: "100%", md: "50%" }}>
        <UserProfileCard userData={userData.player1} />
        
        {userData.player1.saved ? (
          <Tabs variant="enclosed" colorScheme="green" isLazy>
            <TabList>
              <Tab>Short Term</Tab>
              <Tab>Medium Term</Tab>
              <Tab>Long Term</Tab>
            </TabList>
            
            <TabPanels>
              <TabPanel>
                <TrackTimeDisplay 
                  tracks={player1Tracks.short} 
                  title={`${userData.player1.name}'s Recent Favorites`} 
                />
              </TabPanel>
              <TabPanel>
                <TrackTimeDisplay 
                  tracks={player1Tracks.medium} 
                  title={`${userData.player1.name}'s 6-Month Favorites`} 
                />
              </TabPanel>
              <TabPanel>
                <TrackTimeDisplay 
                  tracks={player1Tracks.long} 
                  title={`${userData.player1.name}'s All-Time Favorites`} 
                />
              </TabPanel>
            </TabPanels>
          </Tabs>
        ) : (
          <Center p={8} borderWidth="1px" borderRadius="lg" bg="gray.50">
            <Text>Login to view your top tracks</Text>
          </Center>
        )}
      </Box>
      
      <Divider orientation={{ base: 'horizontal', md: 'vertical' }} 
               height={{ md: "auto" }} 
               width={{ base: "100%", md: "1px" }} 
               mx={{ md: 4 }}
               my={{ base: 4, md: 0 }}
               color="gray.200" />
      
      {/* Player 2 Section */}
      <Box p={4} width={{ base: "100%", md: "50%" }}>
        <UserProfileCard userData={userData.player2} isPlayer2={true} />
        
        {userData.player2.saved ? (
          <Tabs variant="enclosed" colorScheme="blue" isLazy>
            <TabList>
              <Tab>Short Term</Tab>
              <Tab>Medium Term</Tab>
              <Tab>Long Term</Tab>
            </TabList>
            
            <TabPanels>
              <TabPanel>
                <TrackTimeDisplay 
                  tracks={player2Tracks.short} 
                  title={`${userData.player2.name}'s Recent Favorites`} 
                />
              </TabPanel>
              <TabPanel>
                <TrackTimeDisplay 
                  tracks={player2Tracks.medium} 
                  title={`${userData.player2.name}'s 6-Month Favorites`} 
                />
              </TabPanel>
              <TabPanel>
                <TrackTimeDisplay 
                  tracks={player2Tracks.long} 
                  title={`${userData.player2.name}'s All-Time Favorites`} 
                />
              </TabPanel>
            </TabPanels>
          </Tabs>
        ) : (
          <Center p={8} borderWidth="1px" borderRadius="lg" bg="gray.50">
            <Text>Login Player 2 to view their top tracks</Text>
          </Center>
        )}
      </Box>
    </Flex>
  );
};

export default TabGroup;