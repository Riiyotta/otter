import DynEmpty from './DynEmpty.jsx'

/**
 * "Common questions" section on /parents and /sitters.
 * SPEC_parents_sitters_trust.md §6 (end) + §11.1.
 *
 * The CMS collection behind it is empty upstream, so the live site renders
 * only the heading plus Webflow's grey "No items found." placeholder. There
 * is no accordion markup or CSS behind this heading anywhere on the site, so
 * nothing else is built here and no FAQ copy is invented.
 */
export default function CommonQuestions() {
  return (
    <section className="section">
      <div className="container cc-narrow">
        <div className="row row-justify-around">
          <div className="col">
            <div className="section-header">
              <h2 className="h3 u-mb-0">Common questions</h2>
            </div>
          </div>
        </div>
        <div className="w-dyn-list">
          <DynEmpty />
        </div>
      </div>
    </section>
  )
}
