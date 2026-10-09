import InlineRuns from './InlineRuns.jsx'

/**
 * The shared skeleton for /terms-of-use and /privacy-policy.
 * Both pages are structurally identical (spec/SPEC_blog_legal.md §4.1):
 *
 *   div.section.u-pb-0 > .container > .row.row-justify-center
 *     > .col.col-lg-8.col-md-12 > .section-header > h1.u-mb-0
 *   main#main > div.section > .container > .row.row-justify-center
 *     > .col.col-lg-8.col-md-12
 *         div                       ← intro block, NO .splitter
 *         n × div                   ← div.splitter + h3.h4 + p  per section
 *
 * These pages are hand-authored Webflow divs, NOT .w-richtext — so there is
 * deliberately no prose/rich-text wrapper here, just the repeating
 * splitter/heading/paragraph triplet.
 *
 * Note the WIDE `.container` (90% / max 90rem), not `.cc-narrow`: the legal
 * measure is 850.66px @1440, wider than the blog-post measure.
 *
 * Nav / Footer / ClipPathDefs are rendered by Layout, never here.
 *
 * @param title        h1 text
 * @param doc          { intro, sections } from src/data/legal/*.js
 * @param resolveHref  optional (href, label) => href|null, used to repair the
 *                     original's placeholder `href="#"` links.
 */
export default function LegalDocument({ title, doc, resolveHref }) {
  const { intro, sections } = doc

  // The one markup difference between the two routes: the "Effective date"
  // eyebrow is a div.eyebrow.u-mb-1 on /terms-of-use but an h2.eyebrow.u-mb-1
  // on /privacy-policy. Identical computed styling either way.
  const EyebrowTag = intro.eyebrowTag || 'div'

  return (
    <>
      <div className="section u-pb-0">
        <div className="container">
          <div className="row row-justify-center">
            <div className="col col-lg-8 col-md-12">
              <div className="section-header">
                <h1 className="u-mb-0">{title}</h1>
              </div>
            </div>
          </div>
        </div>
      </div>

      <main id="main">
        <div className="section">
          <div className="container">
            <div className="row row-justify-center">
              <div className="col col-lg-8 col-md-12">
                <div>
                  <EyebrowTag className="eyebrow u-mb-1">
                    <InlineRuns runs={intro.eyebrow} resolveHref={resolveHref} />
                  </EyebrowTag>
                  {intro.paragraphs.map((runs, i) => (
                    <p key={i}>
                      <InlineRuns runs={runs} resolveHref={resolveHref} />
                    </p>
                  ))}
                </div>

                {sections.map((section, i) => (
                  <div key={i}>
                    <div className="splitter" />
                    <h3 className="h4">{section.heading}</h3>
                    {section.paragraphs.map((runs, j) => (
                      <p key={j}>
                        <InlineRuns runs={runs} resolveHref={resolveHref} />
                      </p>
                    ))}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </main>
    </>
  )
}
