import React from "react";
import { Box, Text } from "@chakra-ui/react";

const Horario = ({ horario }) => {
    return (
        <Box mt={5} p={4} borderWidth={1} borderRadius="md" shadow="sm">
            <Text fontSize="xl" fontWeight="bold" mb={3}>
                Horario del ramo
            </Text>
            {horario.length > 0 ? (
                horario.map((h, index) => (
                    <Text key={index} fontSize="md">
                        {h.dia}: {h.bloque}
                    </Text>
                ))
            ) : (
                <Text fontSize="md" color="gray.600">
                    No hay horario disponible.
                </Text>
            )}
        </Box>
    );
};

export default Horario;
