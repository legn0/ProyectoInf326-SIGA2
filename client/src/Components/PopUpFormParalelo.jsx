import { React, useState } from "react";
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

export const PopUpFormParalelo = ({ dataCurso, isOpen, onClose, crearParalelo }) => {
  const [nuevoParalelo, setNuevoParalelo] = useState({
    curso: dataCurso.sigla,
    paralelo: -1,
    limite_cupo: -1,
    jornada: "Diurna",
    campus_sede: "San Joaquin",
  });

  const handleParaleloChange = (event) => {
    setNuevoParalelo({ ...nuevoParalelo, paralelo: event.target.value });
  };

  const handleLimiteChange = (event) => {
    setNuevoParalelo({ ...nuevoParalelo, limite_cupo: event.target.value });
  };

  const handleJornadaChange = (event) => {
    setNuevoParalelo({ ...nuevoParalelo, jornada: event.target.value });
  };

  const handleCampusChange = (event) => {
    setNuevoParalelo({ ...nuevoParalelo, campus_sede: event.target.value });
  };

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
            <NumberInput defaultValue={200} >
              <NumberInputField onChange={handleParaleloChange}/>
            </NumberInput>
          </FormControl>
        </ModalHeader>
        <ModalCloseButton />
        <ModalBody pt={10}>
          <FormControl pt={3} isRequired>
            <FormLabel>Limite de Cupo</FormLabel>
            <NumberInput defaultValue={60} >
              <NumberInputField onChange={handleLimiteChange}/>
            </NumberInput>
          </FormControl>
          <FormControl pt={3} isRequired>
            <FormLabel>Jornada</FormLabel>
            <Select onChange={handleJornadaChange}>
              <option value={"Diurna"}>Diurna</option>
              <option value={"Vespertina"}>Vespertina</option>
            </Select>
          </FormControl>
          <FormControl pt={3} isRequired>
            <FormLabel>Campus/Sede</FormLabel>
            <Select onChange={handleCampusChange}>
              <option value={"Casa Central"}>Casa Central</option>
              <option value={"San Joaquin"}>San Joaquin</option>
              <option value={"Viña del Mar"}>Viña del Mar</option>
              <option value={"Vitacura"}>Vitacura</option>
              <option value={"Concepcion"}>Concepcion</option>
            </Select>
          </FormControl>
        </ModalBody>
        <ModalFooter>
          <Button
            mr={5}
            onClick={() => {
              crearParalelo(nuevoParalelo);
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
