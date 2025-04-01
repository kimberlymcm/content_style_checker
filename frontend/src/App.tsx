import { ChakraProvider, Container, Heading } from '@chakra-ui/react';
import { ContentAnalyzer } from './components/ContentAnalyzer';

function App() {
  return (
    <ChakraProvider>
      <Container maxW="container.xl" py={8}>
        <Heading as="h1" size="xl" textAlign="center" mb={8}>
          VA.gov Style Guide Checker
        </Heading>
        <ContentAnalyzer />
      </Container>
    </ChakraProvider>
  );
}

export default App;
