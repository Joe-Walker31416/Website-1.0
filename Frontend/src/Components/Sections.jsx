import { Flex, Tabs, Tab, TabList, TabPanel, TabPanels, AvatarGroup, Avatar, Stack, Text, Box } from '@chakra-ui/react'
import React, { useEffect, useState } from 'react'
import TabGroup from './TabGroup';
import LoginButton from './LoginButton';

const Sections = () => {
  const [data, setData] = useState([]);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Fetch data from Flask API
  const getData = async () => {
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
      } finally {
          setIsLoading(false);
      }
  };

  useEffect(() => {
      getData();
  }, []);

  return (
    <Stack >
      {error && (
        <Box bg="red.100" p={4} mb={4} borderRadius="md">
          <Text color="red.800">Error: {error}</Text>
          <Text>API may not be running. Make sure backend is started at localhost:5000</Text>
        </Box>
      )}
      
      {isLoading && <Text>Loading data...</Text>}
      
      <Flex width={'100%'} alignContent={"center"} justifyContent={"center"}>
        <AvatarGroup alignContent={"center"} justifyContent={"center"} >
          <Avatar name="Joe Walker" src="https://ui-avatars.com/api/?name=Joe+walker" size={"2xl"} />
          <Avatar name="Jane Cooper" src="https://ui-avatars.com/api/?name=Jane+Cooper" size={"2xl"} />
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
            <LoginButton/>
          </TabPanel>
          <TabPanel bg={"gray.400"}>
            <TabGroup/>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </Stack>
  )
}

export default Sections