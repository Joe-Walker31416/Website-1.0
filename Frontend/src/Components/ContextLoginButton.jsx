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
        // Determine the redirect path based on context
        let returnPath;
        
        if (redirectPath && redirectPath.length > 0) {
            // If explicitly provided, use that
            returnPath = redirectPath;
        } else {
            // Extract the current path without the leading slash
            const currentPath = location.pathname;
            const cleanPath = currentPath.startsWith('/') ? currentPath.substring(1) : currentPath;
            
            // Use the current path if it's one of our main pages, or default to 'compare'
            if (cleanPath === 'sections' || cleanPath === 'compare') {
                returnPath = cleanPath;
            } else {
                returnPath = 'compare'; // Default fallback
            }
        }
        
        // Log for debugging
        console.log(`Logging in player ${playerId} with redirect to: ${returnPath}`);
        
        // Store the path for potential use after login
        sessionStorage.setItem('redirect_page', returnPath);
        
        // Redirect to the backend login endpoint with the player ID and redirect path
        window.location.href = `${config.API_URL}/api/login/${playerId}?redirect=${returnPath}`;
    };

    return (
        <Button 
            onClick={handleLogin} 
            colorScheme={colorScheme}
            size={typeof sizeProps === 'object' ? undefined : sizeProps}
            {...(typeof sizeProps === 'object' ? sizeProps : {})}
            _hover={{ transform: 'translateY(-2px)', boxShadow: 'lg' }}
            _active={{ transform: 'translateY(0)', boxShadow: 'md' }}
            transition="all 0.2s"
            {...props}
        >
            {playerId === 2 ? "Login User 2 with Spotify" : "Login with Spotify"}
        </Button>
    );
};

export default ContextLoginButton;