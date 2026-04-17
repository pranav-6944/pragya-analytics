import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Dashboard from './pages/Dashboard'
import Guide from './pages/Guide'
import './index.css'

function ScrollToTop() {
  const { pathname } = window.location
  React.useEffect(() => { window.scrollTo(0, 0) }, [pathname])
  return null
}

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/"          element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/guide"     element={<Guide />} />
      </Routes>
    </Router>
  )
}
