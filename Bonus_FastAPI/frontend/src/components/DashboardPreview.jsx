import React from 'react'
import { Link } from 'react-router-dom'

const highlights = [
  { icon: '📌', text: 'Real-time KPI tracking' },
  { icon: '📈', text: 'Interactive charts and visualizations' },
  { icon: '⚠️', text: 'Instant at-risk alerts' },
  { icon: '🔍', text: 'Deep student-level insights' },
]

export default function DashboardPreview() {
  return (
    <section className="section bg-white overflow-hidden py-16 sm:py-24">
      <div className="container px-4 sm:px-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-10 md:gap-16 items-center">
          {/* Left text */}
          <div>
            <div className="section-tag">✦ Dashboard Preview</div>
            <h2 className="section-title text-3xl sm:text-4xl">All Your Academic Insights<br className="hidden sm:inline" /> in One Place</h2>
            <p className="section-sub text-base sm:text-lg">
              PRAGYA provides a centralized dashboard to monitor student performance,
              track KPIs, and make informed academic decisions with ease.
            </p>
            <ul className="mt-6 sm:mt-8 space-y-3">
              {highlights.map((h, i) => (
                <li key={i} className="flex items-center gap-3 text-navy-700 text-sm font-medium">
                  <span className="w-8 h-8 bg-accent-light rounded-lg flex items-center justify-center text-base flex-shrink-0">
                    {h.icon}
                  </span>
                  {h.text}
                </li>
              ))}
            </ul>
            <div className="mt-8 sm:mt-10">
              <Link to="/dashboard" className="btn-primary w-full sm:w-auto justify-center">
                Explore Dashboard →
              </Link>
            </div>
          </div>

          {/* Right: mock dashboard UI */}
          <div className="relative">
            <div className="bg-white border border-gray-100 rounded-2xl sm:rounded-3xl shadow-2xl overflow-hidden">
              {/* Mock top bar */}
              <div className="bg-navy-900 px-4 sm:px-5 py-3 flex items-center gap-2">
                <div className="w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full bg-red-400" />
                <div className="w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full bg-yellow-400" />
                <div className="w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full bg-green-400" />
                <span className="ml-2 sm:ml-4 text-white/40 text-[10px] sm:text-xs font-mono truncate">pragya.local:8000</span>
              </div>
              {/* Mock sidebar + content */}
              <div className="flex">
                {/* Sidebar - hidden on tiny screens */}
                <div className="hidden sm:flex bg-navy-900 w-12 sm:w-14 py-6 flex-col items-center gap-4 sm:gap-5 flex-shrink-0">
                  {['□','◇','○','△','▽'].map((s,i)=>(
                    <div key={i} className={`w-7 h-7 sm:w-8 sm:h-8 rounded-lg flex items-center justify-center text-xs
                      ${i===0?'bg-accent text-white':'text-white/30 hover:text-white/60'}`}>
                      {s}
                    </div>
                  ))}
                </div>
                {/* Main mock content */}
                <div className="flex-1 bg-gray-50 p-3 sm:p-5 overflow-hidden">
                  {/* KPI row */}
                  <div className="grid grid-cols-3 gap-2 sm:gap-3 mb-3 sm:mb-4">
                    {[['10,000','Total Students','bg-white'],
                      ['2.04','Avg GPA','bg-white'],
                      ['4,207','At-Risk','bg-red-50']].map(([v,l,bg],i)=>(
                      <div key={i} className={`${bg} rounded-lg sm:rounded-xl p-2 sm:p-3 border border-gray-100`}>
                        <div className="text-[10px] sm:text-xs text-gray-400 mb-0.5 sm:mb-1 truncate">{l}</div>
                        <div className="font-bold text-navy-900 text-sm sm:text-lg truncate">{v}</div>
                      </div>
                    ))}
                  </div>
                  {/* Chart mock */}
                  <div className="bg-white rounded-lg sm:rounded-xl border border-gray-100 p-3 sm:p-4 mb-3">
                    <div className="text-[10px] sm:text-xs font-medium text-gray-400 mb-2 sm:mb-3">GPA Distribution</div>
                    <div className="flex items-end gap-1 h-12 sm:h-16">
                      {[20,35,55,80,100,85,60,40,25,15,8].map((h,i)=>(
                        <div key={i} className="flex-1 rounded-sm"
                             style={{height:`${h}%`, background: i===4?'#6366F1':'#E2E8F0'}} />
                      ))}
                    </div>
                  </div>
                  {/* Donut mock */}
                  <div className="bg-white rounded-lg sm:rounded-xl border border-gray-100 p-3 sm:p-4 flex items-center gap-3 sm:gap-4">
                    <div className="relative w-12 h-12 sm:w-16 sm:h-16 flex-shrink-0">
                      <svg viewBox="0 0 36 36" className="w-full h-full -rotate-90">
                        <circle cx="18" cy="18" r="14" fill="none" stroke="#EEF2FF" strokeWidth="4"/>
                        <circle cx="18" cy="18" r="14" fill="none" stroke="#6366F1" strokeWidth="4"
                          strokeDasharray="55 45" strokeLinecap="round"/>
                        <circle cx="18" cy="18" r="14" fill="none" stroke="#10B981" strokeWidth="4"
                          strokeDasharray="30 70" strokeDashoffset="-55" strokeLinecap="round"/>
                        <circle cx="18" cy="18" r="14" fill="none" stroke="#EF4444" strokeWidth="4"
                          strokeDasharray="15 85" strokeDashoffset="-85" strokeLinecap="round"/>
                      </svg>
                    </div>
                    <div className="space-y-1 flex-1">
                      {[['Pass','#6366F1','55%'],['Distinction','#10B981','30%'],['Fail','#EF4444','15%']].map(([l,c,p])=>(
                        <div key={l} className="flex items-center gap-1.5 sm:gap-2">
                          <div className="w-2 h-2 rounded-sm flex-shrink-0" style={{background:c}} />
                          <span className="text-[10px] sm:text-xs text-gray-500 truncate">{l}</span>
                          <span className="text-[10px] sm:text-xs font-semibold ml-auto text-navy-900">{p}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
            {/* Decorative glow */}
            <div className="absolute -inset-4 bg-accent/5 rounded-3xl blur-2xl -z-10" />
          </div>
        </div>
      </div>
    </section>
  )
}
