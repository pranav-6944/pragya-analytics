import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false)
  const [menuOpen, setMenuOpen] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20)
    window.addEventListener('scroll', onScroll)
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300
      ${scrolled ? 'bg-white/95 backdrop-blur shadow-sm border-b border-gray-100' : 'bg-transparent'}`}>
      <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2.5">
          <div className="w-8 h-8 bg-accent rounded-lg flex items-center justify-center text-white font-bold text-sm">P</div>
          <span className="text-lg font-bold text-navy-900 tracking-tight">PRAGYA</span>
        </Link>

        {/* Desktop nav */}
        <div className="hidden md:flex items-center gap-8">
          {[['Features','#features'],['How It Works','#how'],['Use Cases','#usecases']].map(([label, href]) => (
            <a key={label} href={href}
               className="text-sm font-medium text-navy-600 hover:text-navy-900 transition-colors">
              {label}
            </a>
          ))}
          <Link to="/guide"
                className="text-sm font-medium text-navy-600 hover:text-navy-900 transition-colors">
            Guide
          </Link>
          <Link to="/dashboard"
                className="text-sm font-medium text-navy-600 hover:text-navy-900 transition-colors">
            Dashboard
          </Link>
          <Link to="/dashboard" className="btn-primary text-sm py-2.5 px-5">
            Get Started →
          </Link>
        </div>

        {/* Mobile hamburger */}
        <button className="md:hidden p-2" onClick={() => setMenuOpen(!menuOpen)}>
          <div className={`w-5 h-0.5 bg-navy-900 transition-all ${menuOpen?'rotate-45 translate-y-1.5':''}`} />
          <div className={`w-5 h-0.5 bg-navy-900 mt-1 transition-all ${menuOpen?'opacity-0':''}`} />
          <div className={`w-5 h-0.5 bg-navy-900 mt-1 transition-all ${menuOpen?'-rotate-45 -translate-y-1.5':''}`} />
        </button>
      </div>

      {/* Mobile menu */}
      {menuOpen && (
        <div className="md:hidden bg-white border-t border-gray-100 px-6 py-4 flex flex-col gap-4">
          {[['Features','#features'],['How It Works','#how'],['Use Cases','#usecases']].map(([label, href]) => (
            <a key={label} href={href} onClick={() => setMenuOpen(false)}
               className="text-sm font-medium text-navy-700">{label}</a>
          ))}
          <Link to="/dashboard" onClick={() => setMenuOpen(false)} className="btn-primary text-sm text-center">
            Open Dashboard →
          </Link>
        </div>
      )}
    </nav>
  )
}
