import {BrowserRouter, Routes, Route} from 'react-router-dom'
import './App.css';
import EditSchedule from './pages/editSchedule';

function App() {
  return (
    <BrowserRouter>
      <div className='app'>
          <Routes>
            <Route path='/' element={<EditSchedule/>}/>
          </Routes>
      </div>
    
    </BrowserRouter>
  );
}

export default App;
