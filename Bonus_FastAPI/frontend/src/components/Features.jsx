import React from 'react'

const features = [
  {
    icon: '🔮',
    title: 'Predict Performance',
    desc: 'Use machine learning models like Random Forest and Neural Networks to predict student outcomes — Pass, Fail, or Distinction — with high accuracy.',
    tag: 'Random Forest · ANN',
    color: 'bg-violet-50 border-violet-100',
    iconBg: 'bg-violet-100 text-violet-600',
  },
  {
    icon: '📉',
    title: 'At-Risk Detection',
    desc: 'Identify students at risk of failure or dropout based on GPA, attendance, and academic trends — before it\'s too late to intervene.',
    tag: 'Early Warning System',
    color: 'bg-red-50 border-red-100',
    iconBg: 'bg-red-100 text-red-500',
  },
  {
    icon: '📊',
    title: 'Advanced Analytics',
    desc: 'Visualize GPA distributions, attendance patterns, and correlations through interactive charts and comprehensive dashboards.',
    tag: 'Chart.js · Recharts',
    color: 'bg-blue-50 border-blue-100',
    iconBg: 'bg-blue-100 text-blue-500',
  },
  {
    icon: '🧠',
    title: 'Smart Insights',
    desc: 'Gain actionable insights from clustering and segmentation techniques to understand different student groups and their needs.',
    tag: 'K-Means · ARM',
    color: 'bg-emerald-50 border-emerald-100',
    iconBg: 'bg-emerald-100 text-emerald-600',
  },
]

export default function Features() {
  return (
    <section id="features" className="section bg-gray-50/50">
      <div className="container">
        <div className="text-center mb-16">
          <div className="section-tag">✦ Key Features</div>
          <h2 className="section-title">Everything You Need<br />to Drive Student Success</h2>
          <p className="section-sub max-w-xl mx-auto">
            PRAGYA combines advanced ML with intuitive design to give educators
            the tools they need — all in one platform.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {features.map((f, i) => (
            <div key={i}
                 className={`rounded-2xl border p-8 hover:shadow-lg hover:-translate-y-1 transition-all duration-300 ${f.color}`}
                 style={{ animationDelay: `${i*0.1}s` }}>
              <div className={`w-12 h-12 rounded-xl flex items-center justify-center text-2xl mb-5 ${f.iconBg}`}>
                {f.icon}
              </div>
              <h3 className="text-xl font-bold text-navy-900 mb-3">{f.title}</h3>
              <p className="text-navy-600 leading-relaxed text-sm mb-4">{f.desc}</p>
              <span className="inline-block bg-white/80 text-navy-600 text-xs font-medium px-3 py-1 rounded-full border border-white">
                {f.tag}
              </span>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
