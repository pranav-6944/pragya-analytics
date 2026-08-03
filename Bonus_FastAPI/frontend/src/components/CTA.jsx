import React from 'react'
import { Link } from 'react-router-dom'

export default function CTA() {
  return (
    <section className="section bg-gray-50 py-16 sm:py-24">
      <div className="container px-4 sm:px-6">
        <div className="relative bg-navy-900 rounded-2xl sm:rounded-3xl overflow-hidden px-6 py-12 sm:px-10 sm:py-20 text-center shadow-2xl">
          {/* Background glow blobs */}
          <div className="absolute top-0 left-1/4 w-48 sm:w-64 h-48 sm:h-64 bg-accent/20 rounded-full blur-3xl" />
          <div className="absolute bottom-0 right-1/4 w-48 sm:w-64 h-48 sm:h-64 bg-violet-500/10 rounded-full blur-3xl" />
          <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:32px_32px] sm:bg-[size:48px_48px]" />

          <div className="relative z-10">
            <div className="inline-flex items-center gap-2 bg-white/10 text-white/70 text-xs font-semibold uppercase tracking-widest px-4 sm:px-5 py-2 rounded-full mb-6 sm:mb-8">
              ✦ Get Started
            </div>
            <h2 className="text-2xl sm:text-4xl md:text-5xl font-bold text-white leading-tight mb-4 sm:mb-5">
              Ready to Transform<br />Academic Performance?
            </h2>
            <p className="text-white/60 text-sm sm:text-lg max-w-lg mx-auto mb-8 sm:mb-10 leading-relaxed px-2">
              Start using PRAGYA today and make smarter, data-driven decisions
              that improve student outcomes at scale.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-3 sm:gap-4 max-w-xs sm:max-w-none mx-auto">
              <Link to="/dashboard" className="btn-primary text-base w-full sm:w-auto justify-center">
                🚀 Get Started
              </Link>
              <Link to="/dashboard"
                className="inline-flex items-center justify-center gap-2 border-2 border-white/30 text-white font-semibold px-7 py-3.5 rounded-xl hover:border-white hover:bg-white/10 transition-all duration-200 w-full sm:w-auto">
                📊 Explore Dashboard
              </Link>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
