import React, { Fragment } from "react";

import {
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
  Tr,
  Td,
  useDisclosure,
  IconButton,
  Button
} from "@chakra-ui/react";
import { AddIcon, InfoOutlineIcon } from "@chakra-ui/icons";
import PopUpConsulta from "../Components/PopUpConsulta";
import PopUpFormParalelo from "../Components/PopUpFormParalelo";

export const AcordionCursosItem = ({
  index,
  value,
  curso,
  paralelos,
  crearParalelo,
  isAdmin,
  setSelecterParallel,
  horarioOnOpen
}) => {
  const disclosureCosulta = useDisclosure(false);
  const disclosureFormParalelo = useDisclosure(false);

  return (
    <>
      <AccordionItem key={index} value={value} as={Fragment}>
        <Tr>
          <Td>{curso.sigla}</Td>
          <Td>{curso.name}</Td>
          <Td>{curso.departamento}</Td>
          <Td>{curso.prerequisites}</Td>
          <Td>
            <AccordionButton>
              <AccordionIcon />
            </AccordionButton>
          </Td>
        </Tr>

        {paralelos.map((item, index) => {
          return (
            <AccordionPanel key={index} pb={3} paddingRight={"-20px"} marginRight={"-450px"}>
              <Tr>
                <Td>{item.paralelo}</Td>{" "}
                <Td>
                  <IconButton icon={<InfoOutlineIcon/>} onClick={disclosureCosulta.onOpen}/>
                </Td>
                <Td>
                  <Button onClick={()=>{setSelecterParallel(item.block_id); horarioOnOpen();}}>Horario</Button>
                </Td>
                <PopUpConsulta
                  dataParalelo={item}
                  isOpen={disclosureCosulta.isOpen}
                  onClose={disclosureCosulta.onClose}
                />
              </Tr>
            </AccordionPanel>
          );
        })}

        <AccordionPanel as={Tr} paddingRight={"-20px"} marginRight={"-450px"}>
          <Td/>
          <Td/>
          <Td>
            {isAdmin ? <IconButton icon={<AddIcon/>} size={"md"} onClick={disclosureFormParalelo.onOpen} paddingX={"20px"} marginX={"-20px"} /> : ""}
          </Td>
        </AccordionPanel>

          {isAdmin ? <PopUpFormParalelo
            dataCurso={curso}
            isOpen={disclosureFormParalelo.isOpen}
            onClose={disclosureFormParalelo.onClose}
            crearParalelo={crearParalelo}
          /> : ""}
        
      </AccordionItem>
    </>
  );
};

export default AcordionCursosItem;
