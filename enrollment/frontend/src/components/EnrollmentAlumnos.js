import React, { useState } from "react";
import { Box, Heading, HStack, Text, Button, Stack, StackSeparator } from "@chakra-ui/react";
import { MenuContent, MenuItem, MenuRoot, MenuTrigger } from "../components/ui/menu";
import Horario from "./Horario";

const EnrollmentAlumnos = () => {
    // Datos ficticios de los ramos
    const [ramos, setRamos] = useState([
        { id: 1, nombre: "Matemáticas", codigo: "MAT101", creditos: 5, inscritos: "12/30", estado: "Pendiente", paralelos: [{ id: 1, numero: 200 }, { id: 2, numero: 201 }] },
        { id: 2, nombre: "Física", codigo: "FIS102", creditos: 4, inscritos: "29/30", estado: "Inscrita", paralelos: [{ id: 3, numero: 201 }, { id: 4, numero: 204 }] },
        { id: 3, nombre: "Química", codigo: "QUI103", creditos: 6, inscritos: "15/15", estado: "Pendiente", paralelos: [{ id: 5, numero: 200 }, { id: 6, numero: 201 }] },
        { id: 4, nombre: "Biología", codigo: "BIO104", creditos: 3, inscritos: "40/40", estado: "Inscrita", paralelos: [{ id: 7, numero: 202 }, { id: 8, numero: 207 }] },
        { id: 5, nombre: "Historia", codigo: "HIS105", creditos: 4, inscritos: "23/35", estado: "Pendiente",paralelos: [{ id: 9, numero: 200 }, { id: 10, numero: 201 }] },
        { id: 6, nombre: "Programacion", codigo: "PRO115", creditos: 5, inscritos: "29/35", estado: "Pendiente",paralelos: [{ id: 11, numero: 200 }, { id: 12, numero: 201 }] },
        { id: 7, nombre: "Deporte", codigo: "DEP165", creditos: 2, inscritos: "34/35", estado: "Pendiente",paralelos: [{ id: 13, numero: 200 }, { id: 14, numero: 201 }] },
    ]);

    const [ramosInscritos, setRamosInscritos] = useState([
        { id: 8, nombre: "Matemáticas", codigo: "MAT102", creditos: 5, inscritos: "12/30", estado: "Pendiente", paralelos: [{ id: 15, numero: 200 }, { id: 16, numero: 201 }] },
        { id: 9, nombre: "Física", codigo: "FIS103", creditos: 4, inscritos: "29/30", estado: "Inscrita", paralelos: [{ id: 17, numero: 201 }, { id: 18, numero: 204 }] },
        { id: 10, nombre: "Química", codigo: "QUI104", creditos: 6, inscritos: "15/15", estado: "Pendiente", paralelos: [{ id: 19, numero: 200 }, { id: 20, numero: 201 }] },
        { id: 11, nombre: "Deporte", codigo: "DEP109", creditos: 2, inscritos: "15/15", estado: "Pendiente", paralelos: [{ id: 21, numero: 200 }, { id: 22, numero: 201 }] },
        { id: 12, nombre: "Programacion", codigo: "PRO119", creditos: 5, inscritos: "38/40", estado: "Inscrita", paralelos: [{ id: 23, numero: 200 }, { id: 24, numero: 201 }] },
    ]);

    const [HorariosRamo, setHorariosRamo] = useState(null);

    const [selectedParallels, setSelectedParallels] = useState([
        {cursoId: 1, paraleloId: 1},
        {cursoId: 2, paraleloId: 3},
        {cursoId: 3, paraleloId: 5},
        {cursoId: 4, paraleloId: 7},    
        {cursoId: 5, paraleloId: 9},
        {cursoId: 6, paraleloId: 11},
        {cursoId: 7, paraleloId: 13},
    ]);

    const [selectedParallelsInscrito, setSelectedParallelsInscrito] = useState([
        {cursoId: 8, paraleloId: 15},
        {cursoId: 9, paraleloId: 17},
        {cursoId: 10, paraleloId: 19},
        {cursoId: 11, paraleloId: 21},
        {cursoId: 12, paraleloId: 23}
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
        { curso_id: 6, paralelo_id: 11, numero: 200, horario: [{ dia: "Martes", bloque: "11-12" }, { dia: "Jueves", bloque: "11-12" }] },
        { curso_id: 6, paralelo_id: 12, numero: 201, horario: [{ dia: "Martes", bloque: "11-12" }, { dia: "Jueves", bloque: "11-12" }] },
        { curso_id: 7, paralelo_id: 13, numero: 200, horario: [{ dia: "Martes", bloque: "11-12" }, { dia: "Jueves", bloque: "11-12" }] },
        { curso_id: 7, paralelo_id: 14, numero: 201, horario: [{ dia: "Martes", bloque: "11-12" }, { dia: "Jueves", bloque: "11-12" }] },
        { curso_id: 8, paralelo_id: 15, numero: 200, horario: [{ dia: "Martes", bloque: "11-12" }, { dia: "Jueves", bloque: "11-12" }] },
        { curso_id: 8, paralelo_id: 16, numero: 201, horario: [{ dia: "Lunes", bloque: "11-12" }, { dia: "Jueves", bloque: "11-12" }] },
        { curso_id: 9, paralelo_id: 17, numero: 201, horario: [{ dia: "Miercoles", bloque: "11-12" }, { dia: "Viernes", bloque: "11-12" }] },
        { curso_id: 9, paralelo_id: 18, numero: 204, horario: [{ dia: "Martes", bloque: "11-12" }, { dia: "Jueves", bloque: "11-12" }] },
        { curso_id: 10, paralelo_id: 19, numero: 200, horario: [{ dia: "Lunes", bloque: "11-12" }, { dia: "Jueves", bloque: "9-10" }] },
        { curso_id: 10, paralelo_id: 20, numero: 201, horario: [{ dia: "Martes", bloque: "11-12" }, { dia: "Jueves", bloque: "11-12" }] },
        { curso_id: 11, paralelo_id: 21, numero: 200, horario: [{ dia: "Martes", bloque: "11-12" }, { dia: "Jueves", bloque: "11-12" }] },
        { curso_id: 11, paralelo_id: 22, numero: 201, horario: [{ dia: "Martes", bloque: "11-12" }, { dia: "Jueves", bloque: "11-12" }] },
        { curso_id: 12, paralelo_id: 23, numero: 200, horario: [{ dia: "Martes", bloque: "11-12" }, { dia: "Jueves", bloque: "11-12" }] },
        { curso_id: 12, paralelo_id: 24, numero: 201, horario: [{ dia: "Martes", bloque: "11-12" }, { dia: "Jueves", bloque: "11-12" }] },
    ]);

    const handleSelectParallel = (cursoId, newParaleloId) => {
        setSelectedParallels((prev) => 
            prev.map((item) => 
                item.cursoId === cursoId ? { ...item, paraleloId: newParaleloId } : item
            )
        );
    };

    const handleSelectParallelInscrito = (cursoId, newParaleloId) => {
        setSelectedParallelsInscrito((prev) => 
            prev.map((item) => 
                item.cursoId === cursoId ? { ...item, paraleloId: newParaleloId } : item
            )
        );
    };

    const handleEliminar = (cursoId) => {
        setSelectedParallelsInscrito((prev) => prev.filter((item) => item.cursoId !== cursoId));
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
        const ramo = ramos.filter((h) => h.id === cursoId)

        setHorariosRamo({codigo: ramo[0].codigo, ...horario[0]});
    };

    return (
        <Box>
            <Heading color="gray.800" textAlign="center">Inscripción de Ramos</Heading>
            <HStack spacing={4} align="start">
                {/* Sección de ramos */}
                <Box p={5} bg="white" width="60%">
                <Heading size="md" color="gray.800" mb={4}>Ramos para Inscribir</Heading>
                    <Stack separator={<StackSeparator />} align="stretch" spacing={4} borderWidth={3} borderRadius="md" p={4} shadow="md" maxHeight="40vh" overflowY="auto">
                        {ramos.map((ramo) => (
                            <Box key={ramo.id}>
                                <HStack spacing={4} justify="space-between" align="center">
                                    <Text flex={1} fontSize="md" fontWeight="bold" color="gray.800">
                                        {ramo.codigo}
                                    </Text>
                                    <Text flex={1} fontSize="md" color="gray.700">
                                        Créditos: {ramo.creditos}
                                    </Text>
                                    <Text flex={1} fontSize="md" color="gray.700">
                                        Inscritos: {ramo.inscritos}
                                    </Text>
                                    <MenuRoot>
                                        <MenuTrigger asChild>
                                            <Button variant="outline" color="gray.800" backgroundColor="whiteAlpha.300" _hover={{ backgroundColor: "orange.300", color: "white" }}>
                                            Paralelo: {
                                                selectedParallels.find((item) => item.cursoId === ramo.id)?.paraleloId
                                                ? ramo.paralelos.find((p) => p.id === selectedParallels.find((item) => item.cursoId === ramo.id)?.paraleloId)?.numero
                                                : "Seleccionar"
                                            }
                                            </Button>
                                        </MenuTrigger>
                                        <MenuContent backgroundColor="gray.100" borderRadius="md" boxShadow="md">
                                            {ramo.paralelos.map((paralelo) => (
                                                <MenuItem key={paralelo.id} value={paralelo.numero} color="gray.800" backgroundColor="gray.100" _hover={{ backgroundColor: "orange.300", color: "white" }} onClick={() => handleSelectParallel(ramo.id, paralelo.id)}>
                                                    {paralelo.numero}
                                                </MenuItem>
                                            ))}
                                        </MenuContent>
                                    </MenuRoot>
                                    <Button variant="outline" color="gray.800" _hover={{ backgroundColor: "orange.300", color: "white" }} onClick={() => handleHorario(ramo.id)}>
                                        Ver Horario
                                    </Button>
                                    <Button variant="outline" color="gray.800" _hover={{ backgroundColor: "green.300", color: "white" }} onClick={() => handleInscribir(ramo.id)}>
                                        Inscribirse 
                                    </Button>
                                </HStack>
                            </Box>
                        ))}
                    </Stack>
                </Box>

                {/* Sección de horario */}
                <Box p={5} width="40%">
                <Heading size="md" color="gray.800" mb={4}>Horario</Heading>
                    {HorariosRamo && (
                        <Box>
                            <Horario horario={HorariosRamo} />
                        </Box>
                    )}
                </Box>
            </HStack>

            {/* Sección de ramos inscritos */}
            <Box mt={8} p={5} bg="white" width="100%">
                <Heading size="md" color="gray.800" mb={4}>Ramos Inscritos</Heading>
                <Stack separator={<StackSeparator />} align="stretch" spacing={4} borderWidth={3} borderRadius="md" p={4} shadow="md" maxHeight="35vh" overflowY="auto">
                    {selectedParallelsInscrito.map((inscrito) => {
                        const ramo = ramosInscritos.find((ramo) => ramo.id === inscrito.cursoId);
                        return (
                            <Box key={inscrito.cursoId}>
                                <HStack spacing={4} justify="space-between" align="center">
                                    <Text flex={1} fontSize="md" fontWeight="bold" color="gray.800">
                                        {ramo.codigo}
                                    </Text>
                                    <Text flex={1} fontSize="md" color="gray.700">
                                        Créditos: {ramo.creditos}
                                    </Text>
                                    <Text flex={1} fontSize="md" color="gray.700">
                                        Inscritos: {ramo.inscritos}
                                    </Text>
                                    <Text flex={1} fontSize="md" color="gray.700">
                                        Estado: {ramo.estado}
                                    </Text>
                                    <Button variant="outline" color="gray.800" _hover={{ backgroundColor: "orange.300", color: "white" }} onClick={() => handleSelectParallelInscrito(inscrito.cursoId, inscrito.paraleloId)}>
                                        Cambiar Paralelo
                                    </Button>
                                    <Button variant="outline" color="gray.800" _hover={{ backgroundColor: "red.300", color: "white" }} onClick={() => handleEliminar(inscrito.cursoId)}>
                                        Eliminar Inscripción
                                    </Button>
                                </HStack>
                            </Box>
                        );
                    })}
                </Stack>
            </Box>
        </Box>
    );
};

export default EnrollmentAlumnos;