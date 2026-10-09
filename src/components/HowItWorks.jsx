import { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'

// CLONE_SPEC §6.4
const STEPS = [
  {
    n: '1',
    title: 'Get started',
    body:
      "We like to keep it simple. Tell us your name, contact information, and a little bit about your childcare experience and what you're looking for in your next role.",
  },
  {
    n: '2',
    title: 'Give us a call',
    body:
      'Meet Autumn, our AI assistant, who asks you all the right questions to understand your strengths and help you present your best self in just minutes!',
  },
  {
    n: '3',
    title: 'Share your profile',
    body:
      'Showcase your best self everywhere you apply with your portable, customized profile, designed to help you shine.',
  },
]

export default function HowItWorks() {
  // §7.1 — the page's only scroll reveal. IX2 event e-31 (SCROLL_INTO_VIEW,
  // scrollOffsetValue 20 / unit "%", direction BOTTOM, fires once) driving the
  // `slideInBottom` action list: translateY(100px)/opacity 0 -> 0/1 over
  // 1000ms, delay 0, outQuart. The 20% viewport offset becomes the observer's
  // -20% bottom rootMargin; the timing itself lives in CSS (`.reveal.is-in`).
  const headerRef = useRef(null)
  const [revealed, setRevealed] = useState(false)

  useEffect(() => {
    const el = headerRef.current
    if (!el || revealed) return
    if (
      typeof IntersectionObserver !== 'function' ||
      window.matchMedia('(prefers-reduced-motion: reduce)').matches
    ) {
      setRevealed(true)
      return
    }
    const io = new IntersectionObserver(
      (entries, observer) => {
        if (!entries.some((e) => e.isIntersecting)) return
        observer.unobserve(el)
        observer.disconnect()
        setRevealed(true)
      },
      { root: null, rootMargin: '0px 0px -20% 0px', threshold: 0 }
    )
    io.observe(el)
    return () => io.disconnect()
  }, [revealed])

  return (
    <section className="section how-it-works">
      <div className="container cc-narrow">
        {/* Row A */}
        <div className="row row-reverse">
          <div className="col">
            <div className="how-it-works-image-wrapper">
              <img
                src="/img/Illo-Sitter-and-Kid.webp"
                loading="lazy"
                sizes="(max-width: 1062px) 100vw, 1062px"
                srcSet="/img/Illo-Sitter-and-Kid-p-500.png 500w, /img/Illo-Sitter-and-Kid-p-800.png 800w, /img/Illo-Sitter-and-Kid.webp 1062w"
                alt="A child handing a ball to a smiling caregiver"
                className="image"
              />
            </div>
          </div>
          <div className="col">
            {/* §7.1 — the page's ONLY scroll-reveal target. */}
            <div
              ref={headerRef}
              className={`section-header cc-tabas-header reveal${
                revealed ? ' is-in' : ''
              }`}
            >
              <div className="eyebrow">how it works</div>
              <h2 className="h3 u-mb-0">
                {'A profile that feels like you, because it is'}
              </h2>
            </div>
          </div>
        </div>

        {/* Row B */}
        <div className="row how-it-works">
          {STEPS.map((s) => (
            <div className="col" key={s.n}>
              <div className="home-card-2 how-it-works-card">
                <div className="bullet-organic bullet">
                  <div className="text-block-2">{s.n}</div>
                </div>
                <div className="how-it-works-copy">
                  <h3 className="h3-small">{s.title}</h3>
                  <p className="paragraph-1-25">{s.body}</p>
                </div>
              </div>
            </div>
          ))}

          <div className="col col-lg-12">
            <div className="home-card-2 home-card-lg">
              <div className="join-copy">
                <h3 className="h3">We want to help you grow</h3>
                <p className="paragraph-1-25">
                  We want to help you build a sustainable, rewarding career.
                </p>
                <a
                  href="https://app.withotter.com/sign-up"
                  target="_blank"
                  rel="noreferrer"
                  className="button-primary w-inline-block"
                >
                  Join Otter
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
