import React, { useEffect, useState } from 'react';
import { 
  Flex,  
  Text,  
  Card, 
  CardBody, 
  SimpleGrid, 
  Box, 
  Divider,
  Image
} from '@chakra-ui/react';

const TabGroup = () => {
  const [data, setData] = useState([]);

  const getData = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch("http://localhost:5000/api/card_data", {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const result = await response.json();
      console.log("Fetched Data:", result); 
      setData(result); 
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  }

  useEffect(() => {
    getData();
  }, []);

  return (
    <Flex width={'100%'}>
      <Box p={4} width={"50%"}>
        <SimpleGrid columns={3} spacing={4}>
          {data.slice(0, 9).map((song, i) => (
            <Card key={i} width="100%" height="100%" align="center" justify="center">
              <CardBody>
                <Text fontSize="xl" fontWeight="bold">{i+1}.</Text>
                <Image src={song[2]} alt={song[0]} height="100px"  /> {/* boxSize="50px" borderRadius="full" mb={2} /> */}
                <Text fontSize="xl" fontWeight="bold">{song[0]}</Text>
                <Text fontSize="sm" color="gray.500">{song[1]}</Text>
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


{/* <Card maxW='sm'>
  <CardBody>
    <Image src='Album image link' borderRadius='lg' />
    <Stack mt='6' spacing='3'>
    <Heading size='md'>Song Name</Heading>
    <Text color='gray.400'>Artist Name</Text>
    </Stack>
  </CardBody>
</Card>  */}