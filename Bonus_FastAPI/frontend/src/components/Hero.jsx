import React from 'react'
import { Link } from 'react-router-dom'

export default function Hero() {
  return (
    <section className="relative min-h-screen flex flex-col items-center justify-center overflow-hidden bg-white pt-16">
      {/* Subtle grid background */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#f1f5f9_1px,transparent_1px),linear-gradient(to_bottom,#f1f5f9_1px,transparent_1px)] bg-[size:64px_64px]" />
      {/* Radial glow */}
      <div className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[600px] bg-accent/5 rounded-full blur-3xl" />

      <div className="relative container text-center z-10 py-20">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 bg-accent-light border border-accent/20 text-accent text-xs font-semibold uppercase tracking-widest px-5 py-2 rounded-full mb-8 animate-fade-in">
          <span className="w-1.5 h-1.5 bg-accent rounded-full animate-pulse" />
          Academic Intelligence System
        </div>

        {/* Heading */}
        <h1 className="text-5xl md:text-7xl font-bold text-navy-900 leading-[1.1] tracking-tight mb-6 animate-fade-up">
          Predict Student Success<br />
          <span className="gradient-text">Before It's Too Late</span>
        </h1>

        {/* Subheading */}
        <p className="text-xl text-navy-600 max-w-2xl mx-auto leading-relaxed mb-10 animate-fade-up" style={{animationDelay:'0.1s'}}>
          PRAGYA leverages predictive analytics and machine learning to identify at-risk
          students, improve academic performance, and empower data-driven decision making
          in universities.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-wrap items-center justify-center gap-4 mb-12 animate-fade-up" style={{animationDelay:'0.2s'}}>
          <Link to="/dashboard" className="btn-primary text-base">
            🚀 Get Started
          </Link>
          <Link to="/dashboard" className="btn-outline text-base">
            📊 View Dashboard
          </Link>
        </div>

        {/* Trust line */}
        <p className="text-sm text-navy-600/60 tracking-wide animate-fade-up" style={{animationDelay:'0.3s'}}>
          Built for academic excellence &nbsp;·&nbsp; Data-driven &nbsp;·&nbsp; Scalable insights
        </p>

        {/* Stats row */}
        <div className="grid grid-cols-3 gap-6 max-w-xl mx-auto mt-16 animate-fade-up" style={{animationDelay:'0.4s'}}>
          {[['10,000+','Students Analyzed'],['8','ML Models'],['42.1%','At-Risk Detected']].map(([val,label])=>(
            <div key={label} className="text-center p-5 bg-white border border-gray-100 rounded-2xl shadow-sm">
              <div className="text-2xl font-bold text-navy-900">{val}</div>
              <div className="text-xs text-navy-600 mt-1">{label}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Scroll indicator */}
      <div className="absolute bottom-10 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 text-navy-600/40">
        <span className="text-xs tracking-widest uppercase">Scroll</span>
        <div className="w-px h-8 bg-gradient-to-b from-navy-600/40 to-transparent" />
      </div>
    </section>
  )
}
