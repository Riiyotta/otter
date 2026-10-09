/**
 * White rounded CTA card on /parents and /sitters.
 * SPEC_parents_sitters_trust.md §5.
 *
 * /parents  — `.cta-image-contain` (33%) + `.cta-image-aspect` (141%)
 * /sitters  — `.cta-image-contain.cc-extra-wide` (50%) + `.cta-image-aspect.cc-wide`
 *             (75%), and `.cc-wide-cta` on `.container.cc-cta`
 *
 * The decorative blob is `display:none` above 767px.
 * Per spec §11.5 the empty `div.col.col-lg-4.u-mb-0` spacer is dropped.
 */
export default function CtaCard({
  wide = false,
  heading,
  ctaLabel,
  image,
  imageContainClassName,
  imageAspectClassName,
  blobClassName,
}) {
  return (
    <div className={`container cc-cta${wide ? " cc-wide-cta" : ""}`}>
      <div className="container cc-narrow cc-cta-2">
        <div className="row row-justify-between">
          <div className="col col-lg-5 col-md-6 col-sm-11 u-mb-0">
            <div className="section-header">
              <h2 className="h3 u-mb-0">{heading}</h2>
              <a
                href="https://app.withotter.com/sign-up/welcome"
                target="_blank"
                rel="noreferrer"
                className="btn w-button"
              >
                {ctaLabel}
              </a>
            </div>
          </div>
        </div>
      </div>

      <div className="cta-image-wrapper">
        <div className="shape-contain cc-cta">
          <div className="shape-ratio">
            <div className={blobClassName} />
          </div>
        </div>
        <div className={imageContainClassName}>
          <div className={imageAspectClassName}>
            <img
              src={image.src}
              srcSet={image.srcSet}
              sizes={image.sizes}
              alt={image.alt}
              loading="lazy"
              className="u-img-cover"
            />
          </div>
        </div>
      </div>
    </div>
  );
}
