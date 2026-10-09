// CLONE_SPEC §6.5 — "As featured in". DOM order: Forbes, Parents, NYT, mom.com
const LOGOS = [
  { src: '/img/forbes.svg', alt: 'Forbes magazine' },
  { src: '/img/parents.svg', alt: 'parents.com' },
  { src: '/img/NYT.svg', alt: 'The New York Times' },
  { src: '/img/mom.svg', alt: 'mom.com' },
]

export default function TrustBar() {
  return (
    <section className="section">
      <div className="container">
        <div className="row row-justify-between">
          <div className="col col-lg-12 u-mb-0">
            <div className="trust-bar">
              {/* `.u-mb-0` wins font-weight here → 400, not the eyebrow's 600 */}
              <h2 className="eyebrow u-mb-0 u-text-center">As featured in</h2>
              <div className="featured-logos">
                {LOGOS.map((l) => (
                  <div className="featured-logo-wrap" key={l.src}>
                    <img
                      src={l.src}
                      loading="lazy"
                      alt={l.alt}
                      className="featured-logo"
                    />
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
