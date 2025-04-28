import { Box, Flex, Text, Button, useColorMode, IconButton, useColorModeValue } from '@chakra-ui/react';
import { useState } from 'react';

const Navbar = ({ setCurrentPage, currentPage }) => {
  const { colorMode, toggleColorMode } = useColorMode();
  const bg = useColorModeValue('white', 'gray.800');
  const color = useColorModeValue('gray.800', 'white');
  
  const handleLogout = () => {
    localStorage.removeItem('access_token');
    window.location.reload();
  };

  const NavItem = ({ page, label }) => (
    <Box
      px={4}
      py={2}
      cursor="pointer"
      fontWeight={currentPage === page ? "bold" : "normal"}
      borderBottom={currentPage === page ? "2px solid" : "none"}
      borderColor="green.500"
      onClick={() => setCurrentPage(page)}
      _hover={{ color: 'green.500' }}
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
        >
          Spotify Taste Comparison
        </Text>
      </Flex>

      <Flex align="center">
        <NavItem page="compare" label="Compare" />
        
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