import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import Home from './views/Home';
import Register from './views/Register';
import Login from './views/Login';

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
