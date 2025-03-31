import { Flex, Tabs, Tab, TabList, TabPanel, TabPanels, AvatarGroup, Avatar, Stack,  Text } from '@chakra-ui/react'
import React, { useEffect,useState } from 'react'
import BarChart from "components/charts/BarChart"

const Sections = () => {
  // State to store fetched data
  const [data, setData] = useState([]);

  // Fetch data from Flask API
  const getData = async () => {
      try {
          const response = await fetch("http://localhost:5000/api/testdata");
          const result = await response.json(); // Convert response to JSON
          
          console.log("Fetched Data:", result); // Debugging: Check API response

          setData(result); // Set received data
      } catch (error) {
          console.error("Error fetching data:", error);
      }
  };

  // Fetch data on component mount
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
            <Tab>Tab 1</Tab>
            <Tab>Tab 2</Tab>
          </TabList>
          <TabPanels>
            <TabPanel>
              <Text>{JSON.stringify(data, null, 2)}</Text>
            </TabPanel>
            <TabPanel>
              <p>two!</p>
            </TabPanel>
          </TabPanels>
        </Tabs>
    </Stack>

  )
}

export default Sections