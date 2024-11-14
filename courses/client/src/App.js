import './App.css';
import {BrowserRouter, Routes, Route} from 'react-router-dom'

//Pages
import { VistaCursos } from './Pages/VistaCursos';



function App() {
  return (
    <BrowserRouter>
      <div className='app'>
        <div className='app__page'>
          <Routes>
            <Route path='/' element={<VistaCursos/>}/>
          </Routes>
        </div>
      </div>
    
    </BrowserRouter>
  );
}

export default App;
