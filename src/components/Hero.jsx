import { Link } from 'react-router-dom'
// CLONE_SPEC §6.2
export default function Hero() {
  return (
    <header className="section u-pt-0 u-pb-2">
      <div className="container cc-hero">
        <div className="u-z-index-3">
          <div className="row row-justify-center">
            <div className="col u-mb-0 col-lg-7 col-sm-12">
              <div className="hero_copy-wrapper">
                <h1>Build a care career that cares about you</h1>
                <div className="hero_p-container">
                  <p className="paragraph-1-5 u-text-center">
                    We want to get you the job and the pay you deserve.
                  </p>
                </div>
                <a
                  href="https://app.withotter.com/sign-up"
                  target="_blank"
                  rel="noreferrer"
                  className="btn cc-light w-button"
                >
                  Create a free profile
                </a>
              </div>
            </div>
          </div>
        </div>

        {/* class name typo (`brackgorund`) preserved from the original DOM */}
        <div className="hero-brackgorund-wrapper">
          <div className="hero_stones-col cc-left">
            <div className="shape-contain cc-hero_top-left">
              <div className="shape-ratio">
                <div className="shape stone-hero_top-left u-bg-peach">
                  <div className="u-aspect-1x1">
                    <img
                      src="/img/hero1.webp"
                      loading="lazy"
                      sizes="(max-width: 800px) 100vw, 800px"
                      srcSet="/img/hero1-p-500.webp 500w, /img/hero1.webp 800w"
                      alt="a person holding a baby"
                      className="u-img-cover"
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* flat olive, no image; display:none at ≤479 */}
            <div className="shape-contain cc-hero_middle-left">
              <div className="shape-ratio">
                <div className="shape stone-hero_middle-left u-bg-olive" />
              </div>
            </div>

            <div className="shape-contain cc-hero_bottom-left">
              <div className="shape-ratio">
                <div className="shape stone-hero_bottom-left">
                  <div className="u-aspect-1x1">
                    <img
                      src="/img/Playing_Colored_01-1.webp"
                      loading="lazy"
                      sizes="(max-width: 1882px) 100vw, 1882px"
                      srcSet="/img/Playing_Colored_01-1-p-500.png 500w, /img/Playing_Colored_01-1-p-800.png 800w, /img/Playing_Colored_01-1-p-1080.png 1080w, /img/Playing_Colored_01-1-p-1600.png 1600w, /img/Playing_Colored_01-1.webp 1882w"
                      alt="Kid playing with sitter"
                      className="u-img-cover"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="hero_stones-col">
            {/* flat celeste, no image */}
            <div className="shape-contain cc-hero_top-right">
              <div className="shape-ratio">
                <div className="shape stone-hero_top-right u-bg-celeste" />
              </div>
            </div>

            <div className="shape-contain cc-hero_bottom-right">
              <div className="shape-ratio">
                <div className="shape stone-hero_bottom-right">
                  <div className="u-aspect-1x1">
                    <img
                      src="/img/hero2.webp"
                      loading="lazy"
                      sizes="(max-width: 800px) 100vw, 800px"
                      srcSet="/img/hero2-p-500.webp 500w, /img/hero2.webp 800w"
                      alt="a child with their hands on their head"
                      className="u-img-cover"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}
