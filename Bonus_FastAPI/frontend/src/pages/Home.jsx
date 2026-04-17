import React from 'react'
import Navbar from '../components/Navbar'
import Hero from '../components/Hero'
import Features from '../components/Features'
import DashboardPreview from '../components/DashboardPreview'
import HowItWorks from '../components/HowItWorks'
import UseCases from '../components/UseCases'
import CTA from '../components/CTA'
import Footer from '../components/Footer'

export default function Home() {
  return (
    <div className="min-h-screen">
      <Navbar />
      <Hero />
      <Features />
      <DashboardPreview />
      <HowItWorks />
      <UseCases />
      <CTA />
      <Footer />
    </div>
  )
}
