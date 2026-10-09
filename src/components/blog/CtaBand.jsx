// SPEC_blog_legal.md §2.6 — the /blog CTA band.
//
// `.container.cc-cta.cc-wide-cta`: white, 72px radius, min-height 480px,
// 64px block padding; 32px radius / `min-height:auto` / `2rem 2rem 11rem`
// at ≤767, with `padding-bottom:41%` resolving against the parent `.section`
// width (159.898px at 390).
//
// `href="#"` is a dead link on the original (§2.1, §9) — kept as-is rather than
// silently repointed, so this is deliberately not a react-router <Link>.
export default function CtaBand() {
  return (
    <div className="section">
      <div className="container cc-cta cc-wide-cta">
        <div className="container cc-narrow cc-cta-2">
          <div className="row row-justify-between">
            <div className="col col-lg-5 col-md-10 col-xs-11 u-mb-0">
              <div className="section-header">
                <h2 className="h3 u-mb-0">Find kidcare that works for your family.</h2>
                <a className="btn w-button" href="#">
                  Book kidcare
                </a>
              </div>
            </div>
            {/* Empty layout spacer column — present in the original DOM. */}
            <div className="col col-lg-4" />
          </div>
        </div>

        <div className="cta-image-wrapper cc-extra-wide">
          <div className="cta-image-contain cc-extra-wide">
            <div className="cta-image-aspect cc-extra-wide">
              <img
                className="u-img-cover"
                src="/img/blog-cta.webp"
                alt="Illustration of a kid and sitter holding hands"
                loading="lazy"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
