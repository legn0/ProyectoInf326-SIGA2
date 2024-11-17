import React, { useState } from "react";
import {
  Box,
  Text,
  VStack,
  HStack,
} from "@chakra-ui/react";


const Horario = ({ VerHorario, InscritosHorario, width=100, height=30 }) => {

    const cellWidth = `${width}px`;
    const cellHeight = `${height}px`;

    const ScheduleDays = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"];
    const ScheduleBlocks = ['1-2','3-4','5-6','7-8','9-10','11-12','13-14','15-16','17-18'];
    
    const scheduleMatrix = Array(ScheduleDays.length)
    .fill(null)
    .map(() => Array(ScheduleBlocks.length).fill({
        Text: "",
        bg: "whiteAlpha.300"
    }));

    for(const horario of InscritosHorario){
        for (const item of horario.horario){
            const day = ScheduleDays.indexOf(item["dia"]);
            const block = ScheduleBlocks.indexOf(item["bloque"]);
    
            if (day !== -1 && block !== -1) {
                if(scheduleMatrix[day][block].bg !== "whiteAlpha.300"){
                    scheduleMatrix[day][block] = {
                        Text: "TOPE",
                        bg: "orange.600",
                    };
                }else{
                    scheduleMatrix[day][block] = {
                        Text: horario?.codigo || "",
                        bg: "green.300",
                    };
                }
            }
        }
    }

    if(VerHorario){
        for (const item of VerHorario.horario){
            const day = ScheduleDays.indexOf(item["dia"]);
            const block = ScheduleBlocks.indexOf(item["bloque"]);
    
            if (day !== -1 && block !== -1) {
                if(scheduleMatrix[day][block].bg !== "whiteAlpha.300"){
                    scheduleMatrix[day][block] = {
                        Text: "TOPE",
                        bg: "orange.600",
                    };
                }else{
                    scheduleMatrix[day][block] = {
                        Text: VerHorario?.codigo || "",
                        bg: "orange.300",
                    };
                }
            }
        }
    }

    return (
    <Box bg="white" borderRadius="md" p={5} boxShadow="md" borderWidth={3} maxHeight="40vh" overflowY="auto">
        <HStack align="start" spacing={4}>
            <VStack spacing={4} align="stretch">
                <Text fontWeight="bold" textAlign="center" color="gray.800">
                    Bloques
                </Text>
                {ScheduleBlocks.map((block, index) => (
                    <Box
                    key={index}
                    bg="whiteAlpha.300"
                    p={3}
                    textAlign="center"
                    h={cellHeight}
                    w={cellWidth}
                    display="flex"
                    justifyContent="center"
                    alignItems="center"
                    >
                        <Text fontWeight="bold" color="gray.800">{block}</Text>
                    </Box>
                ))}
            </VStack>

            {scheduleMatrix.map((item, index) => (
                <VStack spacing={4} align="stretch">
                    <Text fontWeight="bold" textAlign="center" color="gray.800">
                        {ScheduleDays[index]}
                    </Text>
                    {item.map((itemDay, index) => (
                        <Box
                            key={index}
                            bg={itemDay.bg}
                            p={3}
                            textAlign="center"
                            borderWidth={1}
                            borderRadius="md"
                            h={cellHeight}
                            w={cellWidth}
                            display="flex"
                            justifyContent="center"
                            alignItems="center"
                        >
                            <Text color="gray.800">{itemDay.Text}</Text>
                        </Box>
                    ))}
                </VStack>
            ))}
        </HStack>

        <HStack mt={4}>
            <Box
                bg="green.300"
                p={3}
                textAlign="center"
                borderWidth={1}
                borderRadius="md"
                h="30px"
                w="100px"
                display="flex"
                justifyContent="center"
                alignItems="center"
            >
                <Text color="gray.800">Inscrita</Text>
            </Box>

            <Box
                bg="orange.300"
                p={3}
                textAlign="center"
                borderWidth={1}
                borderRadius="md"
                h="30px"
                w="120px"
                display="flex"
                justifyContent="center"
                alignItems="center"
            >
                <Text color="gray.800">Ver Horario</Text>
            </Box>

            <Box
                bg="orange.600"
                p={3}
                textAlign="center"
                borderWidth={1}
                borderRadius="md"
                h="30px"
                w="100px"
                display="flex"
                justifyContent="center"
                alignItems="center"
            >
                <Text color="gray.800">TOPE</Text>
            </Box>
        </HStack>
    </Box>
  );
};

export default Horario;
