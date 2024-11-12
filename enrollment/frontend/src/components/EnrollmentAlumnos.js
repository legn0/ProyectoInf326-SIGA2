import React, { useState } from "react";
import { Box, Heading, HStack, Text, Button, Stack, StackSeparator } from "@chakra-ui/react";
import { MenuContent, MenuItem, MenuRoot, MenuTrigger } from "../components/ui/menu";
import Horario from "./Horario";

const EnrollmentAlumnos = () => {
    // Datos ficticios de los ramos
    const [ramos, setRamos] = useState([
        { id: 1, nombre: "Matemáticas", codigo: "MAT101", creditos: 5, inscritos: "12/30", paralelos: [{ id: 1, numero: 200 }, { id: 2, numero: 201 }] },
        { id: 2, nombre: "Física", codigo: "FIS102", creditos: 4, inscritos: "29/30", paralelos: [{ id: 3, numero: 201 }, { id: 4, numero: 204 }] },
        { id: 3, nombre: "Química", codigo: "QUI103", creditos: 6, inscritos: "15/15", paralelos: [{ id: 5, numero: 200 }, { id: 6, numero: 201 }] },
        { id: 4, nombre: "Biología", codigo: "BIO104", creditos: 3, inscritos: "40/40", paralelos: [{ id: 7, numero: 202 }, { id: 8, numero: 207 }] },
        { id: 5, nombre: "Historia", codigo: "HIS105", creditos: 4, inscritos: "23/35", paralelos: [{ id: 9, numero: 200 }, { id: 10, numero: 201 }] },
    ]);

    const [HorariosRamo, setHorariosRamo] = useState({});
    const [selectedParallels, setSelectedParallels] = useState([
        {cursoId: 1, paraleloId: 1},
        {cursoId: 2, paraleloId: 3},
        {cursoId: 3, paraleloId: 5},
        {cursoId: 4, paraleloId: 7},
        {cursoId: 5, paraleloId: 9}
    ]);

    const [Horariosdb, setHorariosdb] = useState([
        { curso_id: 1, paralelo_id: 1, numero: 200, horario: [{ dia: "Lunes", bloque: "3-4" }, { dia: "Miércoles", bloque: "3-4" }] },
        { curso_id: 1, paralelo_id: 2, numero: 201, horario: [{ dia: "Martes", bloque: "1-2" }, { dia: "Jueves", bloque: "5-6" }] },
        { curso_id: 2, paralelo_id: 3, numero: 201, horario: [{ dia: "Lunes", bloque: "7-8" }, { dia: "Miércoles", bloque: "7-8" }] },
        { curso_id: 2, paralelo_id: 4, numero: 204, horario: [{ dia: "Martes", bloque: "9-10" }, { dia: "Jueves", bloque: "9-10" }] },
        { curso_id: 3, paralelo_id: 5, numero: 200, horario: [{ dia: "Lunes", bloque: "1-2" }, { dia: "Miércoles", bloque: "1-2" }] },
        { curso_id: 3, paralelo_id: 6, numero: 201, horario: [{ dia: "Martes", bloque: "3-4" }, { dia: "Jueves", bloque: "3-4" }] },
        { curso_id: 4, paralelo_id: 7, numero: 202, horario: [{ dia: "Lunes", bloque: "3-4" }, { dia: "Miércoles", bloque: "3-4" }] },
        { curso_id: 4, paralelo_id: 8, numero: 207, horario: [{ dia: "Martes", bloque: "7-8" }, { dia: "Jueves", bloque: "7-8" }] },
        { curso_id: 5, paralelo_id: 9, numero: 200, horario: [{ dia: "Lunes", bloque: "9-10" }, { dia: "Miércoles", bloque: "9-10" }] },
        { curso_id: 5, paralelo_id: 10, numero: 201, horario: [{ dia: "Martes", bloque: "11-12" }, { dia: "Jueves", bloque: "11-12" }] },
    ]);

    const handleSelectParallel = (cursoId, newParaleloId) => {
        setSelectedParallels((prev) => 
            prev.map((item) => 
                item.cursoId === cursoId ? { ...item, paraleloId: newParaleloId } : item
            )
        );
    };
    

    const handleInscribir = (ramoId) => {
        setRamos((prevRamos) =>
            prevRamos.map((ramo) =>
                ramo.id === ramoId
                    ? { ...ramo, inscritos: (parseInt(ramo.inscritos.split('/')[0]) + 1) + '/30' } // Ejemplo de actualización de inscritos
                    : ramo
            )
        );
    };

    const handleHorario = (cursoId) => {
        const view_parallel = selectedParallels.filter((h) => h.cursoId === cursoId)
        const horario = Horariosdb.filter((h) => h.curso_id === cursoId && h.paralelo_id === view_parallel[0].paraleloId);
        console.log(view_parallel[0].paraleloId, horario)
        setHorariosRamo(horario);
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
                                        <MenuItem key={paralelo.id} value={paralelo.numero} onClick={() => handleSelectParallel(ramo.id, paralelo.id)}>
                                            {paralelo.numero}
                                        </MenuItem>
                                    ))}
                                </MenuContent>
                            </MenuRoot>

                            {/* Botones para ver horario e inscribirse */}
                            <Button colorScheme="blue" onClick={() => handleHorario(ramo.id)}>
                                Ver Horario
                            </Button>
                            <Button colorScheme="blue" onClick={() => handleInscribir(ramo.id)}>
                                Inscribirse
                            </Button>
                        </HStack>
                    </Box>
                ))}
            </Stack>

            {HorariosRamo && HorariosRamo.length > 0 && (
                <Box mt={10}>
                    <Heading size="md" mb={3}>
                        Horarios Seleccionados
                    </Heading>
                    {HorariosRamo.map((horario) => (
                        <Horario key={horario.paralelo_id} horario={horario.horario} />
                    ))}
                </Box>
            )}
        </Box>
    );
};

export default EnrollmentAlumnos;