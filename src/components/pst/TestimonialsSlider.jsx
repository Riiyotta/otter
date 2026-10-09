import DynEmpty from "./DynEmpty.jsx";

/**
 * Testimonials section on /parents and /sitters.
 * SPEC_parents_sitters_trust.md §6.
 *
 * The `.swiper` element is real but the CMS collection behind it is EMPTY —
 * zero `.swiper-slide`s — so the live site renders Webflow's grey
 * "No items found." placeholder inside it. That is reproduced exactly; no
 * testimonial copy is invented. The arrows exist and keep their hover
 * transition, but there is nothing for them to move (the original's Swiper
 * instance initialises against zero slides), so they suppress navigation.
 *
 * The stray empty `div.col.col-lg-6.col-md-6.u-mb-0` before the row is
 * dropped per spec §11.5.
 */
const ARROW_PATH =
  "M11.5314 26.823L10.3135 28C3.72297 21.6755 0.000137671 17.9124 0.000138013 14C0.000138355 10.0876 3.72297 6.28301 10.3135 -1.02167e-06L11.5314 1.16874C5.45837 6.9966 2.31558 10.315 1.8029 13.1715L22 13.1715L22 14.8293L1.80307 14.8293C2.31628 17.6843 5.45904 20.9958 11.5314 26.823Z";

// The original's SVG masks a second, inset copy of the arrow outline at
// fill-opacity .08 — a faint inner edge. Measured in the live DOM; it was
// missing from the first build.
const ARROW_INNER_PATH =
  "M10.3135 28L11.0084 28.7191L10.316 29.3883L9.62112 28.7215L10.3135 28ZM11.5314 26.823L12.2238 26.1015L12.973 26.8204L12.2264 27.542L11.5314 26.823ZM10.3135 -1.02167e-06L9.62349 -0.723793L10.3158 -1.38378L11.0059 -0.721523L10.3135 -1.02167e-06ZM11.5314 1.16874L12.2238 0.447217L12.9757 1.16874L12.2238 1.89026L11.5314 1.16874ZM1.8029 13.1715L1.8029 14.1715L0.607445 14.1715L0.818628 12.9948L1.8029 13.1715ZM22 13.1715L22 12.1715L23 12.1715L23 13.1715L22 13.1715ZM22 14.8293L23 14.8293L23 15.8293L22 15.8293L22 14.8293ZM1.80307 14.8293L0.818847 15.0062L0.607292 13.8293L1.80307 13.8293L1.80307 14.8293ZM9.61857 27.2809L10.8365 26.1039L12.2264 27.542L11.0084 28.7191L9.61857 27.2809ZM1.00014 14C1.00014 15.6213 1.76669 17.3199 3.46998 19.4755C5.17358 21.6314 7.69783 24.104 11.0059 27.2785L9.62112 28.7215C6.33865 25.5716 3.70621 23.0003 1.90076 20.7155C0.095003 18.4302 -0.999862 16.2911 -0.999862 14L1.00014 14ZM11.0035 0.723791C7.69727 3.87577 5.17331 6.34834 3.47069 8.50809C1.76778 10.6682 1.00014 12.3776 1.00014 14L-0.999862 14C-0.999862 11.71 0.0939144 9.56094 1.90006 7.26989C3.70649 4.97848 6.33921 2.40724 9.62349 -0.723793L11.0035 0.723791ZM10.839 1.89026L9.62112 0.72152L11.0059 -0.721523L12.2238 0.447217L10.839 1.89026ZM0.818628 12.9948C1.12291 11.2995 2.18026 9.58864 3.81635 7.64115C5.46477 5.67898 7.80647 3.35734 10.839 0.447217L12.2238 1.89026C9.18332 4.808 6.91709 7.0595 5.34769 8.92762C3.76595 10.8104 2.99557 12.187 2.78717 13.3481L0.818628 12.9948ZM1.8029 12.1715L22 12.1715L22 14.1715L1.8029 14.1715L1.8029 12.1715ZM23 13.1715L23 14.8293L21 14.8293L21 13.1715L23 13.1715ZM22 15.8293L1.80307 15.8293L1.80307 13.8293L22 13.8293L22 15.8293ZM10.839 27.5445C7.807 24.6349 5.46552 22.3152 3.81721 20.3552C2.18123 18.4098 1.1235 16.7011 0.818847 15.0062L2.7873 14.6524C2.99584 15.8125 3.7661 17.187 5.3479 19.0679C6.91737 20.9342 9.18346 23.1838 12.2238 26.1015L10.839 27.5445Z";

const ARROW_MASK_ID = "path-1-inside-1_199_686";

function Arrow({ direction, label }) {
  return (
    <a
      href="#"
      role="button"
      aria-label={label}
      className={`swiper-arrow swiper-button-${direction} w-inline-block`}
      onClick={(e) => e.preventDefault()}
    >
      <div className="swiper-icon">
        <div className="w-embed">
          <svg
            width="100%"
            height="100%"
            viewBox="0 0 22 28"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            aria-hidden="true"
          >
            <mask id={ARROW_MASK_ID} fill="white">
              <path fillRule="evenodd" clipRule="evenodd" d={ARROW_PATH} />
            </mask>
            <path
              fillRule="evenodd"
              clipRule="evenodd"
              d={ARROW_PATH}
              fill="currentColor"
            />
            <path
              d={ARROW_INNER_PATH}
              fill="currentColor"
              fillOpacity="0.08"
              mask={`url(#${ARROW_MASK_ID})`}
            />
          </svg>
        </div>
      </div>
    </a>
  );
}

export default function TestimonialsSlider({ heading, lede }) {
  return (
    <section className="section">
      <div className="container">
        <div className="row row-justify-between">
          <div className="col col-lg-5 col-md-12">
            <div className="u-bg-ivory">
              <div className="testimonials-contain">
                <div className="section-header">
                  <div className="eyebrow">testimonials</div>
                  <h2 className="h3 u-mb-0">{heading}</h2>
                  <p className="paragraph-1-5 u-mb-0">{lede}</p>
                </div>
                <div className="slider-arrows-wrapper">
                  <Arrow direction="prev" label="previous slide" />
                  <Arrow direction="next" label="next slide" />
                </div>
              </div>
            </div>
          </div>
          <div className="col col-lg-6 col-md-12">
            <div className="swiper-contain">
              <div className="swiper w-dyn-list">
                <DynEmpty />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
