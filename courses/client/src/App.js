import './App.css';
import {BrowserRouter, Routes, Route} from 'react-router-dom'

// Pages
import VistaCursos from './Pages/VistaCursos'; // Sin llaves, ya que es exportación por defecto

function App() {
  return (
    <BrowserRouter>
      <div className='app'>
        <div className='app__page'>
          <Routes>
            <Route path='/Cursos' element={<VistaCursos />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;


