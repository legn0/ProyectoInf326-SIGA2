import './App.css';
import {BrowserRouter, Routes, Route} from 'react-router-dom'

// Pages
import VistaCursos from './Pages/VistaCursos'; // Sin llaves, ya que es exportación por defecto
import EnrollmentAdministrativo from './Pages/EnrollmentAdministrativo';
import EnrollmentAlumnos from './Pages/EnrollmentAlumnos';

function App() {
  return (
    <BrowserRouter>
      <div className='app'>
        <div className='app__page'>
          <Routes>
            <Route path='/Cursos' element={<VistaCursos />} />
            <Route path='/InscripcionAdmin' element={<EnrollmentAdministrativo/>}/>
            <Route path='/InscripcionAlumno' element={<EnrollmentAlumnos/>}/>
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;


