import React from "react";
import { Box, Table, Thead, Tbody, Tr, Th, Td } from "@chakra-ui/react";

function HorarioTable({ bloqueId }) {
  // Datos de ejemplo de horarios para cada bloque y día de la semana
  const horarios = [
    { id: 1, bloque_id: 101, dia: "Lunes", hora: "1-2", ocupado: true },
    { id: 2, bloque_id: 101, dia: "Lunes", hora: "5-6", ocupado: false },
    { id: 3, bloque_id: 101, dia: "Martes", hora: "11-12", ocupado: true },
    { id: 4, bloque_id: 102, dia: "Miércoles", hora: "15-16", ocupado: false },
    { id: 5, bloque_id: 102, dia: "Miércoles", hora: "7-8", ocupado: true },
    { id: 6, bloque_id: 103, dia: "Jueves", hora: "3-4", ocupado: true },
    { id: 7, bloque_id: 103, dia: "Viernes", hora: "15-16", ocupado: false },
    // Más horarios según sea necesario
  ];

  // Filtrar los horarios por bloqueId
  const horariosFiltrados = horarios.filter((horario) => horario.bloque_id === bloqueId);

  // Definir los días de la semana
  const diasSemana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"];

  return (
    <Box className="horario-table-container" p={4} width="100%" overflowX="auto">
      <Table variant="simple" className="horario-table" width="100%">
        <Thead>
          <Tr>
            <Th>Hora</Th>
            {diasSemana.map((dia) => (
              <Th key={dia}>{dia}</Th>
            ))}
          </Tr>
        </Thead>
        <Tbody>
          {/* Horas predefinidas (8:00, 10:00, 12:00, etc.) */}
          {["1-2", "3-4", "5-6", "7-8", "9-10", "11-12", "13-14", "15-16", "17-18", "19-20"].map((hora) => (
            <Tr key={hora}>
              <Td>{hora}</Td>
              {diasSemana.map((dia) => {
                // Buscar el horario correspondiente para cada día y hora
                const horario = horariosFiltrados.find(
                  (h) => h.dia === dia && h.hora === hora
                );
                const isOcupado = horario ? horario.ocupado : false;

                return (
                  <Td key={dia} bg={isOcupado ? "red.200" : "green.200"}>
                    {isOcupado ? "Ocupado" : "Vacío"}
                  </Td>
                );
              })}
            </Tr>
          ))}
        </Tbody>
      </Table>
    </Box>
  );
}

export default HorarioTable;