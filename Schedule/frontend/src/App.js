import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Route, Routes, useNavigate } from "react-router-dom";
import HorarioTable from "./pages/HorarioTable";
import './App.css';
import EditSchedule from "./pages/editSchedule";
//import CrearCurso from "./pages/CrearCurso";
//import EliminarCurso from "./pages/EliminarCurso";

function App() {
  const [showModal, setShowModal] = useState(false);
  const [selectedBloqueId, setSelectedBloqueId] = useState(null);

  // Estado para filtros y datos
  const [filters, setFilters] = useState({ curso: "", paralelo: "", profesor: "" });
  const [cursos, setCursos] = useState([
    {
      id: 1,
      nombre: "Matemáticas",
      paralelo: "A",
      nombre_profesor: "Juan Pérez",
      bloque_id: 101
    },
    {
      id: 2,
      nombre: "Física",
      paralelo: "B",
      nombre_profesor: "Ana Gómez",
      bloque_id: 102
    },
    {
      id: 3,
      nombre: "Historia",
      paralelo: "A",
      nombre_profesor: "Carlos López",
      bloque_id: 103
    },
    {
      id: 4,
      nombre: "Biología",
      paralelo: "C",
      nombre_profesor: "Elena Rodríguez",
      bloque_id: 104
    }
  ]);
  const [filteredCursos, setFilteredCursos] = useState([]);
  const [paralelos, setParalelos] = useState(["A", "B", "C"]);

  const navigate = useNavigate();

  useEffect(() => {
    setFilteredCursos(cursos);
  }, [cursos]);

  // Función para manejar cambios en los filtros
  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters((prevFilters) => ({
      ...prevFilters,
      [name]: value,
    }));
  };

  // Función para aplicar filtros al hacer clic en "Buscar"
  const handleSearch = () => {
    const filtered = cursos.filter((curso) => {
      const matchCurso = filters.curso === "" || curso.nombre === filters.curso;
      const matchParalelo = filters.paralelo === "" || curso.paralelo.toString() === filters.paralelo;
      const matchProfesor = curso.nombre_profesor.toLowerCase().includes(filters.profesor.toLowerCase());
      return matchCurso && matchParalelo && matchProfesor;
    });
    setFilteredCursos(filtered);
  };

  // Función para abrir el modal con el horario seleccionado
  const handleOpenHorario = (bloqueId) => {
    setSelectedBloqueId(bloqueId);
    setShowModal(true);
  };

  // Función para cerrar el modal
  const handleCloseModal = () => {
    setShowModal(false);
    setSelectedBloqueId(null);
  };

  // Funciones para navegar a otros componentes
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
    <div>
      <h1>Tabla de Cursos</h1>

      {/* Filtros de búsqueda */}
      <div className="filter-container">
        <select
          name="curso"
          value={filters.curso}
          onChange={handleFilterChange}
          className="dropdown-input"
        >
          <option value="">Seleccionar Curso</option>
          {cursos.map((curso) => (
            <option key={curso.id} value={curso.nombre}>
              {curso.nombre}
            </option>
          ))}
        </select>

        <select
          name="paralelo"
          value={filters.paralelo}
          onChange={handleFilterChange}
          className="dropdown-input"
        >
          <option value="">Seleccionar Paralelo</option>
          {paralelos.map((paralelo, index) => (
            <option key={index} value={paralelo}>
              {paralelo}
            </option>
          ))}
        </select>

        <input
          type="text"
          name="profesor"
          placeholder="Buscar por Profesor"
          value={filters.profesor}
          onChange={handleFilterChange}
          className="search-input"
        />

        <button onClick={handleSearch} className="search-button">
          Buscar
        </button>

        {/* Botones adicionales */}
        <div className="action-buttons">
          <button onClick={goToEditarPagina} className="action-button">
            Editar Página
          </button>
          <button onClick={goToCrearCurso} className="action-button">
            Crear Curso
          </button>
          <button onClick={goToEliminarCurso} className="action-button">
            Eliminar Curso
          </button>
        </div>
      </div>

      {/* Tabla de cursos */}
      <table className="main-table">
        <thead>
          <tr>
            <th>Curso</th>
            <th>Paralelo</th>
            <th>Profesor</th>
            <th>Horario</th>
          </tr>
        </thead>
        <tbody>
          {filteredCursos.map((curso) => (
            <tr key={curso.id}>
              <td>{curso.nombre}</td>
              <td>{curso.paralelo}</td>
              <td>{curso.nombre_profesor}</td>
              <td>
                <button onClick={() => handleOpenHorario(curso.bloque_id)}>
                  Ver Horario
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Modal para mostrar la tabla de horarios */}
      {showModal && (
        <div className="modal">
          <div className="modal-content">
            <button onClick={handleCloseModal} className="close-button">
              Cerrar
            </button>
            <HorarioTable bloqueId={selectedBloqueId} />
          </div>
        </div>
      )}
    </div>
  );
}

// Componente principal de la aplicación con enrutamiento
function MainApp() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/editar-pagina" element={<EditSchedule />} />
        {/*<Route path="/crear-curso" element={<CrearCurso />} />
        <Route path="/eliminar-curso" element={<EliminarCurso />} />*/}
      </Routes>
    </Router>
  );
}

export default MainApp;
