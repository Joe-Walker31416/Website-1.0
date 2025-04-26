// LoginPage.jsx
import { Box, Button, Text, VStack } from '@chakra-ui/react';

const LoginPage = () => {
  const handleLogin = () => {
    window.location.href = 'http://localhost:5000/login';
  };

  return (
    <Box h="100vh" bg="gray.900" color="white" display="flex" justifyContent="center" alignItems="center">
      <VStack spacing={4}>
        <Text fontSize="2xl">Welcome to My Spotify App</Text>
        <Button colorScheme="green" size="lg" onClick={handleLogin}>
          Login with Spotify
        </Button>
      </VStack>
    </Box>
  );
};

export default LoginPage;