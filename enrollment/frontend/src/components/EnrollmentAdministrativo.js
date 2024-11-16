import React from "react";
import { Box, Button, VStack, Heading, Flex, HStack } from "@chakra-ui/react";

const EnrollmentAdministrativo = ({ isAlumnosEnabled, setIsAlumnosEnabled }) => {
  const handleInitRound = () => {
    fetch("")
      .catch((error) => console.error("Error en la llamada a la API:", error));
  };

  return (
    <Box bg="gray.100" minHeight="100vh" p={4}>
      <Heading pt={5} mb={8} color="gray.800" textAlign="center">
        Control Administrativo
      </Heading>

      <Flex direction="column" justifyContent="center" alignItems="center" minHeight="70vh">
        <Box p={6} width="40%" bg="white" shadow="md" mb={20} borderRadius="md" mx={4} textAlign="center" >
          <Heading mb={4} color="gray.800" size="md">
            Control de Inscripción
          </Heading>
          <HStack spacing={4} justify="center">
            <Button variant="outline" color="gray.800" _hover={{ backgroundColor: "green.300", color: "white" }} onClick={() => setIsAlumnosEnabled(true)}>
              Habilitar Inscripción
            </Button>
            <Button variant="outline" color="gray.800" _hover={{ backgroundColor: "red.300", color: "white" }} onClick={() => setIsAlumnosEnabled(false)}>
              Deshabilitar Inscripción
            </Button>
          </HStack>
        </Box>
        <Box p={6} bg="white" shadow="md" borderRadius="md" mx={4} textAlign="center" width="40%">
          <Heading mb={4} color="gray.800" size="md">
            Acciones Adicionales
          </Heading>
          <HStack spacing={4} justify="center">
            <Button variant="outline" color="gray.800" _hover={{ backgroundColor: "orange.300", color: "white" }} onClick={handleInitRound}>
              Iniciar Ronda de Inscripción
            </Button>
          </HStack>
        </Box>
      </Flex>
    </Box>
  );
};

export default EnrollmentAdministrativo;