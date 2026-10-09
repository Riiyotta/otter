import { Link } from 'react-router-dom'
// CLONE_SPEC §6.3 — "Now in Beta" banner
export default function BetaBanner() {
  return (
    <header className="section hp-banner">
      <div className="container hp-banner">
        <div className="row row-justify-center">
          <div className="col">
            <div className="card">
              <div className="row gap-24">
                <div className="col col-narrow u-mb-0">
                  <img
                    src="/img/Playdate.svg"
                    loading="lazy"
                    alt=""
                    height="180"
                    className="image-2"
                  />
                </div>
                <div className="col u-mb-0 v-align-center spacing-md">
                  <div className="stack">
                    <div className="section-header">
                      <div className="eyebrow tag">Now in Beta</div>
                      <h2 className="h3-small">Become a founding caregiver</h2>
                    </div>
                    <p className="paragraph-1-25 u-mb-0">
                      Join Otter now and Otter will be free for you forever, even if we
                      introduce paid plans.
                    </p>
                  </div>
                  <div className="stack stack-x">
                    <a
                      href="https://app.withotter.com/sign-up"
                      target="_blank"
                      rel="noreferrer"
                      className="btn cc-white w-button"
                    >
                      Create a free profile
                    </a>
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
