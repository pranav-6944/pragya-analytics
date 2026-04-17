import React from 'react'

const steps = [
  {
    num: '01',
    title: 'Data Integration',
    desc: 'Consolidates data from multiple sources including student records, attendance, grades, and course enrollments into a unified analytical pipeline.',
    icon: '🗄️',
  },
  {
    num: '02',
    title: 'Data Processing',
    desc: 'Cleans and transforms raw data by handling missing values, normalizing grade formats, and engineering meaningful features like GPA and attendance percentage.',
    icon: '⚙️',
  },
  {
    num: '03',
    title: 'Predictive Modeling',
    desc: 'Applies machine learning algorithms — Random Forest, Neural Networks, SVM — to generate predictions and risk scores with high precision.',
    icon: '🧠',
  },
  {
    num: '04',
    title: 'Visualization & Insights',
    desc: 'Presents results through intuitive dashboards and interactive charts, enabling educators to take proactive, data-backed actions.',
    icon: '📊',
  },
]

export default function HowItWorks() {
  return (
    <section id="how" className="section bg-navy-900 relative overflow-hidden">
      {/* Background texture */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:48px_48px]" />
      <div className="absolute top-0 right-0 w-96 h-96 bg-accent/10 rounded-full blur-3xl" />
      <div className="absolute bottom-0 left-0 w-64 h-64 bg-accent/5 rounded-full blur-3xl" />

      <div className="container relative z-10">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 bg-white/10 text-white/80 text-xs font-semibold uppercase tracking-widest px-5 py-2 rounded-full mb-5">
            ✦ How It Works
          </div>
          <h2 className="text-4xl font-bold text-white leading-tight">
            Engineered for Precision,<br />Built for Impact
          </h2>
          <p className="text-white/60 text-lg mt-4 max-w-xl mx-auto leading-relaxed">
            A systematic four-step pipeline that transforms raw university data
            into actionable academic intelligence.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {steps.map((s, i) => (
            <div key={i} className="relative group">
              {/* Connector line */}
              {i < steps.length - 1 && (
                <div className="hidden lg:block absolute top-10 left-full w-full h-px bg-gradient-to-r from-white/20 to-transparent z-0" />
              )}
              <div className="relative bg-white/5 border border-white/10 rounded-2xl p-7 hover:bg-white/10 hover:border-white/20 transition-all duration-300">
                <div className="text-4xl mb-5">{s.icon}</div>
                <div className="text-accent text-xs font-bold tracking-widest uppercase mb-2">{s.num}</div>
                <h3 className="text-white font-bold text-lg mb-3">{s.title}</h3>
                <p className="text-white/50 text-sm leading-relaxed">{s.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
