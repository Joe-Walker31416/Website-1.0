import { Button } from '@chakra-ui/react';
import React from 'react'

const LoginButton = () => {
    const handleLogin = () => {
        window.location.href = 'http://localhost:3000/login';
    }

  return (
    <Button onClick={handleLogin}>
        Log-in with Spotify
    </Button>
  )
}

export default LoginButton