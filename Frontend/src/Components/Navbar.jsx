import { 
  Box, 
  Flex, 
  Text, 
  Button, 
  useColorMode, 
  IconButton,
  useColorModeValue,
  useToast
} from '@chakra-ui/react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import { useState } from 'react';

const Navbar = ({ setIsAuthenticated }) => {
  const { colorMode, toggleColorMode } = useColorMode();
  const bg = useColorModeValue('white', 'gray.800');
  const color = useColorModeValue('gray.800', 'white');
  const navigate = useNavigate();
  const toast = useToast();
  
  const handleLogout = () => {
    localStorage.removeItem('access_token');
    
    // Trigger a storage event to notify other components
    window.dispatchEvent(new Event('storage'));
    
    // Update authentication state if setIsAuthenticated was provided
    if (setIsAuthenticated) {
      setIsAuthenticated(false);
    }
    
    toast({
      title: "Logged out",
      description: "You have been successfully logged out.",
      status: "success",
      duration: 3000,
      isClosable: true,
    });
    
    // Navigate to login page
    navigate('/login');
  };

  const NavItem = ({ to, label }) => (
    <Box
      as={RouterLink}
      to={to}
      px={4}
      py={2}
      cursor="pointer"
      fontWeight="medium"
      _hover={{ color: 'green.500', textDecoration: 'none' }}
    >
      {label}
    </Box>
  );

  return (
    <Flex
      as="nav"
      align="center"
      justify="space-between"
      wrap="wrap"
      padding="1rem"
      bg={bg}
      color={color}
      position="fixed"
      width="100%"
      top={0}
      zIndex={10}
      boxShadow="md"
    >
      <Flex align="center">
        <Text
          fontSize="xl"
          fontWeight="bold"
          color="green.500"
          as={RouterLink}
          to="/"
          _hover={{ textDecoration: 'none' }}
        >
          Spotify Taste Comparison
        </Text>
      </Flex>

      <Flex align="center">
        <NavItem to="/compare" label="Compare" />
        <NavItem to="/sections" label="My Music" />
        
        <Button
          size="sm"
          ml={4}
          colorScheme="red"
          variant="outline"
          onClick={handleLogout}
        >
          Logout
        </Button>
      </Flex>
    </Flex>
  );
};

export default Navbar;