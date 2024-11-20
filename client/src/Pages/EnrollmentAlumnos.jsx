import React, { useState } from "react";
import {
  Box,
  Heading,
  HStack,
  Text,
  Button,
  Stack,
  StackDivider,
  Select,
} from "@chakra-ui/react";

import { useMutation, useQuery } from "@tanstack/react-query";
import { getAllCursos, getAllParallelsFromCourse } from "../api/courses";

import Horario from "./Horario";
import {
  getAllInscripcionesFromParalelo,
  getInscripcionEstudiante,
  inscribirEstudiante,
  eliminarInscripcion,
} from "../api/enrollment";
import { getAllSchedulesFromParalelo } from "../api/schedule";

export const EnrollmentAlumnos = () => {
  // Datos ficticios de los ramos
  // const [ramos, setRamos] = useState([
  //   {
  //     id: 1,
  //     nombre: "Matemáticas",
  //     codigo: "MAT101",
  //     creditos: 5,
  //     inscritos: "12/30",
  //     paralelos: [
  //       { id: 1, numero: 200 },
  //       { id: 2, numero: 201 },
  //     ],
  //   },
  //   {
  //     id: 2,
  //     nombre: "Física",
  //     codigo: "FIS102",
  //     creditos: 4,
  //     inscritos: "29/30",
  //     paralelos: [
  //       { id: 3, numero: 201 },
  //       { id: 4, numero: 204 },
  //     ],
  //   },
  //   {
  //     id: 3,
  //     nombre: "Química",
  //     codigo: "QUI103",
  //     creditos: 6,
  //     inscritos: "15/15",
  //     paralelos: [
  //       { id: 5, numero: 200 },
  //       { id: 6, numero: 201 },
  //     ],
  //   },
  //   {
  //     id: 4,
  //     nombre: "Biología",
  //     codigo: "BIO104",
  //     creditos: 3,
  //     inscritos: "40/40",
  //     paralelos: [
  //       { id: 7, numero: 202 },
  //       { id: 8, numero: 207 },
  //     ],
  //   },
  //   {
  //     id: 5,
  //     nombre: "Historia",
  //     codigo: "HIS105",
  //     creditos: 4,
  //     inscritos: "23/35",
  //     paralelos: [
  //       { id: 9, numero: 200 },
  //       { id: 10, numero: 201 },
  //     ],
  //   },
  //   {
  //     id: 6,
  //     nombre: "Programacion",
  //     codigo: "PRO115",
  //     creditos: 5,
  //     inscritos: "29/35",
  //     paralelos: [
  //       { id: 11, numero: 200 },
  //       { id: 12, numero: 201 },
  //     ],
  //   },
  //   {
  //     id: 7,
  //     nombre: "Deporte",
  //     codigo: "DEP165",
  //     creditos: 2,
  //     inscritos: "34/35",
  //     paralelos: [
  //       { id: 13, numero: 200 },
  //       { id: 14, numero: 201 },
  //     ],
  //   },
  // ]);

  const [selectedParallels, setSelectedParallels] = useState([]);

  //STUDENT_ID sacado de la sesion
  const [student_id, setStudent_id] = useState(10);

  const inscripcionesEstudianteQuery = useQuery({
    queryKey: ["inscripciones_estudiante", student_id],
    queryFn: () => {
      //course_id, parallel_id, is_active
      let inscripciones = getInscripcionEstudiante(student_id);
      let cursos_inscritos = cursosQuery.data
        .filter((curso) =>
          inscripciones.some((inscripcion) => inscripcion.course_id == curso.id)
        )
        .map((curso) => {
          const los_cursos = inscripciones.filter(
            (inscripcion) => inscripcion.course_id === curso.id
          );
          const paralelosFiltrados = curso.paralelos.filter((paralelo) =>
            los_cursos.some(
              (inscripcion) => inscripcion.parallel_id === paralelo.id
            )
          );

          const isActive = los_cursos[0]?.is_active;
          const inscripcion_id = los_cursos[0]?.id;

          return {
            ...curso,
            paralelos: paralelosFiltrados,
            estado: isActive,
            id_inscripcion: inscripcion_id,
          };
        });
      return cursos_inscritos;
    },
  });

  const cursosQuery = useQuery({
    queryKey: ["courses"],
    queryFn: getAllCursos,
  });

  const paralelosQuery = useQuery({
    queryKey: ["prallels"],
    queryFn: () => {
      return cursosQuery.data.map((value, index) => {
        let cursos_formateados = [];
        let paralelos = getAllParallelsFromCourse(value.id);

        setSelectedParallels([
          ...selectedParallels,
          { cursoId: value.id, paraleloId: paralelos[0]?.id },
        ]);

        cursos_formateados = [
          ...cursos_formateados,
          {
            id: value.id,
            codigo: value.sigla,
            creditos: value.creditos,
            paralelos: paralelos.map((paralelo) => {
              return { id: paralelo.id, numero: paralelo.number };
            }),
          },
        ];
        return cursos_formateados;
      });
    },
  });

  const inscribirEstudianteMutation = useMutation({
    mutationFn: inscribirEstudiante,
    onError: (data) => console.log("Error en la inscripcion"),
  });

  const eliminarInscripcionMutation = useMutation({
    mutationFn: eliminarInscripcion,
    onError: (data) => console.log("Error en la eliminación de la inscripcion"),
  });

  // const [ramosInscritos, setRamosInscritos] = useState([
  //   {
  //     id: 8,
  //     nombre: "Matemáticas",
  //     codigo: "MAT102",
  //     creditos: 5,
  //     estado: "Inscrita",
  //     paralelos: [
  //       { id: 15, numero: 200 },
  //       { id: 16, numero: 201 },
  //     ],
  //      id_inscripcion: 20
  //   },
  //   {
  //     id: 9,
  //     nombre: "Física",
  //     codigo: "FIS103",
  //     creditos: 4,
  //     inscritos: "29/30",
  //     estado: "Inscrita",
  //     paralelos: [
  //       { id: 17, numero: 201 },
  //       { id: 18, numero: 204 },
  //     ],
  //   },
  //   {
  //     id: 10,
  //     nombre: "Química",
  //     codigo: "QUI104",
  //     creditos: 6,
  //     inscritos: "15/15",
  //     estado: "Pendiente",
  //     paralelos: [
  //       { id: 19, numero: 200 },
  //       { id: 20, numero: 201 },
  //     ],
  //   },
  //   {
  //     id: 11,
  //     nombre: "Deporte",
  //     codigo: "DEP109",
  //     creditos: 2,
  //     inscritos: "15/15",
  //     estado: "Pendiente",
  //     paralelos: [
  //       { id: 21, numero: 200 },
  //       { id: 22, numero: 201 },
  //     ],
  //   },
  //   {
  //     id: 12,
  //     nombre: "Programacion",
  //     codigo: "PRO119",
  //     creditos: 5,
  //     inscritos: "38/40",
  //     estado: "Inscrita",
  //     paralelos: [
  //       { id: 23, numero: 200 },
  //       { id: 24, numero: 201 },
  //     ],
  //   },
  // ]);

  const [verHorariosInscritos, setVerHorariosInscritos] = useState([
    {
      codigo: "MAT102",
      curso_id: 8,
      paralelo_id: 15,
      numero: 200,
      horario: [
        { dia: "Martes", bloque: "11-12" },
        { dia: "Jueves", bloque: "11-12" },
      ],
    },
    {
      codigo: "FIS103",
      curso_id: 9,
      paralelo_id: 17,
      numero: 201,
      horario: [
        { dia: "Miércoles", bloque: "11-12" },
        { dia: "Viernes", bloque: "11-12" },
      ],
    },
    {
      codigo: "QUI104",
      curso_id: 10,
      paralelo_id: 20,
      numero: 201,
      horario: [
        { dia: "Lunes", bloque: "3-4" },
        { dia: "Lunes", bloque: "5-6" },
      ],
    },
    {
      codigo: "DEP109",
      curso_id: 11,
      paralelo_id: 22,
      numero: 201,
      horario: [
        { dia: "Viernes", bloque: "1-2" },
        { dia: "Viernes", bloque: "3-4" },
      ],
    },
    {
      codigo: "PRO119",
      curso_id: 12,
      paralelo_id: 24,
      numero: 201,
      horario: [
        { dia: "Martes", bloque: "9-10" },
        { dia: "Jueves", bloque: "11-12" },
      ],
    },
  ]);
  const [verHorariosRamo, setVerHorariosRamo] = useState(null);

  const horariosQuery = useQuery({
    queryKey: ["horarios", selectedParallels],
    queryFn: () => {
      let horariosFinales = [];

      selectedParallels.forEach((value) => {
        let horarios = getAllSchedulesFromParalelo(
          value.cursoId,
          value.paraleloId
        );
        let horarios_formateados = horarios.reduce((acc, curr) => {
          let paralelo = acc.find(
            (item) =>
              item.curso_id === curr.course_id &&
              item.paralelo_id === curr.paralell_id
          );
          if (paralelo) {
            paralelo.horario.push({
              dia: curr.dia,
              bloque: curr.bloque_nombre,
            });
          } else {
            acc.push({
              curso_id: curr.course_id,
              paralelo_id: curr.parallel_id,
              horario: [{ dia: curr.dia, bloque: curr.bloque_nombre }],
            });
          }
          return acc;
        }, []);

        horariosFinales.push(...horarios_formateados);
      });
    },
  });

  const [Horariosdb, setHorariosdb] = useState([
    {
      curso_id: 1,
      paralelo_id: 1,
      numero: 200,
      horario: [
        { dia: "Lunes", bloque: "3-4" },
        { dia: "Miércoles", bloque: "3-4" },
      ],
    },
    {
      curso_id: 1,
      paralelo_id: 2,
      numero: 201,
      horario: [
        { dia: "Martes", bloque: "1-2" },
        { dia: "Jueves", bloque: "5-6" },
      ],
    },
    {
      curso_id: 2,
      paralelo_id: 3,
      numero: 201,
      horario: [
        { dia: "Lunes", bloque: "7-8" },
        { dia: "Miércoles", bloque: "7-8" },
      ],
    },
    {
      curso_id: 2,
      paralelo_id: 4,
      numero: 204,
      horario: [
        { dia: "Martes", bloque: "9-10" },
        { dia: "Jueves", bloque: "9-10" },
      ],
    },
    {
      curso_id: 3,
      paralelo_id: 5,
      numero: 200,
      horario: [
        { dia: "Lunes", bloque: "1-2" },
        { dia: "Miércoles", bloque: "1-2" },
      ],
    },
    {
      curso_id: 3,
      paralelo_id: 6,
      numero: 201,
      horario: [
        { dia: "Martes", bloque: "3-4" },
        { dia: "Jueves", bloque: "3-4" },
      ],
    },
    {
      curso_id: 4,
      paralelo_id: 7,
      numero: 202,
      horario: [
        { dia: "Lunes", bloque: "3-4" },
        { dia: "Miércoles", bloque: "3-4" },
      ],
    },
    {
      curso_id: 4,
      paralelo_id: 8,
      numero: 207,
      horario: [
        { dia: "Martes", bloque: "7-8" },
        { dia: "Jueves", bloque: "7-8" },
      ],
    },
    {
      curso_id: 5,
      paralelo_id: 9,
      numero: 200,
      horario: [
        { dia: "Lunes", bloque: "9-10" },
        { dia: "Miércoles", bloque: "9-10" },
      ],
    },
    {
      curso_id: 5,
      paralelo_id: 10,
      numero: 201,
      horario: [
        { dia: "Martes", bloque: "11-12" },
        { dia: "Jueves", bloque: "11-12" },
      ],
    },
    {
      curso_id: 6,
      paralelo_id: 11,
      numero: 200,
      horario: [
        { dia: "Martes", bloque: "11-12" },
        { dia: "Jueves", bloque: "11-12" },
      ],
    },
    {
      curso_id: 6,
      paralelo_id: 12,
      numero: 201,
      horario: [
        { dia: "Martes", bloque: "11-12" },
        { dia: "Jueves", bloque: "11-12" },
      ],
    },
    {
      curso_id: 7,
      paralelo_id: 13,
      numero: 200,
      horario: [
        { dia: "Martes", bloque: "11-12" },
        { dia: "Jueves", bloque: "11-12" },
      ],
    },
    {
      curso_id: 7,
      paralelo_id: 14,
      numero: 201,
      horario: [
        { dia: "Martes", bloque: "11-12" },
        { dia: "Jueves", bloque: "11-12" },
      ],
    },
    {
      curso_id: 8,
      paralelo_id: 15,
      numero: 200,
      horario: [
        { dia: "Martes", bloque: "11-12" },
        { dia: "Jueves", bloque: "11-12" },
      ],
    },
    {
      curso_id: 8,
      paralelo_id: 16,
      numero: 201,
      horario: [
        { dia: "Lunes", bloque: "11-12" },
        { dia: "Jueves", bloque: "11-12" },
      ],
    },
    {
      curso_id: 9,
      paralelo_id: 17,
      numero: 201,
      horario: [
        { dia: "Miercoles", bloque: "11-12" },
        { dia: "Viernes", bloque: "11-12" },
      ],
    },
    {
      curso_id: 9,
      paralelo_id: 18,
      numero: 204,
      horario: [
        { dia: "Martes", bloque: "11-12" },
        { dia: "Jueves", bloque: "11-12" },
      ],
    },
    {
      curso_id: 10,
      paralelo_id: 19,
      numero: 200,
      horario: [
        { dia: "Lunes", bloque: "11-12" },
        { dia: "Jueves", bloque: "9-10" },
      ],
    },
    {
      curso_id: 10,
      paralelo_id: 20,
      numero: 201,
      horario: [
        { dia: "Martes", bloque: "11-12" },
        { dia: "Jueves", bloque: "11-12" },
      ],
    },
    {
      curso_id: 11,
      paralelo_id: 21,
      numero: 200,
      horario: [
        { dia: "Martes", bloque: "11-12" },
        { dia: "Jueves", bloque: "11-12" },
      ],
    },
    {
      curso_id: 11,
      paralelo_id: 22,
      numero: 201,
      horario: [
        { dia: "Martes", bloque: "11-12" },
        { dia: "Jueves", bloque: "11-12" },
      ],
    },
    {
      curso_id: 12,
      paralelo_id: 23,
      numero: 200,
      horario: [
        { dia: "Martes", bloque: "11-12" },
        { dia: "Jueves", bloque: "11-12" },
      ],
    },
    {
      curso_id: 12,
      paralelo_id: 24,
      numero: 201,
      horario: [
        { dia: "Martes", bloque: "11-12" },
        { dia: "Jueves", bloque: "11-12" },
      ],
    },
  ]);

  const handleSelectParallel = (event) => {
    setSelectedParallels((prev) =>
      prev.map((item) =>
        item.cursoId === event.target.curso
          ? { ...item, paraleloId: event.target.id }
          : item
      )
    );
  };

  // const handleSelectParallelInscrito = (cursoId, newParaleloId) => {
  //   setSelectedParallelsInscrito((prev) =>
  //     prev.map((item) =>
  //       item.cursoId === cursoId ? { ...item, paraleloId: newParaleloId } : item
  //     )
  //   );
  // };

  const handleEliminar = (id_curso, id_paralelo, id_inscripcion) => {
    eliminarInscripcionMutation.mutate({
      course_id: id_curso,
      parallel_id: id_paralelo,
      enrollment_id: id_inscripcion,
    });
  };

  const handleInscribir = (ramoId, paraleloId) => {
    inscribirEstudianteMutation.mutate({
      course_id: ramoId,
      paralell_id: paraleloId,
      estudiante: JSON.stringify({ student_id: student_id }),
    });
  };

  const handleHorario = (cursoId) => {
    //esperando a schedule
    const view_parallel = selectedParallels.filter(
      (h) => h.cursoId === cursoId
    );
    const horario = horariosQuery.data.filter(
      (h) =>
        h.curso_id == cursoId && h.paralelo_id == view_parallel[0].paraleloId
    );
    const ramo = paralelosQuery.data.filter((h) => h.id === cursoId);

    setVerHorariosRamo({ codigo: ramo[0].codigo, ...horario[0] });
  };

  if (cursosQuery.status === "pending") {
    return <h1>perate</h1>;
  } else if (cursosQuery.status == "error") {
    return <h1>Explote Curso: {cursosQuery.error.message}</h1>;
  }

  return (
    <Box>
      <Heading color="gray.800" pt={5} textAlign="center">
        Inscripción de Ramos
      </Heading>
      <HStack spacing={4} align="start">
        {/* Sección de ramos */}
        <Box p={5} bg="white" width="60%">
          <Heading size="md" color="gray.800" mb={2}>
            Ramos para Inscribir
          </Heading>
          <Stack
            separator={<StackDivider />}
            align="stretch"
            spacing={4}
            borderWidth={3}
            borderRadius="md"
            p={4}
            shadow="md"
            maxHeight="40vh"
            overflowY="auto">
            {paralelosQuery.data.map((ramo) => (
              <Box key={ramo.id}>
                <HStack spacing={4} justify="space-between" align="center">
                  <Text
                    flex={1}
                    fontSize="md"
                    fontWeight="bold"
                    color="gray.800">
                    {ramo.codigo}
                  </Text>
                  <Text flex={1} fontSize="md" color="gray.700">
                    Créditos: {ramo.creditos}
                  </Text>
                  <Text flex={1} fontSize="md" color="gray.700">
                    Inscritos: {ramo.inscritos}
                  </Text>
                  <Select onChange={handleSelectParallel}>
                    {ramo.paralelos.map((paralelo) => (
                      <option
                        key={paralelo.id}
                        value={{
                          numero: paralelo.numero,
                          id: paralelo.id,
                          curso: ramo.id,
                        }}
                        color="gray.800"
                        backgroundColor="gray.100"
                        _hover={{
                          backgroundColor: "orange.300",
                          color: "white",
                        }}>
                        {paralelo.numero}
                      </option>
                    ))}
                  </Select>
                  <Button
                    variant="outline"
                    color="gray.800"
                    _hover={{ backgroundColor: "orange.300", color: "white" }}
                    onClick={() => handleHorario(ramo.id)}>
                    Ver Horario
                  </Button>
                  <Button
                    variant="outline"
                    color="gray.800"
                    _hover={{ backgroundColor: "green.300", color: "white" }}
                    onClick={() => handleInscribir(ramo.id)}>
                    Inscribirse
                  </Button>
                </HStack>
              </Box>
            ))}
          </Stack>
        </Box>

        {/* Sección de horario */}
        <Box p={5} width="40%">
          <Heading size="md" color="gray.800" mb={2}>
            Horario
          </Heading>
          <Box>
            <Horario
              VerHorario={verHorariosRamo}
              InscritosHorario={verHorariosInscritos}
              width={90}
              height={30}
            />
          </Box>
        </Box>
      </HStack>

      {/* Sección de ramos inscritos */}
      <Box mt={2} p={5} bg="white" width="100%">
        <Heading size="md" color="gray.800" mb={4}>
          Ramos Inscritos
        </Heading>
        <Stack
          separator={<StackDivider />}
          align="stretch"
          spacing={4}
          borderWidth={3}
          borderRadius="md"
          p={4}
          shadow="md"
          maxHeight="35vh"
          overflowY="auto">
          {inscripcionesEstudianteQuery.data.map((inscrito) => {
            return (
              <Box key={inscrito.cursoId}>
                <HStack spacing={4} justify="space-between" align="center">
                  <Text
                    flex={1}
                    fontSize="md"
                    fontWeight="bold"
                    color="gray.800">
                    {inscrito.codigo}
                  </Text>
                  <Text flex={1} fontSize="md" color="gray.700">
                    Créditos: {inscrito.creditos}
                  </Text>
                  <Text flex={1} fontSize="md" color="gray.700">
                    Estado: {inscrito.estado}
                  </Text>
                  <Text flex={1} fontSize="md" color="gray.700">
                    Paralelo: {inscrito.paralelos[0].id}
                  </Text>
                  <Button
                    variant="outline"
                    color="gray.800"
                    _hover={{ backgroundColor: "red.300", color: "white" }}
                    onClick={() =>
                      handleEliminar(
                        inscrito.id,
                        inscrito.paralelos[0].id,
                        inscrito.inscripcion_id
                      )
                    }>
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
