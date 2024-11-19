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
  Button,
  Input,
  Tag,
  TagLabel,
  TagCloseButton,
  Wrap,
} from "@chakra-ui/react";

export const PopUpFormCurso = ({ isOpen, onClose, crearCurso }) => {
  const [ramos, setRamos] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [nuevoCurso, setNuevoCurso] = useState({
    sigla: "",
    nombre: "",
    departamento: "",
    creditos: 0,
  });

  const handleSiglaChange = (event) => {
    setNuevoCurso({ ...nuevoCurso, sigla: event.target.value });
  };

  const handleNombreChange = (event) => {
    setNuevoCurso({ ...nuevoCurso, nombre: event.target.value });
  };

  const handleCreditosChange = (event) => {
    setNuevoCurso({ ...nuevoCurso, creditos: event.target.value });
  }

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };


  const handleDepartamentoChange = (event) => {
    setNuevoCurso({ ...nuevoCurso, departamento: event.target.value });
  };

  const handleKeypress = (event) => {
    if (event.key === "Enter" && inputValue.trim() !== "") {
      if (!ramos.includes(inputValue.trim())) {
        setRamos([...ramos, inputValue.trim()]);
      }
      setInputValue("");
      event.preventDefault();
    }
  };

  const handleRamoRemove = (ramoToRemove) => {
    setRamos(ramos.filter((ramo) => ramo !== ramoToRemove));
  };

  const cancelClose = () => {
    setRamos([]);
    setInputValue("");
    onClose();
  };
  return (
    <Modal
      isOpen={isOpen}
      onClose={cancelClose}
      size={"4xl"}
      closeOnOverlayClick={false}>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>
          <Heading size={"xl"}> Nuevo Curso</Heading>
        </ModalHeader>
        <ModalCloseButton />
        <ModalBody pt={10}>
          <FormControl pt={3} isRequired>
            <FormLabel>Sigla</FormLabel>
            <Input onChange={handleSiglaChange} />
          </FormControl>
          <FormControl pt={3} isRequired>
            <FormLabel>Nombre</FormLabel>
            <Input onChange={handleNombreChange} />
          </FormControl>
          <FormControl pt={3} isRequired>
            <FormLabel>Departamento</FormLabel>
            <Input onChange={handleDepartamentoChange} />
          </FormControl>
          <FormControl pt={3} isRequired>
            <FormLabel>Creditos</FormLabel>
            <Input onChange={handleCreditosChange} />
          </FormControl>
          <FormControl>
            <FormLabel>Pre-requisitos:</FormLabel>
            <Input
              placeholder="Sigla Ramo prerequisito"
              value={inputValue}
              onChange={handleInputChange}
              onKeyDown={handleKeypress}
            />
            <Wrap mt={2}>
              {ramos.map((ramo, index) => (
                <Tag
                  key={index}
                  borderRadius="full"
                  variant="solid"
                  colorScheme="teal">
                  <TagLabel>{ramo}</TagLabel>
                  <TagCloseButton onClick={() => handleRamoRemove(ramo)} />
                </Tag>
              ))}
            </Wrap>
          </FormControl>
        </ModalBody>
        <ModalFooter>
          <Button
            mr={5}
            onClick={() => {
              setNuevoCurso({ ...nuevoCurso, prerequisitos: ramos.toString() });
              crearCurso(nuevoCurso);
              cancelClose();
            }}
            colorScheme="blue">
            Crear Paralelo
          </Button>
          <Button mr={5} onClick={cancelClose}>
            Cancelar
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
};

export default PopUpFormCurso;
