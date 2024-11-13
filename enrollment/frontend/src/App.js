import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Box } from "@chakra-ui/react";
import EnrollmentAdministrativo from './components/EnrollmentAdministrativo';
import EnrollmentAlumnos from './components/EnrollmentAlumnos';
import EnrollmentProfesores from './components/EnrollmentProfesores';

function App() {
  return (
      <Box bg="white" minHeight="100vh">
          <Router>
            <Routes>
              <Route path="/" element={<Navigate to="/Alumnos" />} /> 
              <Route path="/Administrativo" element={<EnrollmentAdministrativo />} />
              <Route path="/Alumnos" element={<EnrollmentAlumnos />} />
              <Route path="/Profesores" element={<EnrollmentProfesores />} />
            </Routes>
          </Router>
      </Box>
  );
}
export default App;
