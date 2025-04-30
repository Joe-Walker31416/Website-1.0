import config from '../config';
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
  Badge,
  AspectRatio
} from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';

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
  const [activeTimeRange, setActiveTimeRange] = useState('short');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const toast = useToast();
  const navigate = useNavigate();

  // Fetch user status
  const fetchUserStatus = useCallback(async () => {
    try {
      const token = localStorage.getItem('access_token');
      
      if (!token) {
        setIsLoading(false);
        return;
      }
      
      const response = await fetch(config.API_URL + "/api/user_status", {
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

  // Fetch tracks for a specific player
  const fetchUserTracks = useCallback(async (playerId) => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        console.error("No token found in localStorage");
        return null;
      }
      
      console.log(`Fetching tracks for User ${playerId}`);
      console.log(`API URL: ${config.API_URL}/api/all_user_tracks/${playerId}`);
      console.log(`Token: ${token.substring(0, 10)}...`);
      
      // Using the fixed endpoint
      const response = await fetch(`${config.API_URL}/api/all_user_tracks/${playerId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      console.log(`Response status: ${response.status}`);
      
      if (response.ok) {
        const data = await response.json();
        console.log(`User${playerId} tracks:`, data);
        return data;
      } else {
        const errorText = await response.text();
        console.error(`Failed to fetch tracks for User${playerId}:`, response.status, errorText);
        return null;
      }
    } catch (error) {
      console.error(`Error fetching tracks for User${playerId}:`, error);
      return null;
    }
  }, []);

  // Load user data and tracks
  const loadUserData = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      // Fetch user status
      const status = await fetchUserStatus();
      if (!status) {
        setIsLoading(false);
        return;
      }
      
      // Fetch tracks for both players
      if (status.player1.saved) {
        const player1Data = await fetchUserTracks(1);
        if (player1Data) {
          setPlayer1Tracks({
            short: player1Data.short || [],
            medium: player1Data.medium || [],
            long: player1Data.long || []
          });
        }
      }
      
      if (status.player2.saved) {
        const player2Data = await fetchUserTracks(2);
        if (player2Data) {
          setPlayer2Tracks({
            short: player2Data.short || [],
            medium: player2Data.medium || [],
            long: player2Data.long || []
          });
        }
      }
    } catch (error) {
      console.error("Error loading user data:", error);
      setError("Failed to load music data: " + error.message);
    } finally {
      setIsLoading(false);
    }
  }, [fetchUserStatus, fetchUserTracks]);

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

  // Handle login for a specific player
  const handleLogin = (playerId) => {
    // Store the current URL to return to this page after login
    sessionStorage.setItem('redirectUrl', '/sections');
    
    // Redirect to the specific player login URL
    window.location.href = `${config.API_URL}/api/login/${playerId}`;
  };

  // Component to display a single track
  const TrackCard = ({ track, rank, isTopTrack = false, isPlayer2 = false }) => (
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
          // Change badge color for User2's top track to blue
          colorScheme={(rank === 1 && isPlayer2) ? "blue" : (rank === 1) ? "green" : "gray"} 
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
  const TrackTimeDisplay = ({ tracks, title, isPlayer2 = false }) => {
    // Ensure we have at least 10 tracks to display
    const displayTracks = tracks?.slice(0, 10) || [];
    
    // Pad with empty tracks if less than 10
    while (displayTracks.length < 10) {
      displayTracks.push({ name: "No track data", artists_name: "Unknown Artist", image: "" });
    }
    
    const topTrack = displayTracks[0];
    const otherTracks = displayTracks.slice(1, 10);
    
    return (
      <Box>
        <Heading size="md" mb={4} textAlign="center">{title}</Heading>
        
        {/* Top track highlighted */}
        <Box mb={6}>
          {topTrack && (
            <TrackCard 
              track={topTrack} 
              rank={1} 
              isTopTrack={true} 
              isPlayer2={isPlayer2} 
            />
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
              isPlayer2={isPlayer2}
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
              <Text color="gray.600">{isPlayer2 ? "User 2" : "User 1"}</Text>
            </VStack>
          ) : (
            <VStack spacing={3}>
              <Avatar size="xl" mb={2} />
              <Heading size="md">{isPlayer2 ? "User 2" : "User 1"}</Heading>
              <Text color="gray.600">Not logged in</Text>
              <Button 
                colorScheme={isPlayer2 ? "blue" : "green"} 
                onClick={() => handleLogin(isPlayer2 ? 2 : 1)}
                size="sm"
                mt={2}
              >
                Login with Spotify
              </Button>
            </VStack>
          )}
        </Center>
      </CardBody>
    </Card>
  );

  // Simple time range selector using buttons
  const handleTimeRangeChange = (range) => {
    setActiveTimeRange(range);
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

  // Get appropriate title based on active time range
  const getTitle = (name, range) => {
    switch(range) {
      case 'short':
        return `${name}'s Recent Favorites`;
      case 'medium':
        return `${name}'s 6-Month Favorites`;
      case 'long':
        return `${name}'s All-Time Favorites`;
      default:
        return `${name}'s Top Tracks`;
    }
  };

  // Direct display of music without tab interface
  return (
    <Flex width="100%" direction={{ base: "column", md: "row" }}>
      {/* User1 Section */}
      <Box p={4} width={{ base: "100%", md: "50%" }}>
        <UserProfileCard userData={userData.player1} />
        
        {userData.player1.saved ? (
          <Box>
            {/* Simple button selector instead of tabs */}
            <Flex mb={4} justifyContent="center">
              <Button 
                mr={2} 
                colorScheme={activeTimeRange === 'short' ? "green" : "gray"}
                onClick={() => handleTimeRangeChange('short')}
              >
                Short Term
              </Button>
              <Button 
                mr={2} 
                colorScheme={activeTimeRange === 'medium' ? "green" : "gray"}
                onClick={() => handleTimeRangeChange('medium')}
              >
                Medium Term
              </Button>
              <Button 
                colorScheme={activeTimeRange === 'long' ? "green" : "gray"}
                onClick={() => handleTimeRangeChange('long')}
              >
                Long Term
              </Button>
            </Flex>
            
            {/* Display tracks based on selected time range */}
            <Box mt={4}>
              <TrackTimeDisplay 
                tracks={player1Tracks[activeTimeRange]} 
                title={getTitle(userData.player1.name, activeTimeRange)} 
                isPlayer2={false}
              />
            </Box>
          </Box>
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
      
      {/* User2 Section */}
      <Box p={4} width={{ base: "100%", md: "50%" }}>
        <UserProfileCard userData={userData.player2} isPlayer2={true} />
        
        {userData.player2.saved ? (
          <Box>
            {/* Simple button selector instead of tabs */}
            <Flex mb={4} justifyContent="center">
              <Button 
                mr={2} 
                colorScheme={activeTimeRange === 'short' ? "blue" : "gray"}
                onClick={() => handleTimeRangeChange('short')}
              >
                Short Term
              </Button>
              <Button 
                mr={2} 
                colorScheme={activeTimeRange === 'medium' ? "blue" : "gray"}
                onClick={() => handleTimeRangeChange('medium')}
              >
                Medium Term
              </Button>
              <Button 
                colorScheme={activeTimeRange === 'long' ? "blue" : "gray"}
                onClick={() => handleTimeRangeChange('long')}
              >
                Long Term
              </Button>
            </Flex>
            
            {/* Display tracks based on selected time range */}
            <Box mt={4}>
              <TrackTimeDisplay 
                tracks={player2Tracks[activeTimeRange]} 
                title={getTitle(userData.player2.name, activeTimeRange)} 
                isPlayer2={true}
              />
            </Box>
          </Box>
        ) : (
          <Center p={8} borderWidth="1px" borderRadius="lg" bg="gray.50">
            <Text>Login User 2 to view their top tracks</Text>
          </Center>
        )}
      </Box>
    </Flex>
  );
};

export default TabGroup;