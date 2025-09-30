import React from 'react'
import ReactDOM from 'react-dom/client'
import Fridge from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode> {/*Используеться для отладки*/}
    <Fridge />
  </React.StrictMode>, {/*Используеться для отладки*/}
)