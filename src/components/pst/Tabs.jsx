import { useState } from 'react'

/**
 * The dual-mode disclosure widget on /parents and /sitters.
 * SPEC_parents_sitters_trust.md §4.
 *
 * >=992px: a pill tab strip in the left column driving absolutely-positioned
 *          cards in the right column (`.tab-content.cc-card`). Switching is
 *          index-based, exactly like the original's jQuery handler (§4.4).
 * <=991px: the right column is hidden (`.col-md-hide`) and each tab item
 *          becomes an accordion row. Open/close is NOT driven by React — the
 *          CSS sibling selector `.tab-trigger.cc-active + .tab-content-mask`
 *          does it, which is what produces the measured asymmetric timing
 *          (100ms delay + 300ms opening, no delay closing).
 *
 * The body copy is duplicated in the original (accordion bodies + desktop
 * cards). Here it is rendered from one `items` array, as spec §11.3 suggests,
 * so both layouts stay in sync.
 */
export default function Tabs({ eyebrow, heading, lede, items }) {
  const [active, setActive] = useState(0)

  return (
    <>
      <div className="row row-justify-between">
        <div className="col col-lg-5 col-md-12">
          {/* No data-w-id and no inline opacity:0 on this route — the
              homepage's scroll reveal does not run here (spec §8.1). */}
          <div className="section-header cc-tabas-header">
            <div className="eyebrow">{eyebrow}</div>
            <h2 className="h3 u-mb-0">{heading}</h2>
            <p className="u-mb-0 paragraph-1-5">{lede}</p>
          </div>

          <div className="tabs-wrapper">
            {items.map((item, i) => (
              <div className="tab-item" key={item.key}>
                <a
                  href="#"
                  className={`tab-trigger${i === active ? ' cc-active' : ''} w-inline-block`}
                  onClick={(e) => {
                    e.preventDefault()
                    setActive(i)
                  }}
                >
                  <div className="tab-trigger_icon" />
                  <div>{item.label}</div>
                </a>
                {/* Sibling of the trigger — the CSS adjacency is the
                    accordion mechanism. Visible <=991 only. */}
                <div className="tab-content-mask">
                  <div className="tab-content">
                    <div className="tab-content-image">
                      <img
                        src={item.img.src}
                        srcSet={item.img.srcSet}
                        sizes="(max-width: 479px) 80vw, (max-width: 767px) 79vw, (max-width: 991px) 80vw, 100vw"
                        alt={item.img.alt}
                        loading="lazy"
                        className="u-img-cover"
                      />
                    </div>
                    <p className="u-mb-0 u-text-center">{item.body}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="col col-lg-5 col-md-hide">
          <div className="tab-content-wrapper">
            {items.map((item, i) => (
              <div
                className={`tab-content cc-card${i === active ? ' cc-active' : ''}`}
                key={item.key}
              >
                <div className="tab-content-image">
                  <img
                    src={item.img.src}
                    srcSet={item.img.srcSet}
                    sizes={i === 0 ? '(max-width: 991px) 100vw, 30vw' : '100vw'}
                    alt={item.img.alt}
                    loading="lazy"
                    className="u-img-cover"
                  />
                </div>
                <p className="u-mb-0 u-text-center">{item.body}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  )
}
