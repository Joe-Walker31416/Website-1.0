import { Button, useToast } from '@chakra-ui/react';
import React from 'react';

const LoginButton = () => {
    const toast = useToast();

    const handleLogin = () => {
        // Store the current URL in sessionStorage to redirect back after login
        sessionStorage.setItem('redirectUrl', window.location.pathname);
        
        // Check if we need to clear any previous errors
        const hasError = localStorage.getItem('auth_error');
        if (hasError) {
            localStorage.removeItem('auth_error');
        }
        
        // Redirect to the backend login endpoint
        window.location.href = 'http://localhost:5000/login';
    };

    return (
        <Button 
            onClick={handleLogin} 
            colorScheme="green" 
            size="lg"
            _hover={{ transform: 'translateY(-2px)', boxShadow: 'lg' }}
            _active={{ transform: 'translateY(0)', boxShadow: 'md' }}
            transition="all 0.2s"
        >
            Login with Spotify
        </Button>
    );
};

export default LoginButton;