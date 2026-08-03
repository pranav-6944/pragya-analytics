import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import {
  Chart as ChartJS, CategoryScale, LinearScale, BarElement, PointElement,
  ArcElement, RadialLinearScale, Tooltip, Legend
} from 'chart.js'
import { Bar, Doughnut, Scatter, Radar } from 'react-chartjs-2'

ChartJS.register(CategoryScale, LinearScale, BarElement, PointElement,
  ArcElement, RadialLinearScale, Tooltip, Legend)

// Defaults
ChartJS.defaults.font.family = 'Inter, sans-serif'
ChartJS.defaults.font.size   = 11
ChartJS.defaults.color       = '#64748B'
ChartJS.defaults.plugins.tooltip.backgroundColor = '#0F172A'
ChartJS.defaults.plugins.tooltip.padding         = 10
ChartJS.defaults.plugins.tooltip.cornerRadius    = 8
ChartJS.defaults.plugins.legend.labels.boxWidth  = 10
ChartJS.defaults.plugins.legend.labels.padding   = 12

// Use relative URLs – works both in dev (proxied) and production (same server)
const API = ''

const ACCENT = '#6366F1'
const SEG_COLORS = {
  'High Achievers'      : '#10B981',
  'Average Performers'  : '#6366F1',
  'Struggling Students' : '#F59E0B',
  'At-Risk Students'    : '#EF4444',
}

// Static class maps so Tailwind JIT includes them
const RESULT_BADGES = {
  Distinction : { wrap:'bg-emerald-50 text-emerald-700 border border-emerald-200', icon:'🏆' },
  Pass        : { wrap:'bg-blue-50 text-blue-700 border border-blue-200',          icon:'✅' },
  Fail        : { wrap:'bg-red-50 text-red-700 border border-red-200',             icon:'⚠️' },
}
const RISK_BAR_COLORS  = { High:'bg-red-500',    Medium:'bg-amber-500',    Low:'bg-emerald-500' }
const RISK_TEXT_COLORS = { High:'text-red-600',  Medium:'text-amber-600',  Low:'text-emerald-600' }
const RISK_REC = {
  High   : { cls:'bg-red-50 border-red-400 text-red-900',         msg:'🚨 High dropout risk detected. Immediate academic counselling, attendance monitoring, and tutoring strongly recommended.' },
  Medium : { cls:'bg-blue-50 border-blue-400 text-blue-900',      msg:'📌 Moderate risk. Monitor weekly and provide proactive academic support before the next exam cycle.' },
  Low    : { cls:'bg-emerald-50 border-emerald-400 text-emerald-900', msg:'✅ Student is on a strong track. Encourage advanced coursework and research opportunities.' },
}

// ── KPI Card ──────────────────────────────────────────────────────────────────
function KPI({ label, value, sub, danger }) {
  return (
    <div className={`rounded-2xl border p-4 sm:p-5 transition-all hover:shadow-md hover:-translate-y-0.5
      ${danger ? 'bg-red-50 border-red-100' : 'bg-white border-gray-100'}`}>
      <p className="text-[10px] sm:text-xs font-semibold text-gray-400 uppercase tracking-widest mb-1.5 sm:mb-2 truncate">{label}</p>
      <p className={`text-2xl sm:text-3xl font-bold mb-1 truncate ${danger ? 'text-red-600' : 'text-slate-900'}`}>{value ?? '—'}</p>
      {sub && <p className="text-[10px] sm:text-xs text-gray-400 truncate">{sub}</p>}
    </div>
  )
}

// ── Card wrapper ──────────────────────────────────────────────────────────────
function Card({ title, sub, badge, children, className='' }) {
  return (
    <div className={`bg-white border border-gray-100 rounded-2xl p-4 sm:p-6 shadow-sm overflow-hidden ${className}`}>
      <div className="flex items-start justify-between mb-4 sm:mb-5 gap-2">
        <div className="min-w-0 flex-1">
          <h3 className="font-semibold text-slate-900 text-xs sm:text-sm truncate">{title}</h3>
          {sub && <p className="text-[11px] sm:text-xs text-gray-400 mt-0.5 truncate">{sub}</p>}
        </div>
        {badge && <span className="text-[10px] sm:text-xs bg-indigo-50 text-indigo-600 font-medium px-2.5 py-0.5 sm:py-1 rounded-full flex-shrink-0">{badge}</span>}
      </div>
      {children}
    </div>
  )
}

