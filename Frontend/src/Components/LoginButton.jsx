import config from '../config';
import { Button, useToast } from '@chakra-ui/react';
import React from 'react';


const sizeMap = {
    sm: "sm",
    md: "md",
    lg: "lg",
    xl: { fontSize: "xl", px: 8, py: 6 }, // custom size example
  };

const LoginButton = ({size = "md", ...props}) => {
    const sizeProps = sizeMap[size] || sizeMap["md"];
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
        window.location.href = config.API_URL +'/login';
    };

    return (
        <Button 
            onClick={handleLogin} 
            colorScheme="green" 
            size={sizeProps}
            _hover={{ transform: 'translateY(-2px)', boxShadow: 'lg' }}
            _active={{ transform: 'translateY(0)', boxShadow: 'md' }}
            transition="all 0.2s"
        >
            Login with Spotify
        </Button>
    );
};

export default LoginButton;