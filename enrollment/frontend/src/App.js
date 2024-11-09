import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import EnrollmentAdministrativo from './components/EnrollmentAdministrativo';
import EnrollmentAlumnos from './components/EnrollmentAlumnos';
import EnrollmentProfesores from './components/EnrollmentProfesores';

function App() {
  return (
      <Router>
        <Routes>
          <Route path="/Administrativo" element={<EnrollmentAdministrativo />} />
          <Route path="/Alumnos" element={<EnrollmentAlumnos />} />
          <Route path="/Profesores" element={<EnrollmentProfesores />} />
        </Routes>
      </Router>
  );
}

export default App;
