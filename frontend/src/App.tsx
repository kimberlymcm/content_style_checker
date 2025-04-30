import { ChakraProvider, Container, Heading } from "@chakra-ui/react";
import { ContentAnalyzer } from "./components/ContentAnalyzer";

function App() {
  return (
    <ChakraProvider data-oid="_ulpfzq">
      <Container maxW="container.xl" py={8} data-oid="pt5-nwy">
        <Heading
          as="h1"
          size="xl"
          textAlign="center"
          mb={10}
          data-oid="xv43yk_"
          bgGradient="linear(to-r, teal.500, blue.500)"
          bgClip="text"
          fontWeight="extrabold"
          letterSpacing="tight"
          p={2}
          className="shadow-sm rounded-lg"
        >
          VA.gov Style Guide Checker
        </Heading>
        <ContentAnalyzer data-oid="i2.2t_b" />
      </Container>
    </ChakraProvider>
  );
}

export default App;
