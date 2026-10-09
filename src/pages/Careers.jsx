import '../styles/faq-contact-careers.css'

/* /careers — "Careers • Join our team"  (SPEC_faq_contact_careers.md §5)

   Job rows reuse the FAQ accordion markup (`.faq-item.cc-listing`) as an
   <a> pill. No department grouping, no ATS iframe, no empty state: three
   roles are published and each opens Greenhouse in a new tab.

   a11y fixes vs the original (visuals unchanged):
     - dropped `aria-label="accordeon open"` (misspelled, and wrong: it is a
       decorative icon, not a control) from the icon wrapper
     - dropped `role="button"` from that same wrapper (a nested button role
       inside an <a> is invalid) */

const STATS = [
  ['Affordability', '50%', "Of American families can't afford childcare"],
  [
    'access',
    '50%',
    'Of families live in a childcare desert, where there are 3 kids for every seat',
  ],
  ['Impact', '2 million', 'Women left the workforce during the pandemic'],
  ['stay-at-home parents', '12 million', "Parents don't work outside the home"],
  ['Poverty', '25%', 'Of stay-at-home parents and their families live in poverty'],
  ['Daycare', '4 million', 'Childcare seats have been lost since March 2020'],
]

const VALUE_CARDS = [
  [
    'Our values',
    [
      ['Care first', '/img/care-first.webp'],
      ['Always build trust', '/img/always-build-trust.webp'],
      ['Be rigorous', '/img/be-rigorous.webp'],
    ],
  ],
  [
    'Our operating principles',
    [
      ['Always do the right thing', '/img/do-the-right-thing.webp'],
      ['Win some, learn some', '/img/win-some,-learn-some.webp'],
      ['Build for diversity', '/img/build-for-diversity.webp'],
    ],
  ],
]

const BENEFITS = [
  [
    '/img/healthcare.webp',
    'Healthcare',
    'We offer free medical, vision, and dental benefits for you and your dependents.',
  ],
  [
    '/img/401k.webp',
    '401(k) plan',
    'We offer a 401(k) plan so you can plan for your future, starting now.',
  ],
  [
    '/img/exercising-options-1x1.webp',
    '7 years to exercise your options',
    'We offer a 7-year exercise window to exercise options for people who stay with Otter for two years or more.',
  ],
  [
    '/img/flexible-time-off.webp',
    'Flexible time off',
    "We want you to recharge as you need and take time for the things you love — and we'll insist you take the time.",
  ],
  [
    '/img/parental-leave.webp',
    'Parental leave',
    'We offer 16 weeks of paid parental leave and flexible schedules as you come back to work so you can spend time with your growing family.',
  ],
  [
    '/img/dependent-fsa.webp',
    'Dependent care FSA',
    'You can set aside up to $5,000/yr pre-tax to put towards care for any of your dependents — and we will contribute up to $2,500 of that amount.',
  ],
]

const COMPENSATION = [
  [
    'Cohesive',
    'Otter’s compensation strategy fits together as a whole, with each individual piece making sense in light of the overall strategy.',
  ],
  [
    'Consistent',
    'Like individuals should be treated alike. There should be no differentiation based on irrelevant factors, like a better understanding of equity compensation.',
  ],
  [
    'Coherent',
    'Otter’s compensation strategy should be clear and easily understood by team members.',
  ],
]

const JOBS = [
  ['General Interest', 'San Francisco', 'https://boards.greenhouse.io/withotter/jobs/4243384004'],
  [
    'Market Operations - Chicago',
    'Chicago, IL',
    'https://boards.greenhouse.io/withotter/jobs/4894785004',
  ],
  [
    'Market Operations - SF Bay Area',
    'San Francisco Bay Area',
    'https://boards.greenhouse.io/withotter/jobs/4807382004',
  ],
]

function CenteredHeader({ eyebrow, heading, body }) {
  return (
    <div className="section-header cc-centered">
      <div className="eyebrow">{eyebrow}</div>
      <h2 className="h3 u-mb-0">{heading}</h2>
      {/* `.paragraph-1-25.u-mb-0` keeps text-align:left inside the centred
          header — that asymmetry is the original's. */}
      <p className="u-mb-0 paragraph-1-25">{body}</p>
    </div>
  )
}