// ── Predict Panel ─────────────────────────────────────────────────────────────
function PredictPanel() {
  const [vals, setVals]     = useState({ attendance:75, marks:60, load:20, pass_rate:0.8, faculty:5 })
  const [result, setResult] = useState(null)
  const [loading, setLoading]= useState(false)
  const [error, setError]   = useState(null)

  const sliders = [
    { key:'attendance', label:'Attendance %',         min:0,   max:100, step:0.5,  fmt: v=>`${v}%` },
    { key:'marks',      label:'Internal Marks (0–100)',min:0,  max:100, step:0.5,  fmt: v=>v },
    { key:'load',       label:'Course Load (credits)', min:5,  max:60,  step:1,    fmt: v=>v },
    { key:'pass_rate',  label:'Pass Rate (0–1)',        min:0,  max:1,   step:0.01, fmt: v=>parseFloat(v).toFixed(2) },
    { key:'faculty',    label:'Faculty Interactions',  min:1,   max:20,  step:1,    fmt: v=>v },
  ]

  const predict = async () => {
    setLoading(true); setError(null)
    try {
      const r = await fetch(`${API}/api/predict`, {
        method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify(vals)
      })
      if (!r.ok) throw new Error(`HTTP ${r.status}`)
      setResult(await r.json())
    } catch(e) { setError(e.message) }
    finally { setLoading(false) }
  }

  const rb = result ? RESULT_BADGES[result.result] : null
  const riskBarColor  = result ? RISK_BAR_COLORS[result.risk_level]  : 'bg-gray-300'
  const riskTextColor = result ? RISK_TEXT_COLORS[result.risk_level] : 'text-gray-500'
  const rec           = result ? RISK_REC[result.risk_level] : null
  const probColors    = { Distinction:'#10B981', Pass:'#6366F1', Fail:'#EF4444' }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 sm:gap-6">
      {/* Form */}
      <Card title="Student Profile" sub="Adjust sliders to model a student">
        <div className="space-y-4 sm:space-y-5">
          {sliders.map(s => (
            <div key={s.key}>
              <div className="flex justify-between mb-1.5">
                <label className="text-xs sm:text-sm font-medium text-slate-700">{s.label}</label>
                <span className="text-xs sm:text-sm font-semibold text-indigo-500 font-mono">{s.fmt(vals[s.key])}</span>
              </div>
              <input type="range" min={s.min} max={s.max} step={s.step} value={vals[s.key]}
                className="w-full h-2 rounded-full appearance-none cursor-pointer touch-pan-x"
                style={{accentColor:'#6366F1'}}
                onChange={e => setVals(v => ({...v, [s.key]: parseFloat(e.target.value)}))} />
            </div>
          ))}
        </div>
        {error && <p className="mt-4 text-xs sm:text-sm text-red-500 bg-red-50 px-4 py-2.5 rounded-lg">{error}</p>}
        <button onClick={predict} disabled={loading}
          style={{background:'#6366F1'}}
          className="mt-6 w-full py-3 sm:py-3.5 text-white text-xs sm:text-sm font-semibold rounded-xl
                     hover:opacity-90 transition-opacity shadow-lg disabled:opacity-50 active:scale-[0.98]">
          {loading ? '⏳ Predicting…' : '🚀 Predict Outcome'}
        </button>
      </Card>

      {/* Result */}
      <Card title="Prediction Result" sub="Machine learning output">
        {!result ? (
          <div className="flex flex-col items-center justify-center min-h-[220px] sm:h-72 border-2 border-dashed border-gray-100 rounded-xl gap-3 p-4">
            <span className="text-4xl sm:text-5xl">🔮</span>
            <p className="text-xs sm:text-sm text-gray-400 text-center">Set values and click Predict</p>
          </div>
        ) : (
          <div className="space-y-4 sm:space-y-5">
            {/* Result badge */}
            <div className={`inline-flex items-center gap-2.5 sm:gap-3 px-4 py-2.5 sm:px-5 sm:py-3 rounded-xl font-bold text-lg sm:text-xl ${rb.wrap}`}>
              <span>{rb.icon}</span> <span>{result.result}</span>
              <span className="text-xs sm:text-sm font-normal opacity-70 ml-auto">GPA ≈ {result.gpa_estimate}</span>
            </div>

            {/* Risk bar */}
            <div>
              <div className="flex justify-between text-xs sm:text-sm mb-2">
                <span className="font-medium text-slate-700">
                  Dropout Risk —{' '}
                  <span className={riskTextColor}>{result.risk_level}</span>
                </span>
                <span className="font-mono text-gray-400">{(result.dropout_prob*100).toFixed(1)}%</span>
              </div>
              <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                <div className={`h-full rounded-full transition-all duration-700 ${riskBarColor}`}
                     style={{width:`${result.dropout_prob*100}%`}} />
              </div>
            </div>

            {/* Prob bars */}
            <div className="space-y-2.5 sm:space-y-3">
              {Object.entries(result.probabilities).map(([cls, p]) => (
                <div key={cls} className="flex items-center gap-2.5 sm:gap-3">
                  <span className="text-xs font-medium text-gray-500 w-20 sm:w-24 flex-shrink-0 truncate">{cls}</span>
                  <div className="flex-1 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                    <div className="h-full rounded-full transition-all duration-700"
                         style={{width:`${p*100}%`, background: probColors[cls]}} />
                  </div>
                  <span className="text-xs font-mono text-gray-400 w-10 text-right">{(p*100).toFixed(1)}%</span>
                </div>
              ))}
            </div>

            {/* Recommendation */}
            {rec && (
              <div className={`p-3.5 sm:p-4 rounded-xl text-xs sm:text-sm leading-relaxed border-l-4 ${rec.cls}`}>
                {rec.msg}
              </div>
            )}
          </div>
        )}
      </Card>
    </div>
  )
}

