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

  // Lock body scroll when mobile menu is open
  useEffect(() => {
    if (menuOpen) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = 'unset'
    }
    return () => { document.body.style.overflow = 'unset' }
  }, [menuOpen])

  return (
    <>
      <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300
        ${scrolled ? 'bg-white/95 backdrop-blur shadow-sm border-b border-gray-100' : 'bg-transparent'}`}>
        <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2.5 z-10" onClick={() => setMenuOpen(false)}>
            <img src="/logo.png" alt="PRAGYA Logo" className="w-9 h-9 object-contain" />
            <span className="text-lg font-bold text-navy-900 tracking-tight">PRAGYA</span>
          </Link>

          {/* Desktop nav */}
          <div className="hidden md:flex items-center gap-6 lg:gap-8">
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

          {/* Mobile hamburger button */}
          <button className="md:hidden p-2 z-10 rounded-lg hover:bg-gray-100/50 transition-colors"
                  aria-label="Toggle Navigation Menu"
                  onClick={() => setMenuOpen(!menuOpen)}>
            <div className="w-5 h-4 flex flex-col justify-between">
              <div className={`w-5 h-0.5 bg-navy-900 rounded-full transition-all duration-300 origin-left ${menuOpen ? 'rotate-45 translate-x-0.5 -translate-y-0.5' : ''}`} />
              <div className={`w-5 h-0.5 bg-navy-900 rounded-full transition-all duration-300 ${menuOpen ? 'opacity-0 scale-x-0' : ''}`} />
              <div className={`w-5 h-0.5 bg-navy-900 rounded-full transition-all duration-300 origin-left ${menuOpen ? '-rotate-45 translate-x-0.5 translate-y-0.5' : ''}`} />
            </div>
          </button>
        </div>
      </nav>

      {/* Mobile drawer backdrop */}
      {menuOpen && (
        <div className="fixed inset-0 bg-navy-900/40 backdrop-blur-sm z-40 md:hidden animate-fade-in"
             onClick={() => setMenuOpen(false)} />
      )}

      {/* Mobile drawer menu */}
      <div className={`fixed top-16 left-0 right-0 bg-white border-b border-gray-100 z-40 md:hidden shadow-xl
        transition-all duration-300 ease-in-out transform ${menuOpen ? 'translate-y-0 opacity-100' : '-translate-y-full opacity-0 pointer-events-none'}`}>
        <div className="px-6 py-6 flex flex-col gap-4 max-h-[calc(100vh-4rem)] overflow-y-auto">
          {[['Features','#features'],['How It Works','#how'],['Use Cases','#usecases']].map(([label, href]) => (
            <a key={label} href={href} onClick={() => setMenuOpen(false)}
               className="text-base font-semibold text-navy-800 hover:text-accent py-2 border-b border-gray-50 flex items-center justify-between">
              <span>{label}</span>
              <span className="text-gray-300 text-xs">→</span>
            </a>
          ))}
          <Link to="/guide" onClick={() => setMenuOpen(false)}
                className="text-base font-semibold text-navy-800 hover:text-accent py-2 border-b border-gray-50 flex items-center justify-between">
            <span>User Guide</span>
            <span className="text-gray-300 text-xs">📖</span>
          </Link>
          <Link to="/dashboard" onClick={() => setMenuOpen(false)}
                className="text-base font-semibold text-navy-800 hover:text-accent py-2 border-b border-gray-50 flex items-center justify-between">
            <span>Analytics Dashboard</span>
            <span className="text-gray-300 text-xs">📊</span>
          </Link>
          <div className="pt-2">
            <Link to="/dashboard" onClick={() => setMenuOpen(false)}
                  className="btn-primary text-base py-3.5 w-full justify-center text-center shadow-lg">
              🚀 Open Dashboard
            </Link>
          </div>
        </div>
      </div>
    </>
  )
}
