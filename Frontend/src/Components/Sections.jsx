import { Flex, Tabs, Tab, TabList, TabPanel, TabPanels, AvatarGroup, Avatar, Stack,  Text,  Card, CardHeader, CardBody, CardFooter, Image, Heading } from '@chakra-ui/react'
import React, { useEffect,useState } from 'react'
import TabGroup from './TabGroup';


const Sections = () => {
  // State to store fetched data
  const [data, setData] = useState([]);

  // Fetch data from Flask API
  const getData = async () => {
      try {
          const response = await fetch("http://localhost:5000/api/testdata");
          const result = await response.json();
          console.log("Fetched Data:", result); 
          setData(result); 
      } catch (error) {
          console.error("Error fetching data:", error);
      }
  };
  useEffect(() => {
      getData();
  }, []);
  return (
  <Stack >
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
              {/* <Text>{JSON.stringify(data, null, 2)}</Text> */}
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