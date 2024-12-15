import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';

import Home from './views/Home';
import Register from './views/Register';
import Login from './views/Login';

function App() {

  return (
    <BrowserRouter>
      <AuthProvider>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
          </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App
