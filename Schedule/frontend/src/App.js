import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Route, Routes, useNavigate } from "react-router-dom";
import { Box,Button, Heading, Stack,Input, Select, Table, Tbody, Td, Th, Thead, Tr, Modal, ModalOverlay, ModalContent, ModalHeader, ModalCloseButton, ModalBody, useDisclosure } from "@chakra-ui/react";
import HorarioTable from "./pages/HorarioTable";
import './App.css';
import EditSchedule from "./pages/editSchedule";
// import CrearCurso from "./pages/CrearCurso";
// import EliminarCurso from "./pages/EliminarCurso";

function App() {
  const [selectedBloqueId, setSelectedBloqueId] = useState(null);
  const [isAdmin, setIsAdmin] = useState(false);
  const [filters, setFilters] = useState({ curso: "", paralelo: "", profesor: "" });
  const [cursos, setCursos] = useState([
    {
      id: 1,
      nombre: "Matemáticas",
      paralelo: "A",
      nombre_profesor: "Juan Pérez",
      bloque_id: 101,
    },
    {
      id: 2,
      nombre: "Física",
      paralelo: "B",
      nombre_profesor: "Ana Gómez",
      bloque_id: 102,
    },
    {
      id: 3,
      nombre: "Historia",
      paralelo: "A",
      nombre_profesor: "Carlos López",
      bloque_id: 103,
    },
    {
      id: 4,
      nombre: "Biología",
      paralelo: "C",
      nombre_profesor: "Elena Rodríguez",
      bloque_id: 104,
    },
  ]);
  const [filteredCursos, setFilteredCursos] = useState([]);
  const [paralelos, setParalelos] = useState(["A", "B", "C"]);

  const navigate = useNavigate();
  const { isOpen, onOpen, onClose } = useDisclosure();

  useEffect(() => {
    setFilteredCursos(cursos);
    const userIsAdmin = true;
    setIsAdmin(userIsAdmin);
  }, [cursos]);

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters((prevFilters) => ({
      ...prevFilters,
      [name]: value,
    }));
  };

  const handleSearch = () => {
    const filtered = cursos.filter((curso) => {
      const matchCurso = filters.curso === "" || curso.nombre === filters.curso;
      const matchParalelo = filters.paralelo === "" || curso.paralelo.toString() === filters.paralelo;
      const matchProfesor = curso.nombre_profesor.toLowerCase().includes(filters.profesor.toLowerCase());
      return matchCurso && matchParalelo && matchProfesor;
    });
    setFilteredCursos(filtered);
  };

  const handleOpenHorario = (bloqueId) => {
    setSelectedBloqueId(bloqueId);
    onOpen();
  };

  const goToEditarPagina = () => {
    navigate("/editar-pagina");
  };

  const goToCrearCurso = () => {
    navigate("/crear-curso");
  };

  const goToEliminarCurso = () => {
    navigate("/eliminar-curso");
  };

  return (
    <Box p={4}>
      <Heading mb={4}>Tabla de Cursos</Heading>

      <Box mb={4}>       
        <Stack spacing={4} mb={4} direction="row">
          <Select
            name="curso"
            value={filters.curso}
            onChange={handleFilterChange}
            placeholder="Seleccionar Curso"
            width="200px"
          >
            {cursos.map((curso) => (
              <option key={curso.id} value={curso.nombre}>
                {curso.nombre}
              </option>
            ))}
          </Select>
        
          <Select
            name="paralelo"
            value={filters.paralelo}
            onChange={handleFilterChange}
            placeholder="Seleccionar Paralelo"
            width="200px"
          >
            {paralelos.map((paralelo, index) => (
              <option key={index} value={paralelo}>
                {paralelo}
              </option>
            ))}
          </Select>
        
          <Input
            type="text"
            name="profesor"
            placeholder="Buscar por Profesor"
            value={filters.profesor}
            onChange={handleFilterChange}
            width="200px"
          />
        
          <Button onClick={handleSearch} colorScheme="green" width="100px" mr={150}>
            Buscar
          </Button>
          {isAdmin && (
            <Box>
                <Stack direction="row">
                <Button onClick={goToEditarPagina} colorScheme="blue" mr={1}>
                  Editar Página
                </Button>
                <Button onClick={goToCrearCurso} colorScheme="blue" mr={1}>
                  Crear Curso
                </Button>
                <Button onClick={goToEliminarCurso} colorScheme="blue">
                  Eliminar Curso
                </Button>
                </Stack>
              
            </Box>
          )}
        </Stack>

      </Box>

      <Table variant="simple">
        <Thead>
          <Tr>
            <Th>Curso</Th>
            <Th>Paralelo</Th>
            <Th>Profesor</Th>
            <Th>Horario</Th>
          </Tr>
        </Thead>
        <Tbody>
          {filteredCursos.map((curso) => (
            <Tr key={curso.id}>
              <Td>{curso.nombre}</Td>
              <Td>{curso.paralelo}</Td>
              <Td>{curso.nombre_profesor}</Td>
              <Td>
                <Button onClick={() => handleOpenHorario(curso.bloque_id)} colorScheme="green">
                  Ver Horario
                </Button>
              </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>

      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent maxWidth="50vw" width="50vw">
          <ModalHeader>Horario</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <HorarioTable bloqueId={selectedBloqueId} />
          </ModalBody>
        </ModalContent>
      </Modal>
    </Box>
  );
}

function MainApp() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/editar-pagina" element={<EditSchedule />} />
        {/* <Route path="/crear-curso" element={<CrearCurso />} />
        <Route path="/eliminar-curso" element={<EliminarCurso />} /> */}
      </Routes>
    </Router>
  );
}

export default MainApp;