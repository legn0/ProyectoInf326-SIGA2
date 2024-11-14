import logo from './logo.svg';
import './App.css';
import {Box} from '@chakra-ui/react';
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
