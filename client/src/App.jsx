import React from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Signin from './pages/Signin'
import Signup from './pages/Signup'


const App = () => {
  return (
    <>
    <BrowserRouter>
    <Routes>
    <Route path="/signin" element={<Signin/>} />
    <Route path="/signup" element={<Signup/>} />
    </Routes>
    </BrowserRouter>
    </>
  )
}

export default App