// ── Segments section ──────────────────────────────────────────────────────────
function SegmentsSection({ segData }) {
  const segs = segData?.segments
  if (!Array.isArray(segs) || segs.length === 0) {
    return (
      <div className="py-16 text-center text-slate-400">
        <p className="text-sm">Segment data is not available yet. Try refreshing in a moment.</p>
      </div>
    )
  }
  const gpas  = segData.avg_gpa      || segs.map(() => 0)
  const atts  = segData.avg_att       || segs.map(() => 0)
  const loads = segData.avg_load      || segs.map(() => 0)
  const prs   = segData.avg_passrate  || segs.map(() => 0)
  const cnts  = segData.counts        || segs.map(() => 0)
  const colors = Object.values(SEG_COLORS)

  return (
    <div>
      <div className="mb-6 sm:mb-8">
        <h1 className="text-xl sm:text-2xl font-bold text-slate-900">Student Segments</h1>
        <p className="text-xs sm:text-sm text-gray-400 mt-1">K-Means clustering (k=4) — comparative profile</p>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <Card title="Segment Radar" sub="Feature comparison across all clusters" badge="K-Means">
          <div className="h-[260px] sm:h-[300px]">
            <Radar
              data={{
                labels: ['GPA', 'Attendance', 'Course Load', 'Pass Rate'],
                datasets: segs.map((s, i) => ({
                  label: s,
                  fill: true,
                  data: [
                    (gpas[i]  || 0) / 4 * 100,
                    (atts[i]  || 0),
                    Math.min((loads[i] || 0) / 60 * 100, 100),
                    (prs[i]   || 0) * 100,
                  ],
                  backgroundColor: (colors[i] || ACCENT) + '33',
                  borderColor:     colors[i]  || ACCENT,
                  borderWidth: 2,
                  pointRadius: 3,
                }))
              }}
              options={{
                maintainAspectRatio: false,
                plugins: { legend: { position: 'bottom', labels: { boxWidth: 10, font: { size: 10 } } } },
                scales: {
                  r: {
                    min: 0, max: 100,
                    ticks: { stepSize: 25, font: { size: 9 } },
                    grid:  { color: '#E2E8F0' },
                  }
                }
              }}
            />
          </div>
        </Card>

        <Card title="Segment Profiles" sub="Average feature values per cluster">
          <div className="overflow-x-auto">
            <table className="w-full text-xs sm:text-sm">
              <thead>
                <tr className="border-b border-gray-100">
                  {['Segment','Count','Avg GPA','Att %','Pass %'].map(h => (
                    <th key={h} className="text-left text-[10px] sm:text-xs text-gray-400 uppercase tracking-wide pb-3 font-semibold pr-3">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {segs.map((seg, i) => (
                  <tr key={i} className="border-b border-gray-50 hover:bg-gray-50/80">
                    <td className="py-2.5 pr-3">
                      <span className="flex items-center gap-2 font-medium text-slate-800">
                        <span className="w-2 h-2 rounded-full flex-shrink-0"
                              style={{ background: colors[i] || ACCENT }} />
                        <span className="text-xs truncate max-w-[110px] sm:max-w-none">{seg}</span>
                      </span>
                    </td>
                    <td className="py-2.5 pr-3 text-gray-600 tabular-nums">{(cnts[i] ?? 0).toLocaleString()}</td>
                    <td className="py-2.5 pr-3 text-gray-600 tabular-nums">{(gpas[i] ?? 0).toFixed(2)}</td>
                    <td className="py-2.5 pr-3 text-gray-600 tabular-nums">{(atts[i] ?? 0).toFixed(1)}%</td>
                    <td className="py-2.5 text-gray-600 tabular-nums">{((prs[i] ?? 0) * 100).toFixed(1)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      </div>
    </div>
  )
}

// ── Loading spinner ───────────────────────────────────────────────────────────
function Spinner() {
  return (
    <div className="flex items-center justify-center h-80 sm:h-96 gap-3 text-gray-400 text-xs sm:text-sm">
      <div className="w-5 h-5 border-2 border-gray-200 border-t-indigo-500 rounded-full animate-spin" />
      Loading analytics…
    </div>
  )
}

// ── Chart options helpers ──────────────────────────────────────────────────────
const baseBar = (horiz=false) => ({
  maintainAspectRatio: false,
  indexAxis: horiz ? 'y' : 'x',
  plugins:   { legend:{ display:false } },
  scales: horiz
    ? { x:{ grid:{color:'#F8FAFC'}, ticks:{font:{size:10}} }, y:{ grid:{display:false}, ticks:{font:{size:10}} } }
    : { x:{ grid:{display:false}, ticks:{font:{size:10}} },   y:{ grid:{color:'#F8FAFC'}, ticks:{font:{size:10}} } }
})

// ── Main Dashboard ────────────────────────────────────────────────────────────
export default function Dashboard() {
  const [page, setPage]            = useState('overview')
  const [data, setData]            = useState({})
  const [loading, setLoading]       = useState(true)
  const [fetchErr, setFetchErr]     = useState(null)
  const [warmingUp, setWarmingUp]   = useState(false)
  const [retryCountdown, setRetryCountdown] = useState(0)
  const [retryAttempt, setRetryAttempt]     = useState(0)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const MAX_POLLS  = 45   // 45 × 4s = 3 minutes max wait
  const POLL_DELAY = 4    // seconds between health checks

  const fetchAllData = React.useCallback(() => {
    setLoading(true)
    setFetchErr(null)
    Promise.all([
      fetch(`${API}/api/overview`).then(r    => { if(!r.ok) throw Object.assign(new Error(r.status), {status:r.status}); return r.json() }),
      fetch(`${API}/api/scatter`).then(r     => { if(!r.ok) throw Object.assign(new Error(r.status), {status:r.status}); return r.json() }),
      fetch(`${API}/api/departments`).then(r => { if(!r.ok) throw Object.assign(new Error(r.status), {status:r.status}); return r.json() }),
      fetch(`${API}/api/courses`).then(r     => { if(!r.ok) throw Object.assign(new Error(r.status), {status:r.status}); return r.json() }),
      fetch(`${API}/api/segments`).then(r    => { if(!r.ok) throw Object.assign(new Error(r.status), {status:r.status}); return r.json() }),
    ]).then(([overview, scatter, depts, courses, segments]) => {
      setData({ overview, scatter, depts, courses, segments })
      setWarmingUp(false)
      setFetchErr(null)
      setLoading(false)
    }).catch(e => {
      setFetchErr(e.message)
      setLoading(false)
      setWarmingUp(false)
    })
  }, [])

  const pollHealth = React.useCallback((poll = 0) => {
    setLoading(false)
    setWarmingUp(true)
    setRetryAttempt(poll + 1)

    fetch(`${API}/api/health`)
      .then(r => r.json())
      .then(h => {
        if (h.models_loaded) {
          setWarmingUp(false)
          fetchAllData()
        } else if (poll < MAX_POLLS) {
          let secs = POLL_DELAY
          setRetryCountdown(secs)
          const tick = setInterval(() => {
            secs -= 1
            setRetryCountdown(secs)
            if (secs <= 0) { clearInterval(tick); pollHealth(poll + 1) }
          }, 1000)
        } else {
          setFetchErr('Server took too long to load models. Please refresh the page.')
          setWarmingUp(false)
          setLoading(false)
        }
      })
      .catch(() => {
        if (poll < MAX_POLLS) {
          let secs = POLL_DELAY
          setRetryCountdown(secs)
          const tick = setInterval(() => {
            secs -= 1
            setRetryCountdown(secs)
            if (secs <= 0) { clearInterval(tick); pollHealth(poll + 1) }
          }, 1000)
        } else {
          setFetchErr('Cannot reach server. Check Render logs.')
          setWarmingUp(false)
          setLoading(false)
        }
      })
  }, [fetchAllData])

  useEffect(() => {
    fetch(`${API}/api/health`)
      .then(r => r.json())
      .then(h => {
        if (h.models_loaded) {
          fetchAllData()
        } else {
          pollHealth(0)
        }
      })
      .catch(() => pollHealth(0))
  }, [fetchAllData, pollHealth])

  const navItems = [
    { id:'overview',    icon:'⊞', label:'Overview' },
    { id:'predict',     icon:'◈', label:'Predict Student' },
    { id:'departments', icon:'⬡', label:'Departments' },
    { id:'courses',     icon:'◻', label:'Course Difficulty' },
    { id:'segments',    icon:'◑', label:'Segments' },
  ]

  const ov = data.overview || {}

  const handleNavClick = (id) => {
    setPage(id)
    setMobileMenuOpen(false)
  }

  return (
    <div className="min-h-screen bg-slate-50 font-sans flex flex-col md:flex-row">

      {/* ── Mobile top navbar ── */}
      <header className="md:hidden sticky top-0 z-40 bg-slate-900 text-white px-4 h-14 flex items-center justify-between border-b border-slate-800 shadow-md">
        <Link to="/" className="flex items-center gap-2 text-decoration-none">
          <div className="w-7 h-7 bg-indigo-600 rounded-lg flex items-center justify-center text-white font-bold text-xs">P</div>
          <span className="font-bold text-sm tracking-tight text-white">PRAGYA</span>
        </Link>

        <div className="flex items-center gap-2">
          <span className="text-[11px] text-indigo-400 font-medium bg-indigo-500/10 px-2.5 py-0.5 rounded-full border border-indigo-500/20 truncate max-w-[120px]">
            {navItems.find(n => n.id === page)?.label}
          </span>
          <button onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                  className="p-1.5 text-slate-300 hover:text-white rounded-lg hover:bg-slate-800 transition-colors"
                  aria-label="Toggle Navigation">
            <div className="w-5 h-4 flex flex-col justify-between">
              <div className={`w-5 h-0.5 bg-white transition-all origin-left ${mobileMenuOpen ? 'rotate-45 translate-x-0.5 -translate-y-0.5' : ''}`} />
              <div className={`w-5 h-0.5 bg-white transition-all ${mobileMenuOpen ? 'opacity-0' : ''}`} />
              <div className={`w-5 h-0.5 bg-white transition-all origin-left ${mobileMenuOpen ? '-rotate-45 translate-x-0.5 translate-y-0.5' : ''}`} />
            </div>
          </button>
        </div>
      </header>

      {/* ── Mobile menu backdrop ── */}
      {mobileMenuOpen && (
        <div className="fixed inset-0 bg-slate-950/60 backdrop-blur-sm z-40 md:hidden"
             onClick={() => setMobileMenuOpen(false)} />
      )}

      {/* ── Responsive Sidebar Drawer ── */}
      <aside className={`fixed top-0 left-0 bottom-0 z-50 w-64 md:w-56 bg-slate-900 text-white flex flex-col transition-transform duration-300 ease-in-out md:translate-x-0 ${
        mobileMenuOpen ? 'translate-x-0 shadow-2xl' : '-translate-x-full md:translate-x-0'
      }`}>
        <Link to="/" className="flex items-center gap-2.5 px-5 py-4 border-b border-white/10 text-decoration-none">
          <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center text-white font-bold text-sm shadow-md">P</div>
          <span className="text-white font-bold text-sm tracking-tight">PRAGYA</span>
        </Link>

        <div className="p-3 flex-1 overflow-y-auto">
          <p className="text-[10px] text-white/30 uppercase tracking-widest font-semibold px-2 mb-2">Analytics</p>
          {navItems.map(n => (
            <button key={n.id} onClick={() => handleNavClick(n.id)}
              className={`flex items-center gap-2.5 w-full px-3 py-2.5 rounded-xl border-0 cursor-pointer text-left text-xs font-medium mb-1 transition-all ${
                page===n.id ? 'bg-indigo-500/20 text-indigo-400 font-semibold' : 'text-white/60 hover:text-white hover:bg-white/5'
              }`}>
              <span className="text-sm">{n.icon}</span>
              <span>{n.label}</span>
            </button>
          ))}
        </div>

        <Link to="/guide" className="flex items-center gap-2 px-5 py-3 border-t border-white/10 text-white/40 hover:text-white text-xs text-decoration-none transition-colors">
          📖 User Guide
        </Link>
        <div className="px-5 py-4 text-[11px] text-white/30 border-t border-white/5 leading-relaxed">
          Pranav Lamkhade<br/>Roll 42 · PRN 202401120062
        </div>
      </aside>

      {/* ── Main content ── */}
      <main className="flex-1 md:ml-56 p-4 sm:p-6 md:p-8 min-w-0">

        {/* Warming-up banner (cold start) */}
        {warmingUp && (
          <div className="mb-4 p-3.5 sm:p-4 bg-orange-50 border border-orange-200 rounded-xl flex items-center gap-3 text-xs sm:text-sm">
            <div className="w-4 h-4 sm:w-5 sm:h-5 border-2 border-orange-500 border-t-transparent rounded-full animate-spin flex-shrink-0" />
            <div>
              <p className="margin-0 font-semibold text-orange-800">
                🚀 AI Models loading on server… (check {retryAttempt}/{MAX_POLLS})
              </p>
              <p className="margin-0 text-orange-600 text-xs mt-0.5">
                Elapsed ≈ {Math.round(retryAttempt * POLL_DELAY)}s — Retrying in {retryCountdown}s.
                Free tier needs ~60s to train models. Please wait…
              </p>
            </div>
          </div>
        )}

        {fetchErr && (
          <div className="mb-4 p-3.5 sm:p-4 bg-red-50 border border-red-200 rounded-xl text-xs sm:text-sm text-red-700">
            ⚠️ Could not connect to the API server (<code>{fetchErr}</code>).{' '}
            <button onClick={() => pollHealth(0)}
              className="ml-2 font-semibold text-indigo-600 bg-none border-0 cursor-pointer underline">
              Retry now
            </button>
          </div>
        )}

        {(loading && !warmingUp) ? <Spinner /> : (!warmingUp && (
          <>

          {/* ══ OVERVIEW ══ */}
          {page === 'overview' && (
            <div>
              <div className="mb-6 sm:mb-8">
                <h1 className="text-xl sm:text-2xl font-bold text-slate-900">Overview Dashboard</h1>
                <p className="text-xs sm:text-sm text-gray-400 mt-1">Academic performance metrics across {ov.total_students?.toLocaleString()} students</p>
              </div>

              {/* KPI Cards Grid */}
              <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3 sm:gap-4 mb-6">
                <KPI label="Total Students"  value={ov.total_students?.toLocaleString()} sub="Enrolled" />
                <KPI label="Avg GPA"         value={ov.avg_gpa}       sub="Out of 4.0" />
                <KPI label="Avg Attendance"  value={`${ov.avg_attendance}%`} sub="All courses" />
                <KPI label="At-Risk"         value={ov.at_risk?.toLocaleString()}
                     sub={`${(ov.at_risk/ov.total_students*100).toFixed(1)}% of total`} danger />
                <KPI label="Distinctions"    value={ov.distinctions?.toLocaleString()} sub="High performers" />
              </div>

              {/* Charts Row 1 */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-5 mb-5">
                <Card title="Result Distribution" sub="Pass / Fail / Distinction" badge="Classification">
                  <div className="h-[200px] sm:h-[220px]">
                    <Doughnut data={{
                      labels: Object.keys(ov.result_counts||{}),
                      datasets:[{data:Object.values(ov.result_counts||{}),
                        backgroundColor:['#10B981','#6366F1','#EF4444'], borderWidth:0, hoverOffset:6}]
                    }} options={{maintainAspectRatio:false, cutout:'70%', plugins:{legend:{position:'right', labels:{boxWidth:10}}}}} />
                  </div>
                </Card>
                <Card title="Student Segments" sub="K-Means cluster distribution" badge="Clustering">
                  <div className="h-[200px] sm:h-[220px]">
                    <Doughnut data={{
                      labels: Object.keys(ov.segment_counts||{}),
                      datasets:[{data:Object.values(ov.segment_counts||{}),
                        backgroundColor:Object.keys(ov.segment_counts||{}).map(k=>SEG_COLORS[k]||ACCENT),
                        borderWidth:0, hoverOffset:6}]
                    }} options={{maintainAspectRatio:false, cutout:'70%', plugins:{legend:{position:'right', labels:{boxWidth:10}}}}} />
                  </div>
                </Card>
              </div>

              {/* Charts Row 2 */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-5 mb-5">
                <Card title="GPA Distribution" sub="Student GPA spread">
                  <div className="h-[180px] sm:h-[200px]">
                    <Bar data={{
                      labels: ov.gpa_hist?.bins.slice(0,-1).map(b=>b.toFixed(1)),
                      datasets:[{label:'Students', data:ov.gpa_hist?.values,
                        backgroundColor:`${ACCENT}88`, borderColor:ACCENT, borderWidth:1, borderRadius:3}]
                    }} options={{...baseBar(), scales:{x:{grid:{display:false},ticks:{maxTicksLimit:8,font:{size:9}}},y:{grid:{color:'#F1F5F9'},ticks:{font:{size:9}}}}}} />
                  </div>
                </Card>
                <Card title="Attendance Distribution" sub="Percentage across students">
                  <div className="h-[180px] sm:h-[200px]">
                    <Bar data={{
                      labels: ov.att_hist?.bins.slice(0,-1).map(b=>b.toFixed(0)),
                      datasets:[{label:'Students', data:ov.att_hist?.values,
                        backgroundColor:'#10B98188', borderColor:'#10B981', borderWidth:1, borderRadius:3}]
                    }} options={{...baseBar(), scales:{x:{grid:{display:false},ticks:{maxTicksLimit:8,font:{size:9}}},y:{grid:{color:'#F1F5F9'},ticks:{font:{size:9}}}}}} />
                  </div>
                </Card>
              </div>

              {data.scatter && (
                <Card title="Attendance vs GPA" sub="1,500 random students — coloured by result" badge="Correlation">
                  <div className="h-[240px] sm:h-[260px]">
                    <Scatter data={{
                      datasets:['Distinction','Pass','Fail'].map(cls=>({
                        label:cls,
                        data:data.scatter.attendance.reduce((acc,a,i)=>
                          data.scatter.result[i]===cls?[...acc,{x:a,y:data.scatter.gpa[i]}]:acc,[]),
                        backgroundColor:(cls==='Distinction'?'#10B981':cls==='Pass'?'#6366F1':'#EF4444')+'55',
                        pointRadius:2.5, pointHoverRadius:4
                      }))
                    }} options={{maintainAspectRatio:false, plugins:{legend:{position:'top', labels:{boxWidth:10}}},
                      scales:{x:{title:{display:true,text:'Attendance %',font:{size:10}},grid:{color:'#F8FAFC'},ticks:{font:{size:9}}},
                               y:{title:{display:true,text:'GPA',font:{size:10}},grid:{color:'#F8FAFC'},ticks:{font:{size:9}}}}}} />
                  </div>
                </Card>
              )}
            </div>
          )}

          {/* ══ PREDICT ══ */}
          {page === 'predict' && (
            <div>
              <div className="mb-6 sm:mb-8">
                <h1 className="text-xl sm:text-2xl font-bold text-slate-900">Predict Student Outcome</h1>
                <p className="text-xs sm:text-sm text-gray-400 mt-1">Powered by Random Forest & Neural Network</p>
              </div>
              <PredictPanel />
            </div>
          )}

          {/* ══ DEPARTMENTS ══ */}
          {page === 'departments' && data.depts && (
            <div>
              <div className="mb-6 sm:mb-8">
                <h1 className="text-xl sm:text-2xl font-bold text-slate-900">Department Performance</h1>
                <p className="text-xs sm:text-sm text-gray-400 mt-1">Top 15 departments — Green means High, Red means At-Risk</p>
              </div>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-5">
                <Card title="Avg GPA by Department" sub="Coloured by performance">
                  <div className="h-[300px] sm:h-[360px]">
                    <Bar data={{
                      labels: data.depts.ids,
                      datasets:[{label:'Avg GPA', data:data.depts.avg_gpa,
                        backgroundColor: data.depts.avg_gpa.map(v=>v>=2.05?'#10B98166':v>=1.95?'#6366F166':'#EF444466'),
                        borderColor:     data.depts.avg_gpa.map(v=>v>=2.05?'#10B981':v>=1.95?'#6366F1':'#EF4444'),
                        borderWidth:1.5, borderRadius:4}]
                    }} options={{...baseBar(true), scales:{x:{min:1.8,max:2.2,grid:{color:'#F8FAFC'},ticks:{font:{size:9}}},y:{grid:{display:false},ticks:{font:{size:9}}}}}} />
                  </div>
                </Card>
                <Card title="Pass Rate % by Department">
                  <div className="h-[300px] sm:h-[360px]">
                    <Bar data={{
                      labels: data.depts.ids,
                      datasets:[{label:'Pass %', data:data.depts.pass_pct,
                        backgroundColor:`${ACCENT}33`, borderColor:ACCENT, borderWidth:1.5, borderRadius:4}]
                    }} options={{...baseBar(true), scales:{x:{min:70,max:90,grid:{color:'#F8FAFC'},ticks:{font:{size:9}}},y:{grid:{display:false},ticks:{font:{size:9}}}}}} />
                  </div>
                </Card>
              </div>
            </div>
          )}

          {/* ══ COURSES ══ */}
          {page === 'courses' && data.courses && (
            <div>
              <div className="mb-6 sm:mb-8">
                <h1 className="text-xl sm:text-2xl font-bold text-slate-900">Course Difficulty Bottlenecks</h1>
                <p className="text-xs sm:text-sm text-gray-400 mt-1">Difficulty = (1 − Pass Rate) × Credits &nbsp;·&nbsp; Red = Very Hard</p>
              </div>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-5">
                <Card title="Difficulty Score" sub="Higher = needs more academic intervention">
                  <div className="h-[280px] sm:h-[320px]">
                    <Bar data={{
                      labels: data.courses.ids,
                      datasets:[{label:'Difficulty', data:data.courses.difficulty,
                        backgroundColor: data.courses.difficulty.map(v=>v>1.2?'#EF444466':v>0.8?'#F59E0B66':'#10B98166'),
                        borderColor:     data.courses.difficulty.map(v=>v>1.2?'#EF4444':v>0.8?'#F59E0B':'#10B981'),
                        borderWidth:1.5, borderRadius:4}]
                    }} options={{...baseBar(), scales:{x:{grid:{display:false},ticks:{font:{size:9}}},y:{grid:{color:'#F8FAFC'},ticks:{font:{size:9}}}}}} />
                  </div>
                </Card>
                <Card title="Pass Rate %" sub="Lower = course bottleneck">
                  <div className="h-[280px] sm:h-[320px]">
                    <Bar data={{
                      labels: data.courses.ids,
                      datasets:[{label:'Pass %', data:data.courses.pass_pct,
                        backgroundColor:`${ACCENT}33`, borderColor:ACCENT, borderWidth:1.5, borderRadius:4}]
                    }} options={{...baseBar(), scales:{x:{grid:{display:false},ticks:{font:{size:9}}},y:{grid:{color:'#F8FAFC'},ticks:{font:{size:9}}}}}} />
                  </div>
                </Card>
              </div>
            </div>
          )}

          {/* ══ SEGMENTS ══ */}
          {page === 'segments' && <SegmentsSection segData={data.segments} />}

          </>
        ))}
      </main>
    </div>
  )
}
