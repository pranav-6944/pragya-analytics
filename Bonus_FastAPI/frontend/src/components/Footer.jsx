import React from 'react'
import { Link } from 'react-router-dom'

const links = {
  'About PRAGYA': ['Overview', 'How It Works', 'Technology Stack', 'Team'],
  'Features': ['Predict Performance', 'At-Risk Detection', 'Advanced Analytics', 'Smart Insights'],
  'Contact': ['GitHub Repository', 'Documentation', 'Report an Issue', 'Contribute'],
}

export default function Footer() {
  return (
    <footer className="bg-navy-900 text-white">
      <div className="max-w-6xl mx-auto px-6 py-16">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-10 mb-12">
          {/* Brand */}
          <div className="md:col-span-1">
            <div className="flex items-center gap-2.5 mb-5">
              <img src="/logo.png" alt="PRAGYA Logo" className="w-9 h-9 object-contain" />
              <span className="text-lg font-bold tracking-tight">PRAGYA</span>
            </div>
            <p className="text-white/50 text-sm leading-relaxed mb-5">
              Academic intelligence system powered by machine learning.
              Empowering universities with data-driven insights.
            </p>
            <div className="flex items-center gap-3">
              <a href="#" aria-label="GitHub"
                className="w-9 h-9 bg-white/5 hover:bg-white/15 border border-white/10 rounded-lg
                           flex items-center justify-center text-sm transition-colors">
                ⌨
              </a>
              <a href="#" aria-label="Docs"
                className="w-9 h-9 bg-white/5 hover:bg-white/15 border border-white/10 rounded-lg
                           flex items-center justify-center text-sm transition-colors">
                📄
              </a>
            </div>
          </div>

          {/* Nav columns */}
          {Object.entries(links).map(([section, items]) => (
            <div key={section}>
              <h4 className="text-white text-sm font-semibold mb-5">{section}</h4>
              <ul className="space-y-3">
                {items.map(item => (
                  <li key={item}>
                    <Link to="/dashboard"
                      className="text-white/40 hover:text-white/80 text-sm transition-colors">
                      {item}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Bottom bar */}
        <div className="border-t border-white/10 pt-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-white/30 text-sm">
            © 2026 PRAGYA &nbsp;·&nbsp; Built for Academic Excellence
          </p>
          <div className="flex items-center gap-6">
            <span className="text-white/30 text-xs">Pranav Lamkhade &nbsp;·&nbsp; Roll 42 &nbsp;·&nbsp; PRN 202401120062</span>
          </div>
        </div>
      </div>
    </footer>
  )
}
