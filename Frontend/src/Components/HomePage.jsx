import { Button, Flex, Link } from '@chakra-ui/react'
import React from 'react'

const HomePage = () => {
  return (
    <Flex justifyContent="center" alignItems="center" height="100vh">
      <Link href='/login' >Home Page</Link>
      </Flex>
  )
}

export default HomePage