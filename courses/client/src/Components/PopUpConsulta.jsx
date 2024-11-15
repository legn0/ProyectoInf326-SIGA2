import React from "react";
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  Heading,
  UnorderedList,
  ListItem,
} from "@chakra-ui/react";

export const PopUpConsulta = ({ dataParalelo, isOpen, onClose }) => {
  return (
    <Modal isOpen={isOpen} onClose={onClose} size={"4xl"}>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>
          <Heading size={"xl"}>Curso: {dataParalelo.curso}</Heading>
          <Heading size={"xl"}>Paralelo: {dataParalelo.paralelo}</Heading>
        </ModalHeader>
        <ModalCloseButton />

        <ModalBody pt={10}>
          <UnorderedList spacing={6} fontSize={"xl"}>
            <ListItem>Limite de Cupo: {dataParalelo.limite_cupo}</ListItem>
            <ListItem>Jornada: {dataParalelo.jornada}</ListItem>
            <ListItem>Campus/Sede: {dataParalelo.campus_sede}</ListItem>
          </UnorderedList>
        </ModalBody>
        <ModalFooter></ModalFooter>
      </ModalContent>
    </Modal>
  );
};

export default PopUpConsulta;
