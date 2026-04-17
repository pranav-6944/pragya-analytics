import React, { useState } from 'react'
import { Link } from 'react-router-dom'

const steps = [
  {
    num: '01', icon: '🚀', title: 'Start the Server',
    content: (
      <div>
        <p className="text-slate-600 mb-4 leading-relaxed">
          PRAGYA runs on a <strong>FastAPI</strong> backend. Open a terminal,
          navigate to the project folder, and run:
        </p>
        <div className="bg-slate-900 text-emerald-400 rounded-xl px-5 py-4 font-mono text-sm leading-relaxed">
          <span className="text-slate-500">cd </span>Bonus_FastAPI<br/>
          <span className="text-slate-500"># activate your venv first, then:</span><br/>
          ..\venv\Scripts\uvicorn.exe main:app --host 127.0.0.1 --port 8000
        </div>
        <p className="text-sm text-slate-500 mt-3">
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
        <p className="text-slate-600 leading-relaxed">
          <strong>PRAGYA</strong> (meaning <em>wisdom</em> in Sanskrit) is a full-stack
          <strong> University Academic Analytics & Predictive Intelligence System</strong>.
          It was built as the Bonus Deployment for the University Analytics Engineering assignment.
        </p>
        <div className="grid grid-cols-2 gap-4">
          {[
            ['📊','It analyses data from 10,000+ students across courses, grades, attendance, and enrollments.'],
            ['🧠','It trains ML models (Random Forest + ANN) to predict academic outcomes and dropout risk.'],
            ['🗂️','It segments students into 4 clusters using K-Means to identify high-risk groups early.'],
            ['📈','It surfaces department and course-level bottlenecks to help academic administrators act.'],
          ].map(([icon,text],i)=>(
            <div key={i} className="flex gap-3 p-4 bg-indigo-50/50 rounded-xl text-sm text-slate-700 leading-relaxed">
              <span className="text-xl flex-shrink-0">{icon}</span>{text}
            </div>
          ))}
        </div>
      </div>
    )
  },
  {
    num: '03', icon: '⊞', title: 'Overview Dashboard',
    content: (
      <div className="space-y-3 text-slate-600 text-sm leading-relaxed">
        <p>The <strong>Overview</strong> page shows the full academic picture at a glance:</p>
        <ul className="space-y-2 pl-4">
          {[
            ['Total Students','Total number of students in the dataset (10,000).'],
            ['Avg GPA','Mean GPA across all students on a 0–4.0 scale.'],
            ['At-Risk Count','Students with GPA < 1.5 OR attendance < 50% — flagged for intervention.'],
            ['Distinctions','Students who scored Internal Marks ≥ 75 (GPA ≥ 3.0).'],
            ['Result Doughnut','Proportion of Pass / Fail / Distinction in the cohort.'],
            ['GPA Histogram','Distribution of GPA values — useful to see if the class is skewed.'],
            ['Scatter Plot','Each dot = one student. X = Attendance %, Y = GPA. See the positive correlation.'],
          ].map(([k,v])=>(
            <li key={k} className="flex gap-2">
              <span className="text-indigo-500 font-medium w-36 flex-shrink-0">{k}</span>
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
      <div className="space-y-3 text-slate-600 text-sm leading-relaxed">
        <p>The <strong>Predict</strong> page lets you model any student in real-time using 5 sliders:</p>
        <table className="w-full text-sm border-collapse">
          <thead>
            <tr className="border-b border-gray-100">
              <th className="text-left pb-2 text-gray-400 font-semibold text-xs uppercase">Input</th>
              <th className="text-left pb-2 text-gray-400 font-semibold text-xs uppercase">What it means</th>
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
                <td className="py-2.5 pr-4 font-medium text-indigo-600 text-xs">{k}</td>
                <td className="py-2.5 text-slate-600">{v}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 text-amber-800 text-sm mt-2">
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
      <div className="space-y-3 text-sm text-slate-600 leading-relaxed">
        <p><strong>Departments</strong> — sorted by average GPA:</p>
        <ul className="space-y-1 pl-4 list-disc">
          <li><span className="text-emerald-600 font-semibold">Green bars</span> = GPA ≥ 2.05 (high performing)</li>
          <li><span className="text-indigo-500 font-semibold">Indigo bars</span> = GPA 1.95–2.05 (average)</li>
          <li><span className="text-red-500 font-semibold">Red bars</span> = GPA &lt; 1.95 (needs support)</li>
        </ul>
        <p className="mt-3"><strong>Course Difficulty</strong> formula:</p>
        <div className="bg-slate-100 rounded-xl px-5 py-3 font-mono text-sm text-slate-700">
          difficulty = (1 − pass_rate) × credits
        </div>
        <p>A high difficulty score means the course has a low pass rate AND high credit weight — a major academic bottleneck requiring curriculum review or additional tutoring.</p>
      </div>
    )
  },
  {
    num: '06', icon: '◑', title: 'Student Segments',
    content: (
      <div className="space-y-4 text-sm text-slate-600 leading-relaxed">
        <p>K-Means clustering groups students into <strong>4 segments</strong> based on GPA, attendance, course load, and pass rate:</p>
        <div className="space-y-3">
          {[
            ['#10B981','High Achievers','High GPA + High Attendance. Star performers. Encourage advanced research.'],
            ['#6366F1','Average Performers','On track but could do better. Benefit from mentoring programs.'],
            ['#F59E0B','Struggling Students','Below-average GPA + inconsistent attendance. Need academic counselling.'],
            ['#EF4444','At-Risk Students','Low GPA + Low Attendance. Immediate intervention required. Dropout risk is highest.'],
          ].map(([color,name,desc])=>(
            <div key={name} className="flex gap-3 items-start p-4 rounded-xl border border-gray-100">
              <div className="w-3 h-3 rounded-full flex-shrink-0 mt-1" style={{background:color}} />
              <div>
                <div className="font-semibold text-slate-800 text-sm">{name}</div>
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
      <div style={{background:'white', borderBottom:'1px solid #E2E8F0', padding:'0 40px',
                   display:'flex', alignItems:'center', gap:16, height:56, position:'sticky', top:0, zIndex:10}}>
        <Link to="/" style={{display:'flex', alignItems:'center', gap:8, textDecoration:'none'}}>
          <div style={{width:28, height:28, background:'#6366F1', borderRadius:7,
                       display:'flex', alignItems:'center', justifyContent:'center',
                       color:'white', fontWeight:700, fontSize:12}}>P</div>
          <span style={{fontWeight:700, fontSize:14, color:'#0F172A', letterSpacing:'-0.02em'}}>PRAGYA</span>
        </Link>
        <span style={{color:'#CBD5E1', fontSize:14}}>/</span>
        <span style={{color:'#64748B', fontSize:14}}>User Guide</span>
        <div style={{marginLeft:'auto', display:'flex', gap:12}}>
          <Link to="/" style={{fontSize:13, color:'#64748B', textDecoration:'none'}}>Home</Link>
          <Link to="/dashboard"
            style={{fontSize:13, color:'white', background:'#6366F1', padding:'6px 16px',
                    borderRadius:8, textDecoration:'none', fontWeight:600}}>
            Open Dashboard →
          </Link>
        </div>
      </div>

      <div style={{maxWidth:860, margin:'0 auto', padding:'48px 24px'}}>
        {/* Hero */}
        <div style={{marginBottom:48, textAlign:'center'}}>
          <div style={{display:'inline-flex', alignItems:'center', gap:8, background:'#EEF2FF',
                       color:'#6366F1', fontSize:12, fontWeight:600, letterSpacing:'0.1em',
                       padding:'6px 16px', borderRadius:999, textTransform:'uppercase', marginBottom:20}}>
            📖 User Guide
          </div>
          <h1 style={{fontSize:40, fontWeight:800, color:'#0F172A', lineHeight:1.1, letterSpacing:'-0.03em', marginBottom:14}}>
            How to Use PRAGYA
          </h1>
          <p style={{fontSize:16, color:'#64748B', maxWidth:560, margin:'0 auto', lineHeight:1.7}}>
            Everything you need to know — from starting the server to reading
            every chart in the dashboard.
          </p>
        </div>

        {/* Quick links */}
        <div style={{display:'grid', gridTemplateColumns:'repeat(3, 1fr)', gap:12, marginBottom:40}}>
          {steps.map((s,i)=>(
            <button key={i} onClick={()=>setOpen(i)}
              style={{
                display:'flex', alignItems:'center', gap:10, padding:'14px 16px',
                background: open===i ? '#EEF2FF' : 'white',
                border: `1.5px solid ${open===i?'#6366F1':'#E2E8F0'}`,
                borderRadius:12, cursor:'pointer', textAlign:'left', transition:'all 0.15s'
              }}>
              <span style={{fontSize:20}}>{s.icon}</span>
              <div>
                <div style={{fontSize:10, color:'#6366F1', fontWeight:700, letterSpacing:'0.08em'}}>{s.num}</div>
                <div style={{fontSize:12, fontWeight:600, color:'#0F172A', marginTop:1}}>{s.title}</div>
              </div>
            </button>
          ))}
        </div>

        {/* Accordion */}
        <div style={{display:'flex', flexDirection:'column', gap:12}}>
          {steps.map((s,i)=>(
            <div key={i}
              style={{background:'white', border:`1.5px solid ${open===i?'#6366F1':'#E2E8F0'}`,
                      borderRadius:16, overflow:'hidden', transition:'all 0.2s'}}>
              <button onClick={()=>setOpen(open===i?-1:i)}
                style={{width:'100%', display:'flex', alignItems:'center', gap:14, padding:'18px 22px',
                        background:'none', border:'none', cursor:'pointer', textAlign:'left'}}>
                <span style={{fontSize:24}}>{s.icon}</span>
                <div style={{flex:1}}>
                  <span style={{fontSize:11, color:'#6366F1', fontWeight:700, letterSpacing:'0.1em'}}>{s.num}</span>
                  <div style={{fontSize:15, fontWeight:700, color:'#0F172A', marginTop:1}}>{s.title}</div>
                </div>
                <span style={{color:'#94A3B8', fontSize:20, transition:'transform 0.2s',
                              transform: open===i?'rotate(45deg)':'rotate(0deg)'}}>+</span>
              </button>
              {open===i && (
                <div style={{padding:'4px 22px 22px 60px', borderTop:'1px solid #F1F5F9'}}>
                  {s.content}
                </div>
              )}
            </div>
          ))}
        </div>

        {/* CTA */}
        <div style={{marginTop:48, background:'#0F172A', borderRadius:20, padding:'36px 40px', textAlign:'center'}}>
          <div style={{fontSize:22, fontWeight:800, color:'white', marginBottom:10}}>
            Ready to explore?
          </div>
          <p style={{color:'rgba(255,255,255,0.5)', fontSize:14, marginBottom:24}}>
            Open the live dashboard and start analysing your academic data.
          </p>
          <Link to="/dashboard"
            style={{display:'inline-flex', alignItems:'center', gap:8, background:'#6366F1',
                    color:'white', fontWeight:600, padding:'12px 28px', borderRadius:10,
                    textDecoration:'none', fontSize:14}}>
            📊 Open Dashboard →
          </Link>
        </div>
      </div>
    </div>
  )
}
