import React, { Fragment } from "react";

import {
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
  Box,
  Tr,
  Td,
  Button,
  useDisclosure,
} from "@chakra-ui/react";
import PopUpConsulta from "../Components/PopUpConsulta";
import PopUpFormParalelo from "../Components/PopUpFormParalelo";

export const AcordionCursosItem = ({ index, value, curso, paralelos, crearParalelo }) => {
  const disclosureCosulta = useDisclosure(false);
  const disclosureFormParalelo = useDisclosure(false);

  return (
    <>
      <AccordionItem key={index} value={value} as={Fragment}>
        <Tr>
          <Td>{curso.sigla}</Td>
          <Td>{curso.nombre}</Td>
          <Td>{curso.departamento}</Td>
          <Td>{curso.prerequisitos}</Td>
          <Td>
            <AccordionButton>
              <AccordionIcon />
            </AccordionButton>
          </Td>
        </Tr>

        {paralelos.map((item, index) => {
          return (
            <>
              <AccordionPanel pb={4} as={Tr}>
                <Td>{item.paralelo}</Td>{" "}
                <Td>
                  <Button onClick={disclosureCosulta.onOpen}>
                    Ver Paralelo
                  </Button>
                </Td>
              </AccordionPanel>
              <PopUpConsulta
                dataParalelo={item}
                isOpen={disclosureCosulta.isOpen}
                onClose={disclosureCosulta.onClose}
              />
            </>
          );
        })}

        <AccordionPanel as={Tr}>
          <Td></Td>
          <Td>
            <Button onClick={disclosureFormParalelo.onOpen}>
              Crear Paralelo
            </Button>
          </Td>

          <PopUpFormParalelo
            dataCurso={curso}
            isOpen={disclosureFormParalelo.isOpen}
            onClose={disclosureFormParalelo.onClose}
            crearParalelo={crearParalelo}
          />
        </AccordionPanel>
      </AccordionItem>
    </>
  );
};

export default AcordionCursosItem;
