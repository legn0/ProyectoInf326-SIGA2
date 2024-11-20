import React, { useState } from "react";
import {
  Box,
  Button,
  Heading,
  Flex,
  HStack,
  FormLabel,
  NumberInput,
  NumberInputField,
  FormControl,
} from "@chakra-ui/react";
import { useMutation } from "@tanstack/react-query";
import { startEnrollmentRound } from "../api/enrollment";

const EnrollmentAdministrativo = () => {
  const [paraleloID, setParaleloID] = useState();
  const [cursoID, setCursoID] = useState();

  const handleParaleloIDChange = (e) => {
    setParaleloID(e.target.value);
  };

  const handleCursoIDChange = (e) => {
    setCursoID(e.target.value);
  };

  const iniciarRonda = useMutation({
    mutationFn: startEnrollmentRound,
    onError: () => console.log("No pude iniciar la ronda"), //asdasd
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    iniciarRonda.mutate(cursoID, paraleloID);
  };

  return (
    <Box bg="gray.100" minHeight="100vh" p={4}>
      <Heading pt={5} mb={8} color="gray.800" textAlign="center">
        Control Administrativo
      </Heading>

      <Flex
        direction="column"
        justifyContent="center"
        alignItems="center"
        minHeight="70vh">
        <Box
          p={6}
          bg="white"
          shadow="md"
          borderRadius="md"
          mx={4}
          textAlign="center"
          width="40%">
          <Heading mb={4} color="gray.800" size="md">
            Acciones Adicionales
          </Heading>
          <HStack spacing={4} justify="center">
            <Flex direction={"column"}>
              <FormControl>
                <FormLabel>ID de curso:</FormLabel>
                <NumberInput>
                  <NumberInputField onChange={handleCursoIDChange} />
                </NumberInput>
              </FormControl>
              <FormControl>
                <FormLabel>ID de paralelo:</FormLabel>
                <NumberInput>
                  <NumberInputField onChange={handleParaleloIDChange} />
                </NumberInput>
              </FormControl>
              <Button
                variant="outline"
                color="gray.800"
                _hover={{ backgroundColor: "orange.300", color: "white" }}
                onClick={handleSubmit}>
                Iniciar Ronda de Inscripción
              </Button>
            </Flex>
          </HStack>
        </Box>
      </Flex>
    </Box>
  );
};

export default EnrollmentAdministrativo;
