import * as React from 'react'

import { Button, ChakraProvider, Flex } from '@chakra-ui/react'
import Background from './Components/Background'
import HomePage from './Components/HomePage'
import Sections from './Components/Sections'


function App() {
  return (
    <ChakraProvider>
      <Background/>
    </ChakraProvider>
  )
}
  
export default App
