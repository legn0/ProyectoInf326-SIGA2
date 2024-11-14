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
  FormControl,
  FormLabel,
  NumberInput,
  NumberInputField,
  Select,
  Button,
} from "@chakra-ui/react";

export const PopUpFormParalelo = ({ dataCurso, isOpen, onClose }) => {
  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      size={"4xl"}
      closeOnOverlayClick={false}>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>
          <Heading size={"xl"}>
            {" "}
            Crear paralelo para el curso: {dataCurso.curso}
          </Heading>
          <FormControl isRequired>
            <FormLabel>Numero Paralelo</FormLabel>
            <NumberInput defaultValue={200}>
              <NumberInputField />
            </NumberInput>
          </FormControl>
        </ModalHeader>
        <ModalCloseButton />
        <ModalBody pt={10}>
          <FormControl pt={3} isRequired>
            <FormLabel>Limite de Cupo</FormLabel>
            <NumberInput defaultValue={60}>
              <NumberInputField />
            </NumberInput>
          </FormControl>
          <FormControl pt={3} isRequired>
            <FormLabel>Jornada</FormLabel>
            <Select>
              <option value={0}>Diurna</option>
              <option value={1}>Vespertina</option>
            </Select>
          </FormControl>
          <FormControl pt={3} isRequired>
            <FormLabel>Campus/Sede</FormLabel>
            <Select>
              <option>Casa Central</option>
              <option>San Joaquin</option>
              <option>Viña del Mar</option>
              <option>Vitacura</option>
              <option>Concepcion</option>
            </Select>
          </FormControl>
        </ModalBody>
        <ModalFooter>
          <Button
            mr={5}
            onClick={() => {
              console.log("placeholder");
              onClose();
            }}
            colorScheme="blue">
            Crear Paralelo
          </Button>
          <Button mr={5} onClick={onClose}>
            Cancelar
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
};

export default PopUpFormParalelo;
