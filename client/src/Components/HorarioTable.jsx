import React from "react";
import {
  Box,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Modal,
  ModalContent,
  ModalOverlay,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
} from "@chakra-ui/react";

import { useQuery } from "@tanstack/react-query";
import { getAllSchedulesFromParalelo } from "../api/schedule";
function HorarioTable({ isOpen, onClose, paralelo, curso }) {
  // Definir los días de la semana
  const diasSemana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"];

  const horarioQuery = useQuery({
    queryKey: ["schedule", curso, paralelo],
    queryFn: getAllSchedulesFromParalelo(curso, paralelo) 
  })

  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <ModalOverlay />
      <ModalContent maxW={"50vw"}>
        <ModalHeader>Horario</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          <Box
            className="horario-table-container"
            p={4}
            width="100%"
            overflowX="auto">
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
                {[
                  "1-2",
                  "3-4",
                  "5-6",
                  "7-8",
                  "9-10",
                  "11-12",
                  "13-14",
                  "15-16",
                  "17-18",
                  "19-20",
                ].map((hora) => (
                  <Tr key={hora}>
                    <Td>{hora}</Td>
                    {diasSemana.map((dia) => {
                      // Buscar el horario correspondiente para cada día y hora
                      const horario = (horarioQuery.data ? horarioQuery.data : []).find(
                        (h) => h.dia === dia && h.bloque_nombre === hora
                      );

                      return (
                        <Td key={dia} bg={horario ? "red.200" : "green.200"}>
                          {horario ? "Ocupado" : "Vacío"}
                        </Td>
                      );
                    })}
                  </Tr>
                ))}
              </Tbody>
            </Table>
          </Box>
        </ModalBody>
      </ModalContent>
    </Modal>
  );
}

export default HorarioTable;
