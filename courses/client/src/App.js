import logo from './logo.svg';
import './App.css';
import { Box } from '@chakra-ui/react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ChakraProvider } from "@chakra-ui/react";

// Componentes
import NavBar from './Components/NavBar'; // Asegúrate de que el `NavBar` esté exportado como `default` en su archivo

// Pages
import { VistaCursos } from './Pages/VistaCursos';

function App() {
  return (
    <ChakraProvider>
      <BrowserRouter>
        <div className="app">
          {/* Incluye NavBar aquí */}
          <NavBar />
          <div className="app__page">
            <Routes>
              <Route path="/" element={<VistaCursos />} />
            </Routes>
          </div>
        </div>
      </BrowserRouter>
    </ChakraProvider>
  );
}

export default App;

