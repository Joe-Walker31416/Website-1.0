import React, { useEffect, useState, useCallback } from 'react';
import { 
  Flex,  
  Text,  
  Card, 
  CardBody,
  CardHeader,
  CardFooter, 
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
  Button,
  Tabs,
  TabList,
  Tab,
  TabPanels,
  TabPanel,
  Badge,
  Grid,
  GridItem,
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

  // Fetch tracks for a specific player and time range
  const fetchPlayerTracks = useCallback(async (playerId, timeRange) => {
    try {
      const token = localStorage.getItem('access_token');
      
      if (!token) return [];
      
      const response = await fetch(`http://localhost:5000/api/player/${playerId}/tracks?time_range=${timeRange}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        },
        credentials: 'include'
      });
      
      if (response.ok) {
        const data = await response.json();
        return data.tracks || [];
      } else {
        // If API fails, try to use test data
        const testResponse = await fetch("http://localhost:5000/api/testdata");
        if (testResponse.ok) {
          const testData = await testResponse.json();
          // Convert test data format to match expected format
          return testData.map(item => {
            if (Array.isArray(item)) {
              return {
                name: item[0],
                artists_name: item[1] || "Unknown Artist",
                image: item[2] || "https://via.placeholder.com/300"
              };
            }
            return item;
          });
        }
        console.error(`Failed to fetch tracks for Player ${playerId}`);
        return [];
      }
    } catch (error) {
      console.error(`Error fetching tracks for Player ${playerId}:`, error);
      return [];
    }
  }, []);

  // Load all track data
  const loadAllTrackData = useCallback(async () => {
    setIsLoading(true);
    
    const status = await fetchUserStatus();
    if (!status) {
      setIsLoading(false);
      return;
    }
    
    // Load tracks for player 1 if logged in
    if (status.player1.saved) {
      const shortTracks = await fetchPlayerTracks(1, 'short');
      const mediumTracks = await fetchPlayerTracks(1, 'medium');
      const longTracks = await fetchPlayerTracks(1, 'long');
      
      setPlayer1Tracks({
        short: shortTracks,
        medium: mediumTracks,
        long: longTracks
      });
    }
    
    // Load tracks for player 2 if logged in
    if (status.player2.saved) {
      const shortTracks = await fetchPlayerTracks(2, 'short');
      const mediumTracks = await fetchPlayerTracks(2, 'medium');
      const longTracks = await fetchPlayerTracks(2, 'long');
      
      setPlayer2Tracks({
        short: shortTracks,
        medium: mediumTracks,
        long: longTracks
      });
    }
    
    setIsLoading(false);
  }, [fetchUserStatus, fetchPlayerTracks]);

  // Initial data loading
  useEffect(() => {
    loadAllTrackData();
  }, [loadAllTrackData]);

  // Listen for auth changes
  useEffect(() => {
    const handleStorageChange = () => {
      const token = localStorage.getItem('access_token');
      if (token) {
        loadAllTrackData();
      }
    };
    
    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, [loadAllTrackData]);

  // Handle login for player 2
  const handleLoginPlayer2 = () => {
    window.location.href = `http://localhost:5000/api/login/2`;
  };

  // Component to display a single track
  const TrackCard = ({ track, rank, isTopTrack = false }) => (
    <Card 
      height={isTopTrack ? "100%" : "100%"} 
      boxShadow="md" 
      borderRadius="lg" 
      overflow="hidden"
      transition="transform 0.3s"
      _hover={{ transform: 'translateY(-5px)', boxShadow: 'lg' }}
    >
      <Box position="relative">
        <AspectRatio ratio={1}>
          <Image 
            src={track.image} 
            alt={track.name} 
            objectFit="cover"
            fallbackSrc="https://via.placeholder.com/300?text=No+Image" 
          />
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
            {track.name}
          </Text>
          <Text 
            color="gray.600" 
            fontSize={isTopTrack ? "md" : "sm"} 
            noOfLines={1}
          >
            {track.artists_name}
          </Text>
        </VStack>
      </CardBody>
    </Card>
  );

  // Component to display tracks for a specific time period
  const TrackTimeDisplay = ({ tracks, title }) => {
    // Ensure we have at least 10 tracks to display
    const displayTracks = tracks.slice(0, 10);
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
        </CardBody>
      </Card>
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