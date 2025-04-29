import {Box, Flex} from '@chakra-ui/react'
import React from 'react'
import Sections from './Sections';
import config from '../config';

const Background = () => {
  
  return (
    <Flex justifyContent="center" alignItems="center" height="100vh">
      <Box p={4} height={'100%'} width={'75%'} boxShadow="lg" borderRadius="lg" bg="white" textAlign="center" fontSize="xl" fontWeight="bold" borderWidth={"3px"} position="relative">
        <Sections />
      </Box>
    </Flex>
  );
}

export default Background