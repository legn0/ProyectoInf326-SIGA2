import './App.css';
import {BrowserRouter, Routes, Route} from 'react-router-dom'

// Pages
import VistaCursos from './Pages/VistaCursos'; // Sin llaves, ya que es exportación por defecto
import EnrollmentAdministrativo from './Pages/EnrollmentAdministrativo';
import EnrollmentAlumnos from './Pages/EnrollmentAlumnos';
import EditSchedule from './Pages/editSchedule';

function App() {
  return (
    <BrowserRouter>
      <div className='app'>
        <div className='app__page'>
          <Routes>
            <Route path='/Cursos' element={<VistaCursos />} />
            <Route path='/InscripcionAdmin' element={<EnrollmentAdministrativo/>}/>
            <Route path='/InscripcionAlumno' element={<EnrollmentAlumnos/>}/>
            <Route path="/CrearHorario/:course_id/:parallel_id" element={<EditSchedule/>}/>
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;


