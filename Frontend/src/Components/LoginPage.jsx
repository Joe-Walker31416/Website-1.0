// LoginPage.jsx
import config from '../config';
import { Box, Button, Text, VStack, Heading } from '@chakra-ui/react';

const LoginPage = () => {
  const handleLogin = () => {
    window.location.href = config.API_URL + '/login';
  };

  return (
    <Box 
      h="100vh" 
      bg="gray.900" 
      color="white" 
      display="flex" 
      justifyContent="center" 
      alignItems="center"
    >
      <VStack spacing={6} p={8} bg="gray.800" borderRadius="lg" boxShadow="xl">
        <Heading>Welcome to Spotify Comparison!</Heading>
        <Text fontSize="lg">Compare your music taste with friends</Text>
        <Button 
          colorScheme="green" 
          size="lg" 
          onClick={handleLogin}
          _hover={{ bg: "green.500" }}
        >
          Login with Spotify
        </Button>
      </VStack>
    </Box>
  );
};

export default LoginPage;