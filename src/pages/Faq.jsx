import '../styles/faq-contact-careers.css'

/* /faq — "Common Questions • Otter Kidcare"  (SPEC_faq_contact_careers.md §3)

   There is NO accordion on this route. Both CMS collection lists are
   genuinely empty on the original: the server HTML ships no item template
   at all, only Webflow's `.w-dyn-empty` placeholder. We replicate that
   exactly — two static category rows plus the grey "No items found." box.
   No FAQ copy is invented. The accordion component itself is ported in
   src/styles/faq-contact-careers.css for /careers and future CMS content. */

function EmptyCollectionList() {
  return (
    <div className="w-dyn-list">
      <div className="w-dyn-empty">
        <div>No items found.</div>
      </div>
    </div>
  )
}

function CategorySection({ heading }) {
  return (
    <section className="section">
      <div className="container cc-narrow">
        <div className="row row-justify-around">
          <div className="col col-lg-4 col-sm-12">
            <div>
              <h2 className="h3">{heading}</h2>
            </div>
          </div>
          <div className="col col-lg-7 col-sm-12">
            <EmptyCollectionList />
          </div>
        </div>
      </div>
    </section>
  )
}

export default function Faq() {
  return (
    <>
      <header className="section">
        <div className="container cc-narrow">
          <div className="row row-align-center row-justify-between">
            <div className="col col-lg-6 col-sm-10 col-xs-12">
              <div className="section-header">
                <h1>Common questions</h1>
              </div>
            </div>
            <div className="col u-mb-0 col-lg-5 col-sm-12">
              <div className="header-shapes-contain">
                <div className="shape-contain cc-sitters-top">
                  <div className="shape-ratio">
                    <div className="shape footer-shape-right">
                      <div className="u-aspect-1x1">
                        <img
                          src="/img/hero2.webp"
                          srcSet="/img/hero2-p-500.webp 500w, /img/hero2.webp 800w"
                          sizes="(max-width: 479px) 72vw, (max-width: 767px) 68vw, (max-width: 991px) 38vw, 32vw"
                          loading="lazy"
                          alt="a child with their hands on their head"
                          className="u-img-cover"
                        />
                      </div>
                    </div>
                  </div>
                </div>
                <div className="shape-contain cc-sitters-bottom">
                  <div className="shape-ratio">
                    <div className="shape stone-hero_bottom-left u-bg-peach" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main id="main">
        <CategorySection heading="For parents" />
        <CategorySection heading="For sitters" />
      </main>
    </>
  )
}
