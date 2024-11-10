import React, { useState } from "react";
import { Box, Heading, HStack, Text, Button, Stack, StackSeparator } from "@chakra-ui/react";
import { MenuContent, MenuItem, MenuRoot, MenuTrigger } from "../components/ui/menu";

const EnrollmentAlumnos = () => {
    // Datos ficticios de los ramos
    const [ramos, setRamos] = useState([
        { id: 1, nombre: "Matemáticas", codigo: "MAT101", creditos: 5, inscritos: "12/30", paralelos: [200, 201, 202, 203, 204, 205, 206, 207, 208] },
        { id: 2, nombre: "Física", codigo: "FIS102", creditos: 4, inscritos: "29/30", paralelos: [200, 201, 203, 204, 205] },
        { id: 3, nombre: "Química", codigo: "QUI103", creditos: 6, inscritos: "15/15", paralelos: [200, 201, 202, 203] },
        { id: 4, nombre: "Biología", codigo: "BIO104", creditos: 3, inscritos: "40/40", paralelos: [200, 201] },
        { id: 5, nombre: "Historia", codigo: "HIS105", creditos: 4, inscritos: "23/35", paralelos: [200, 201, 202] },
    ]);

    const handleInscribir = (ramoId) => {
        setRamos((prevRamos) =>
            prevRamos.map((ramo) =>
                ramo.id === ramoId
                    ? { ...ramo, inscritos: (parseInt(ramo.inscritos.split('/')[0]) + 1) + '/30' } // Ejemplo de actualización de inscritos
                    : ramo
            )
        );
    };

    const handleHorario = () => {
        // Aquí puedes agregar la lógica para mostrar el horario si es necesario
    };

    return (
        <Box p={5}>
            <Heading mb={5}>Inscripción de Ramos</Heading>
            <Stack separator={<StackSeparator />} align="stretch" spacing={4} borderWidth={3} borderRadius="md" p={4} shadow="md">
                {ramos.map((ramo) => (
                    <Box key={ramo.id}>
                        <HStack spacing={6} justify="space-between" align="center">
                            {/* Información de cada ramo */}
                            <Text flex={1} fontSize="xl" fontWeight="bold">
                                {ramo.codigo}
                            </Text>
                            <Text flex={1} fontSize="md" color="gray.600">
                                Inscritos: {ramo.inscritos}
                            </Text>
                            <Text flex={1} fontSize="md" color="gray.500">
                                Créditos: {ramo.creditos}
                            </Text>

                            {/* Menú para seleccionar el paralelo */}
                            <MenuRoot>
                                <MenuTrigger asChild>
                                    <Button variant="outline" size="sm">
                                        Seleccionar Paralelo
                                    </Button>
                                </MenuTrigger>
                                <MenuContent>
                                    {ramo.paralelos.map((paralelo) => (
                                        <MenuItem key={paralelo} value={paralelo}>
                                            {paralelo}
                                        </MenuItem>
                                    ))}
                                </MenuContent>
                            </MenuRoot>

                            {/* Botones para ver horario e inscribirse */}
                            <Button colorScheme="blue" onClick={() => handleHorario()}>
                                Ver Horario
                            </Button>
                            <Button colorScheme="blue" onClick={() => handleInscribir(ramo.id)}>
                                Inscribirse
                            </Button>
                        </HStack>
                    </Box>
                ))}
            </Stack>
        </Box>
    );
};

export default EnrollmentAlumnos;