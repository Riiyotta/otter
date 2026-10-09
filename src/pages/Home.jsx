import Hero from '../components/Hero.jsx'
import BetaBanner from '../components/BetaBanner.jsx'
import HowItWorks from '../components/HowItWorks.jsx'
import TrustBar from '../components/TrustBar.jsx'

// DOM order per CLONE_SPEC §6.
export default function Home() {
  return (
    <>
      <Hero />
      <BetaBanner />
      <main id="main">
        <HowItWorks />
        <TrustBar />
      </main>
    </>
  )
}
