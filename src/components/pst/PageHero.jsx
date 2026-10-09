/**
 * Light hero used by /parents, /sitters and /trust-safety.
 * SPEC_parents_sitters_trust.md §2 — same skeleton on all three routes; only
 * the copy, CTA count, column spans and shape fills differ.
 *
 * Both stones reuse the existing clip-path defs from ClipPathDefs.jsx; no new
 * `d` strings exist on these routes (spec §0).
 */
export default function PageHero({
  rowClassName,
  copyColClassName,
  topShape,
  bottomShape,
  children,
}) {
  return (
    <header className="section">
      <div className="container cc-narrow">
        <div className={rowClassName}>
          <div className={copyColClassName}>
            <div className="section-header">{children}</div>
          </div>
          <div className="col u-mb-0 col-lg-5 col-sm-12">
            <div className="header-shapes-contain">
              <div className="shape-contain cc-sitters-top">
                <div className="shape-ratio">
                  <div className={topShape.className}>
                    {topShape.img ? (
                      <div className="u-aspect-1x1">
                        <img
                          src={topShape.img.src}
                          alt={topShape.img.alt}
                          loading="lazy"
                          className="u-img-cover"
                        />
                      </div>
                    ) : null}
                  </div>
                </div>
              </div>
              <div className="shape-contain cc-sitters-bottom">
                <div className="shape-ratio">
                  <div className={bottomShape.className} />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}
