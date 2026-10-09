import { Link, NavLink } from 'react-router-dom'
import OtterWordmark from './OtterWordmark.jsx'

// CLONE_SPEC §6.6. The stray empty `div.container` before the real one is
// dropped, per the spec's note.
//
// `chrome="site"` populates `.footer_links-container` with the three
// `ul.footer_link-list` columns that every route except `/` ships
// (SPEC_parents_sitters_trust §3.3, SPEC_faq_contact_careers §2.2,
// SPEC_blog_legal §1.2). `chrome="home"` leaves it the empty 0-height spacer
// the audited homepage renders.

// Columns in DOM order. Column 3 is external + target=_blank.
const SITE_LINKS = [
  { to: '/parents', label: 'Parents' },
  { to: '/sitters', label: 'Sitters' },
  { to: '/trust-safety', label: 'Trust & Safety' },
]

const RESOURCE_LINKS = [
  { to: '/faq', label: 'FAQ' },
  { to: '/careers', label: 'Careers' },
  { to: '/blog', label: 'Blog' },
  { to: '/contact', label: 'Contact' },
]

const SOCIAL_LINKS = [
  { href: 'https://www.instagram.com/otterchildcare/', label: 'Instagram' },
  { href: 'https://www.facebook.com/withotter/', label: 'Facebook' },
  { href: 'https://twitter.com/WithOtter', label: 'Twitter' },
  { href: 'https://www.linkedin.com/company/withotter', label: 'Linkedin' },
]

// Bare anchors, no class — they inherit `a { color: var(--primary);
// font-weight: 500; text-decoration: none }`. NavLink so the active route's
// anchor picks up `w--current` the way Webflow's does (no visual rule applies
// in the footer, but it keeps the markup faithful).
function InternalColumn({ items }) {
  return (
    <ul role="list" className="footer_link-list w-list-unstyled">
      {items.map((item) => (
        <li key={item.to} className="footer_link">
          <NavLink
            to={item.to}
            className={({ isActive }) => (isActive ? 'w--current' : undefined)}
          >
            {item.label}
          </NavLink>
        </li>
      ))}
    </ul>
  )
}

export default function Footer({ chrome = 'site' }) {
  const isHome = chrome === 'home'

  return (
    <footer className="section cc-footer">
      {/* The original ships an empty, zero-height `div.container` here before
          the real one. CLONE_SPEC §6.6 calls it droppable, and it has no
          layout effect, but two pixel audits flagged the DOM-count
          difference — kept for exact parity. */}
      <div className="container" />
      <div className="container cc-footer-container">
        <div className="footer_card cc-left u-bg-primary">
          <div className="section-header cc-footer">
            <h2 className="h4 u-mb-0">Build a care career that loves you back</h2>
            <p className="paragraph-1-25">
              Level up your care career: gain access to the best care jobs, maximize
              your earnings, and unlock your potential.
            </p>
            {/* Auth screens are hosted locally in this clone, so the footer
                CTA routes in-app on every chrome instead of out to
                app.withotter.com. Note the original sends this one to
                /sign-up while hero/nav CTAs go to /sign-up/welcome. */}
            <a href="https://app.withotter.com/sign-up" target="_blank" rel="noreferrer" className="btn w-button">
              Get started
            </a>
          </div>
          <div className="shape-contain cc-footer-left">
            <div className="shape-ratio">
              <div className="shape footer-shape-left u-bg-olive" />
            </div>
          </div>
        </div>

        <div className="footer_card cc-right u-bg-white">
          <div className="footer_row">
            {isHome ? (
              /* empty on the homepage — renders as a 0-height spacer */
              <div className="footer_links-container" />
            ) : (
              <div className="footer_links-container">
                <InternalColumn items={SITE_LINKS} />
                <InternalColumn items={RESOURCE_LINKS} />
                <ul role="list" className="footer_link-list w-list-unstyled">
                  {SOCIAL_LINKS.map((item) => (
                    <li key={item.href} className="footer_link">
                      <a href={item.href} target="_blank" rel="noreferrer">
                        {item.label}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            <div aria-label="home" className="brand_logo cc-footer">
              <div className="w-embed">
                <OtterWordmark idSuffix="footer" />
              </div>
              <div className="u-sr-only">Go to home page</div>
            </div>
          </div>

          <div className="footer_row cc-bottom">
            <div className="footer_terms-links-wrapper">
              {isHome ? (
                <>
                  <a href="/terms-of-use" className="footer_terms-link">
                    Terms of Use
                  </a>
                  <div className="bullet">&nbsp;●</div>
                  <a href="/privacy-policy" className="footer_terms-link">
                    Privacy Policy
                  </a>
                </>
              ) : (
                <>
                  <Link to="/terms-of-use" className="footer_terms-link">
                    Terms of Use
                  </Link>
                  <div className="bullet">&nbsp;●</div>
                  <Link to="/privacy-policy" className="footer_terms-link">
                    Privacy Policy
                  </Link>
                </>
              )}
            </div>
            {/* the original injects the current year via Webflow's
                `.copyright-year` script; the spec measured 2025 */}
            <div className="footer_terms-link">
              © <span className="copyright-year">2025</span> With Otter Inc.
            </div>
          </div>

          <div className="shape-contain cc-footer-right">
            <div className="shape-ratio">
              <div className="shape footer-shape-right u-bg-peach" />
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}