export default function Careers() {
  return (
    <>
      <header className="section">
        <div className="container cc-narrow">
          <div className="row row-justify-between row-align-center">
            <div className="col col-lg-6 col-md-6 col-sm-10 col-xs-12">
              <div className="section-header">
                {/* `.u-mb-0` also sets font-weight:400 → Reckless Neue 400 is
                    requested while only the 900 Heavy face is hosted. The
                    synthesised face IS the original's look. */}
                <h1 className="u-mb-0">Making the impossible things about kidcare possible</h1>
                <p className="paragraph-1-5 u-mb-0">
                  We connect parents who need childcare with parents who can care for their kids.
                </p>
                <a href="#jobs" className="btn w-button">
                  Join our team
                </a>
              </div>
            </div>
            <div className="col u-mb-0 col-lg-5 col-sm-12">
              <div className="header-shapes-contain">
                <div className="shape-contain cc-sitters-top">
                  <div className="shape-ratio">
                    <div className="shape stone-hero_middle-left u-bg-coral">
                      <div className="u-aspect-1x1">
                        <img
                          src="/img/Playing_Colored_01-1.webp"
                          srcSet="/img/Playing_Colored_01-1-p-500.png 500w, /img/Playing_Colored_01-1-p-800.png 800w, /img/Playing_Colored_01-1-p-1080.png 1080w, /img/Playing_Colored_01-1-p-1600.png 1600w, /img/Playing_Colored_01-1.webp 1882w"
                          sizes="(max-width: 479px) 72vw, (max-width: 767px) 68vw, (max-width: 991px) 38vw, 32vw"
                          loading="lazy"
                          alt="Kid playing with sitter"
                          className="u-img-cover"
                        />
                      </div>
                    </div>
                  </div>
                </div>
                <div className="shape-contain cc-sitters-bottom">
                  <div className="shape-ratio">
                    <div className="shape stone-hero_top-left u-bg-olive rotate-90" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main id="main">
        {/* 3 — Kidcare that fills the gap */}
        <section className="section">
          <div className="container cc-narrow">
            <div className="row">
              <div className="col col-lg-6 col-sm-12">
                <div className="u-aspect-9x16">
                  <img
                    src="/img/Illo-Sitter---Parents.webp"
                    srcSet="/img/Illo-Sitter---Parents-p-500.png 500w, /img/Illo-Sitter---Parents-p-800.png 800w, /img/Illo-Sitter---Parents-p-1080.png 1080w, /img/Illo-Sitter---Parents.webp 1252w"
                    sizes="(max-width: 479px) 90vw, (max-width: 767px) 85vw, (max-width: 991px) 40vw, 43vw"
                    loading="lazy"
                    alt=""
                    className="u-img-cover"
                  />
                </div>
              </div>
              {/* `.col-sm-first` puts this copy above the image at ≤767 */}
              <div className="col col-lg-6 col-sm-first col-sm-12">
                <div className="section-header">
                  <h2 className="h3 u-mb-0">Kidcare that fills the gap</h2>
                  <p className="paragraph-1-5">
                    If we succeed in closing the childcare gap, every child will have access to
                    trustworthy kidcare and every parent will be economically empowered like never
                    before.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* 4 — The kidcare gap */}
        <section className="section">
          <div className="container cc-narrow u-mb-1">
            <h2 className="h3 u-text-center u-mb-2">The kidcare gap</h2>
            <div className="row row-justify-center">
              <div className="col col-lg-1 u-mb-0 col-md-hide" />
              {STATS.slice(0, 3).map(([eyebrow, figure, body]) => (
                <div className="col col-lg-3 col-md-4 col-sm-6" key={eyebrow}>
                  <div className="stat-contain">
                    <h3 className="eyebrow">{eyebrow}</h3>
                    <div className="h4 u-mb-0">{figure}</div>
                    <p>{body}</p>
                  </div>
                </div>
              ))}
              <div className="col col-lg-1 u-mb-0 col-md-hide" />
              {STATS.slice(3).map(([eyebrow, figure, body]) => (
                <div className="col col-lg-3 col-md-4 col-sm-6" key={eyebrow}>
                  <div className="stat-contain">
                    <h3 className="eyebrow">{eyebrow}</h3>
                    <div className="h4 u-mb-0">{figure}</div>
                    <p>{body}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* 5 — Values / operating principles. Full `.container`, not cc-narrow. */}
        <section className="section">
          <h2 className="u-sr-only">Values</h2>
          <div className="container">
            <div className="row row-justify-center">
              {VALUE_CARDS.map(([title, items]) => (
                <div className="col col-lg-5 col-md-12" key={title}>
                  <div className="values-wrap">
                    <h3 className="h4 u-mb-2 u-text-center">{title}</h3>
                    {items.map(([label, icon]) => (
                      <div className="values_item" key={label}>
                        <div className="paragraph-1-5">{label}</div>
                        <div className="icon-wrap-72">
                          <div className="u-aspect-1x1">
                            <img
                              src={icon}
                              loading="lazy"
                              alt=""
                              className="u-img-cover"
                            />
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* 6 — Benefits */}
        <section className="section">
          <div className="container cc-narrow">
            <div className="row row-justify-center u-mb-1">
              <div className="col col-lg-5 col-md-8 col-sm-12">
                <CenteredHeader
                  eyebrow="Taking Care of Our Team"
                  heading="Benefits"
                  body="In addition to competitive salaries and equity ownership in the company, we offer:"
                />
              </div>
            </div>
            <div className="row">
              {BENEFITS.map(([icon, title, body]) => (
                <div className="col col-lg-4 col-md-6 col-sm-12" key={title}>
                  <div className="trust-card">
                    <div className="benefits-icons">
                      <div className="u-aspect-1x1">
                        <img src={icon} loading="lazy" alt="" className="u-img-cover" />
                      </div>
                    </div>
                    <div className="trust-card_header">
                      <h3 className="trust-bar_header">{title}</h3>
                      <p className="u-mb-0">{body}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* 7 — Compensation philosophy */}
        <section className="section">
          <div className="container cc-narrow u-mb-1">
            <div className="row row-justify-center u-mb-1">
              <div className="col col-lg-7 col-md-12">
                <CenteredHeader
                  eyebrow="internal equity"
                  heading="Our compensation philosophy"
                  body="We articulated our compensation philosophy when we were still a team of two; our way of taking care of the team before they walked in the door."
                />
              </div>
            </div>
            <div className="row row-justify-center">
              {COMPENSATION.map(([title, body], i) => (
                <div
                  className={
                    ['col col-lg-4 col-sm-10 col-xs-12', 'col col-lg-4 col-sm-12 col-xs-12',
                      'col col-lg-4 col-md-12 col-xs-12'][i]
                  }
                  key={title}
                >
                  {/* `.stat-contain.u-text-center` centres the <p>, but
                      `.h4.u-mb-0` keeps the heading text-align:left. */}
                  <div className="stat-contain u-text-center">
                    <h3 className="h4 u-mb-0">{title}</h3>
                    <p>{body}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* 8 — Current Positions */}
        <section id="jobs" className="section">
          <div className="container cc-narrow u-mb-1">
            <div className="row row-justify-center u-mb-1">
              <div className="col col-lg-7 col-md-12">
                <CenteredHeader
                  eyebrow="join the team"
                  heading="Current Positions"
                  body="To build childcare that feels like family for families everywhere, we need a team with all kinds of different perspectives, experiences and backgrounds."
                />
              </div>
            </div>
            <div className="w-dyn-list">
              <div role="list" className="row w-dyn-items">
                {JOBS.map(([title, location, href]) => (
                  <div role="listitem" className="col u-mb-0 col-lg-12 w-dyn-item" key={href}>
                    <a
                      href={href}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="faq-item cc-listing w-inline-block"
                    >
                      <div className="faq-content">
                        <div className="faq-spacer">
                          <h3 className="paragraph-1-5 u-mb-0">{title}</h3>
                        </div>
                        <p className="u-mb-0">{location}</p>
                      </div>
                      <div className="faq-icon-wrapper cc-listing">
                        <div className="faq-icon">
                          <img
                            src="/img/up-right.svg"
                            loading="lazy"
                            alt=""
                            className="u-img-cover"
                          />
                        </div>
                      </div>
                    </a>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>
      </main>
    </>
  )
}
