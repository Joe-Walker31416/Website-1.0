import config from '../config';
import { Button, useToast } from '@chakra-ui/react';
import React from 'react';
import { useLocation } from 'react-router-dom';

const sizeMap = {
    sm: "sm",
    md: "md",
    lg: "lg",
    xl: { fontSize: "xl", px: 8, py: 6 },
};

const ContextLoginButton = ({
    size = "md",
    playerId = 1,
    colorScheme = "green",
    redirectPath = "",
    ...props
}) => {
    const sizeProps = sizeMap[size] || sizeMap["md"];
    const toast = useToast();
    const location = useLocation();
    
    const handleLogin = () => {
        // Determine redirect path - use provided path, current path, or default to 'compare'
        const returnPath = redirectPath || location.pathname.replace('/', '') || 'compare';
        
        // Store the path to return to after login
        sessionStorage.setItem('redirect_page', returnPath);
        
        // Clear any previous errors
        const hasError = localStorage.getItem('auth_error');
        if (hasError) {
            localStorage.removeItem('auth_error');
        }
        
        // Log for debugging
        console.log(`Logging in player ${playerId} with redirect to: ${returnPath}`);
        
        // Redirect to the backend login endpoint with the player ID
        window.location.href = `${config.API_URL}/api/login/${playerId}?redirect=${returnPath}`;
    };

    return (
        <Button 
            onClick={handleLogin} 
            colorScheme={colorScheme}
            size={sizeProps}
            _hover={{ transform: 'translateY(-2px)', boxShadow: 'lg' }}
            _active={{ transform: 'translateY(0)', boxShadow: 'md' }}
            transition="all 0.2s"
            {...props}
        >
            {playerId === 2 ? "Login with Spotify" : "Login with Spotify"}
        </Button>
    );
};

export default ContextLoginButton;