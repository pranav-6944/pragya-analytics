import React from 'react'

const cases = [
  {
    icon: '🎓',
    who: 'Academic Institutions',
    desc: 'Improve student success rates and reduce dropout rates using predictive insights at the institutional level.',
    color: 'from-violet-50 to-white',
    border: 'border-violet-100',
  },
  {
    icon: '👨‍🏫',
    who: 'Faculty Members',
    desc: 'Identify weak students early and provide targeted interventions before exam cycles, reducing failure rates.',
    color: 'from-blue-50 to-white',
    border: 'border-blue-100',
  },
  {
    icon: '🧑‍🎓',
    who: 'Students',
    desc: 'Track personal performance benchmarks and receive early warnings to improve academic outcomes proactively.',
    color: 'from-emerald-50 to-white',
    border: 'border-emerald-100',
  },
]

const differentiators = [
  { icon: '💡', title: 'Intelligent Predictions', desc: 'Goes beyond traditional analytics by predicting future outcomes, not just reporting the past.' },
  { icon: '⚙️', title: 'Data-Driven Decisions', desc: 'Empowers institutions with actionable insights backed by real, structured academic data.' },
  { icon: '🚀', title: 'Scalable System', desc: 'Designed to handle large academic datasets with 10,000+ students efficiently.' },
  { icon: '🎯', title: 'User-Friendly Interface', desc: 'Simple, intuitive dashboard for educators and administrators — no data science required.' },
]

export default function UseCases() {
  return (
    <>
      {/* Use Cases */}
      <section id="usecases" className="section bg-white">
        <div className="container">
          <div className="text-center mb-16">
            <div className="section-tag">✦ Applications</div>
            <h2 className="section-title">Who Benefits from PRAGYA?</h2>
            <p className="section-sub max-w-xl mx-auto">
              Designed for every stakeholder in the academic ecosystem.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-24">
            {cases.map((c, i) => (
              <div key={i} className={`bg-gradient-to-b ${c.color} border ${c.border} rounded-2xl p-8
                hover:shadow-xl hover:-translate-y-1 transition-all duration-300`}>
                <div className="text-4xl mb-5">{c.icon}</div>
                <h3 className="text-xl font-bold text-navy-900 mb-3">{c.who}</h3>
                <p className="text-navy-600 text-sm leading-relaxed">{c.desc}</p>
              </div>
            ))}
          </div>

          {/* Why PRAGYA */}
          <div className="text-center mb-14">
            <div className="section-tag">✦ Why PRAGYA</div>
            <h2 className="section-title">What Makes Us Different</h2>
            <p className="section-sub max-w-xl mx-auto">
              PRAGYA is not just analytics — it's academic intelligence reimagined.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {differentiators.map((d, i) => (
              <div key={i} className="text-center p-8 rounded-2xl border border-gray-100 hover:shadow-lg
                hover:border-accent/20 hover:-translate-y-1 transition-all duration-300 bg-white">
                <div className="w-14 h-14 bg-accent-light rounded-2xl flex items-center justify-center text-2xl mx-auto mb-5">
                  {d.icon}
                </div>
                <h3 className="font-bold text-navy-900 mb-3">{d.title}</h3>
                <p className="text-navy-600 text-sm leading-relaxed">{d.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </>
  )
}
