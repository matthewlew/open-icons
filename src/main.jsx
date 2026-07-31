import React from 'react'
import ReactDOM from 'react-dom/client'
import { HashRouter, Routes, Route } from 'react-router-dom'
import App from '../open-icons-playground_12_3.jsx'
import ReadmePage from './ReadmePage.jsx'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <HashRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/docs" element={<ReadmePage />} />
      </Routes>
    </HashRouter>
  </React.StrictMode>
)
