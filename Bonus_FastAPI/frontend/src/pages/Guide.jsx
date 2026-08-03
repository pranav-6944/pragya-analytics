import React, { useState } from 'react'
import { Link } from 'react-router-dom'

const steps = [
  {
    num: '01', icon: '🚀', title: 'Start the Server',
    content: (
      <div>
        <p className="text-slate-600 mb-4 leading-relaxed text-xs sm:text-sm">
          PRAGYA runs on a <strong>FastAPI</strong> backend. Open a terminal,
          navigate to the project folder, and run:
        </p>
        <div className="bg-slate-900 text-emerald-400 rounded-xl px-4 py-3 sm:px-5 sm:py-4 font-mono text-xs sm:text-sm leading-relaxed overflow-x-auto">
          <span className="text-slate-500">cd </span>Bonus_FastAPI<br/>
          <span className="text-slate-500"># activate your venv first, then:</span><br/>
          ..\venv\Scripts\uvicorn.exe main:app --host 127.0.0.1 --port 8000
        </div>
        <p className="text-xs sm:text-sm text-slate-500 mt-3">
          Once you see <code className="bg-slate-100 px-1.5 py-0.5 rounded text-xs">Application startup complete</code>, open{' '}
          <a href="http://127.0.0.1:8000" target="_blank" rel="noreferrer"
             className="text-indigo-600 underline">http://127.0.0.1:8000</a>
        </p>
      </div>
    )
  },
  {
    num: '02', icon: '🎓', title: 'What is PRAGYA?',
    content: (
      <div className="space-y-4">
        <p className="text-slate-600 leading-relaxed text-xs sm:text-sm">
          <strong>PRAGYA</strong> (meaning <em>wisdom</em> in Sanskrit) is a full-stack
          <strong> University Academic Analytics & Predictive Intelligence System</strong>.
          It was built as the Bonus Deployment for the University Analytics Engineering assignment.
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
          {[
            ['📊','It analyses data from 10,000+ students across courses, grades, attendance, and enrollments.'],
            ['🧠','It trains ML models (Random Forest + ANN) to predict academic outcomes and dropout risk.'],
            ['🗂️','It segments students into 4 clusters using K-Means to identify high-risk groups early.'],
            ['📈','It surfaces department and course-level bottlenecks to help academic administrators act.'],
          ].map(([icon,text],i)=>(
            <div key={i} className="flex gap-3 p-3.5 sm:p-4 bg-indigo-50/50 rounded-xl text-xs sm:text-sm text-slate-700 leading-relaxed">
              <span className="text-lg sm:text-xl flex-shrink-0">{icon}</span>
              <span>{text}</span>
            </div>
          ))}
        </div>
      </div>
    )
  },
  {
    num: '03', icon: '⊞', title: 'Overview Dashboard',
    content: (
      <div className="space-y-3 text-slate-600 text-xs sm:text-sm leading-relaxed">
        <p>The <strong>Overview</strong> page shows the full academic picture at a glance:</p>
        <ul className="space-y-2.5 sm:space-y-2">
          {[
            ['Total Students','Total number of students in the dataset (10,000).'],
            ['Avg GPA','Mean GPA across all students on a 0–4.0 scale.'],
            ['At-Risk Count','Students with GPA < 1.5 OR attendance < 50% — flagged for intervention.'],
            ['Distinctions','Students who scored Internal Marks ≥ 75 (GPA ≥ 3.0).'],
            ['Result Doughnut','Proportion of Pass / Fail / Distinction in the cohort.'],
            ['GPA Histogram','Distribution of GPA values — useful to see if the class is skewed.'],
            ['Scatter Plot','Each dot = one student. X = Attendance %, Y = GPA. See the positive correlation.'],
          ].map(([k,v])=>(
            <li key={k} className="flex flex-col sm:flex-row sm:gap-2">
              <span className="text-indigo-600 font-medium w-full sm:w-36 flex-shrink-0">{k}:</span>
              <span>{v}</span>
            </li>
          ))}
        </ul>
      </div>
    )
  },
  {
    num: '04', icon: '◈', title: 'Predict Student Outcome',
    content: (
      <div className="space-y-3 text-slate-600 text-xs sm:text-sm leading-relaxed">
        <p>The <strong>Predict</strong> page lets you model any student in real-time using 5 sliders:</p>
        <div className="overflow-x-auto">
          <table className="w-full text-xs sm:text-sm border-collapse">
            <thead>
              <tr className="border-b border-gray-100">
                <th className="text-left pb-2 text-gray-400 font-semibold text-[10px] sm:text-xs uppercase pr-4">Input</th>
                <th className="text-left pb-2 text-gray-400 font-semibold text-[10px] sm:text-xs uppercase">What it means</th>
              </tr>
            </thead>
            <tbody>
              {[
                ['Attendance %','% of classes attended (0–100)'],
                ['Internal Marks','Score out of 100 — maps to GPA as GPA = Marks/25'],
                ['Course Load','Total credits enrolled in this semester'],
                ['Pass Rate','Fraction of past courses passed (0.0–1.0)'],
                ['Faculty Interactions','Number of unique faculty this student has interacted with'],
              ].map(([k,v])=>(
                <tr key={k} className="border-b border-gray-50">
                  <td className="py-2.5 pr-4 font-medium text-indigo-600 text-xs flex-shrink-0 whitespace-nowrap">{k}</td>
                  <td className="py-2.5 text-slate-600">{v}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="bg-amber-50 border border-amber-200 rounded-xl p-3.5 sm:p-4 text-amber-800 text-xs sm:text-sm mt-2">
          <strong>📌 How to read the Risk Level:</strong><br/>
          <span className="text-red-600 font-semibold">High (&gt;60%)</span> → Immediate action needed &nbsp;·&nbsp;
          <span className="text-amber-600 font-semibold">Medium (30–60%)</span> → Monitor weekly &nbsp;·&nbsp;
          <span className="text-emerald-600 font-semibold">Low (&lt;30%)</span> → On track
        </div>
      </div>
    )
  },
  {
    num: '05', icon: '⬡', title: 'Departments & Courses',
    content: (
      <div className="space-y-3 text-xs sm:text-sm text-slate-600 leading-relaxed">
        <p><strong>Departments</strong> — sorted by average GPA:</p>
        <ul className="space-y-1 pl-4 list-disc">
          <li><span className="text-emerald-600 font-semibold">Green bars</span> = GPA ≥ 2.05 (high performing)</li>
          <li><span className="text-indigo-500 font-semibold">Indigo bars</span> = GPA 1.95–2.05 (average)</li>
          <li><span className="text-red-500 font-semibold">Red bars</span> = GPA &lt; 1.95 (needs support)</li>
        </ul>
        <p className="mt-3"><strong>Course Difficulty</strong> formula:</p>
        <div className="bg-slate-100 rounded-xl px-4 py-2.5 sm:px-5 sm:py-3 font-mono text-xs sm:text-sm text-slate-700 overflow-x-auto">
          difficulty = (1 − pass_rate) × credits
        </div>
        <p>A high difficulty score means the course has a low pass rate AND high credit weight — a major academic bottleneck requiring curriculum review or additional tutoring.</p>
      </div>
    )
  },
  {
    num: '06', icon: '◑', title: 'Student Segments',
    content: (
      <div className="space-y-4 text-xs sm:text-sm text-slate-600 leading-relaxed">
        <p>K-Means clustering groups students into <strong>4 segments</strong> based on GPA, attendance, course load, and pass rate:</p>
        <div className="space-y-3">
          {[
            ['#10B981','High Achievers','High GPA + High Attendance. Star performers. Encourage advanced research.'],
            ['#6366F1','Average Performers','On track but could do better. Benefit from mentoring programs.'],
            ['#F59E0B','Struggling Students','Below-average GPA + inconsistent attendance. Need academic counselling.'],
            ['#EF4444','At-Risk Students','Low GPA + Low Attendance. Immediate intervention required. Dropout risk is highest.'],
          ].map(([color,name,desc])=>(
            <div key={name} className="flex gap-3 items-start p-3.5 sm:p-4 rounded-xl border border-gray-100">
              <div className="w-3 h-3 rounded-full flex-shrink-0 mt-1" style={{background:color}} />
              <div>
                <div className="font-semibold text-slate-800 text-xs sm:text-sm">{name}</div>
                <div className="text-slate-500 text-xs mt-0.5 leading-relaxed">{desc}</div>
              </div>
            </div>
          ))}
        </div>
        <p>The <strong>Radar chart</strong> compares all 4 groups across 4 dimensions simultaneously — a quick visual diagnostic of where each group stands.</p>
      </div>
    )
  },
]

export default function Guide() {
  const [open, setOpen] = useState(0)

  return (
    <div style={{minHeight:'100vh', background:'#F8FAFC', fontFamily:'Inter,sans-serif'}}>
      {/* Top nav */}
      <div className="bg-white border-b border-gray-200 px-4 sm:px-10 flex items-center justify-between h-14 sticky top-0 z-10 shadow-sm">
        <div className="flex items-center gap-2 sm:gap-4 truncate">
          <Link to="/" className="flex items-center gap-2 text-decoration-none">
            <img src="/logo.png" alt="PRAGYA Logo" className="w-8 h-8 object-contain" />
            <span className="font-bold text-sm text-slate-900 tracking-tight">PRAGYA</span>
          </Link>
          <span className="text-slate-300 text-sm">/</span>
          <span className="text-slate-500 text-xs sm:text-sm truncate">User Guide</span>
        </div>
        <div className="flex items-center gap-2 sm:gap-4 flex-shrink-0">
          <Link to="/" className="text-xs sm:text-sm text-slate-600 hover:text-slate-900 px-2 py-1">Home</Link>
          <Link to="/dashboard"
                className="text-xs sm:text-sm text-white bg-indigo-600 hover:bg-indigo-700 px-3 py-1.5 sm:px-4 sm:py-2 rounded-lg font-semibold transition-all">
            Dashboard →
          </Link>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8 sm:py-12">
        {/* Hero */}
        <div className="mb-8 sm:mb-12 text-center">
          <div className="inline-flex items-center gap-2 bg-indigo-50 text-indigo-600 text-xs font-semibold tracking-widest px-4 py-1.5 rounded-full uppercase mb-4 sm:mb-5">
            📖 User Guide
          </div>
          <h1 className="text-2xl sm:text-4xl font-extrabold text-slate-900 leading-tight tracking-tight mb-3 sm:mb-4">
            How to Use PRAGYA
          </h1>
          <p className="text-sm sm:text-base text-slate-500 max-w-xl mx-auto leading-relaxed">
            Everything you need to know — from starting the server to reading
            every chart in the dashboard.
          </p>
        </div>

        {/* Quick links */}
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5 sm:gap-3 mb-8 sm:mb-10">
          {steps.map((s,i)=>(
            <button key={i} onClick={()=>setOpen(i)}
              className={`flex items-center gap-2.5 p-3 sm:p-4 rounded-xl border text-left transition-all cursor-pointer ${
                open===i ? 'bg-indigo-50/80 border-indigo-500 shadow-sm' : 'bg-white border-slate-200 hover:border-indigo-300'
              }`}>
              <span className="text-lg sm:text-xl flex-shrink-0">{s.icon}</span>
              <div className="truncate">
                <div className="text-[10px] text-indigo-600 font-bold tracking-wider">{s.num}</div>
                <div className="text-xs font-semibold text-slate-900 truncate mt-0.5">{s.title}</div>
              </div>
            </button>
          ))}
        </div>

        {/* Accordion */}
        <div className="flex flex-col gap-3">
          {steps.map((s,i)=>(
            <div key={i}
              className={`bg-white border rounded-2xl overflow-hidden transition-all duration-200 ${
                open===i ? 'border-indigo-500 shadow-md' : 'border-slate-200'
              }`}>
              <button onClick={()=>setOpen(open===i?-1:i)}
                className="w-full flex items-center gap-3 sm:gap-4 p-4 sm:px-6 sm:py-5 bg-none border-none cursor-pointer text-left">
                <span className="text-xl sm:text-2xl flex-shrink-0">{s.icon}</span>
                <div className="flex-1 min-w-0">
                  <span className="text-[10px] sm:text-xs text-indigo-600 font-bold tracking-widest">{s.num}</span>
                  <div className="text-sm sm:text-base font-bold text-slate-900 truncate">{s.title}</div>
                </div>
                <span className={`text-slate-400 text-xl transition-transform duration-200 ${open===i?'rotate-45':''}`}>+</span>
              </button>
              {open===i && (
                <div className="px-4 pb-4 pt-1 sm:px-6 sm:pb-6 border-t border-slate-100">
                  {s.content}
                </div>
              )}
            </div>
          ))}
        </div>

        {/* CTA */}
        <div className="mt-10 sm:mt-14 bg-slate-900 rounded-2xl p-6 sm:p-10 text-center text-white">
          <div className="text-xl sm:text-2xl font-extrabold mb-2">
            Ready to explore?
          </div>
          <p className="text-white/60 text-xs sm:text-sm mb-6 max-w-md mx-auto">
            Open the live dashboard and start analysing your academic data.
          </p>
          <Link to="/dashboard"
            className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold px-6 py-3 rounded-xl transition-all text-xs sm:text-sm">
            📊 Open Dashboard →
          </Link>
        </div>
      </div>
    </div>
  )
}
