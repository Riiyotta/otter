import { useLayoutEffect, useRef, useState } from 'react'
import { Link, NavLink } from 'react-router-dom'
import OtterWordmark from './OtterWordmark.jsx'
import '../styles/chrome.css'

// CLONE_SPEC §6.1 + §8. Non-sticky (position: relative), transparent,
// margin: 48px 0, 60px tall on desktop.
// §7.3 — a-11 runs 200ms delay + 300ms, then flips display:none.
//
// `chrome="site"` adds the primary link group that every route except `/`
// ships (SPEC_parents_sitters_trust §3.1, SPEC_faq_contact_careers §2.1,
// SPEC_blog_legal §1.1). `chrome="home"` is the audited homepage markup and
// must stay byte-identical.
const CLOSE_MS = 500

// SPEC_parents_sitters_trust.md §3.1 — verbatim. viewBox 0 0 34 22.
const BLOB_D =
  'M0.54127 7.43938C-1.37846 10.4619 2.25598 18.3642 4.46461 19.6478C8.02481 21.6745 12.1971 22.4246 16.2626 21.769C20.5028 21.1227 33.3538 20.3852 33.9689 15.0138C34.4908 10.6803 28.3029 4.0891 26.2993 2.86916C24.0627 1.51267 15.6755 -0.553935 13.1127 0.137967C10.55 0.82987 2.29326 4.68998 0.54127 7.43938Z'

const NAV_LINKS = [
  { to: '/parents', label: 'Parents' },
  { to: '/sitters', label: 'Sitters' },
  { to: '/trust-safety', label: 'Trust & Safety' },
  { to: '/blog', label: 'Blog' },
]

// Mirrors Webflow's `w--current`: react-router's `isActive` resolves the same
// way (exact match on these non-nested routes), so the blob / coral pill lands
// on the same link the original marks.
function NavContentLink({ to, label, onNavigate }) {
  return (
    <NavLink
      to={to}
      onClick={onNavigate}
      className={({ isActive }) =>
        `nav_link w-inline-block${isActive ? ' w--current' : ''}`
      }
    >
      <div>{label}</div>
      <div className="nav_link-current-icon">
        <div className="current-icon">
          <div className="w-embed">
            <svg
              width="100%"
              height="100%"
              viewBox="0 0 34 22"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              aria-hidden="true"
              focusable="false"
            >
              <path d={BLOB_D} fill="currentColor" />
            </svg>
          </div>
        </div>
      </div>
    </NavLink>
  )
}

export default function Nav({ chrome = 'site' }) {
  const isHome = chrome === 'home'
  const [open, setOpen] = useState(false)
  // `mounted` owns the display:none -> block flip (IX2 a-10 group 2); `active`
  // owns the tweens (group 3). They have to be separate states because a
  // transition can't start out of display:none. `mounted` is raised in the
  // click handler itself so the flip is already committed by the time the
  // layout effect below runs.
  const [mounted, setMounted] = useState(false)
  const [active, setActive] = useState(false)
  const menuRef = useRef(null)
  const closeTimer = useRef(0)

  const toggle = () => {
    clearTimeout(closeTimer.current)
    setOpen((v) => {
      if (!v) setMounted(true)
      return !v
    })
  }

  const close = () => {
    clearTimeout(closeTimer.current)
    setOpen(false)
  }

  // useLayoutEffect + a forced reflow rather than waiting on rAF: the display
  // flip is already committed here, the reflow resolves it as the transition's
  // before-change style, and `active` is then flushed in the same frame before
  // paint. That keeps the tweens starting on the click's own frame the way IX2
  // does — a double rAF measured ~30ms behind the original.
  useLayoutEffect(() => {
    if (open) {
      if (menuRef.current) void menuRef.current.offsetHeight
      setActive(true)
      return undefined
    }

    setActive(false)
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      setMounted(false)
      return undefined
    }
    // a-11 / a-6: 200ms delay + 300ms, then display:none. Verified identical
    // in both action lists, so CLOSE_MS is not variant-dependent.
    closeTimer.current = setTimeout(() => setMounted(false), CLOSE_MS)
    return () => clearTimeout(closeTimer.current)
  }, [open])

  return (
    <nav className={`nav_wrapper${active ? ' is-nav-open' : ''}`}>
      <a href="#main" className="nav_skip-link w-inline-block">
        <div>Skip to Main</div>
      </a>
      <div className="container cc-nav">
        <div className="nav_logo-wrapper">
          {isHome ? (
            <a
              aria-label="home"
              href="/"
              aria-current="page"
              className="brand_logo w-inline-block"
            >
              <div className="w-embed">
                <OtterWordmark idSuffix="nav" />
              </div>
              <div className="u-sr-only">Go to home page</div>
            </a>
          ) : (
            // Not the current page off `/`, so no aria-current here.
            <Link aria-label="home" to="/" className="brand_logo w-inline-block">
              <div className="w-embed">
                <OtterWordmark idSuffix="nav" />
              </div>
              <div className="u-sr-only">Go to home page</div>
            </Link>
          )}
        </div>

        {/* ≤991 only. Open/close state is real; the IX2 timings in §7.2/§7.3
            are left to the Animation agent. */}
        <a
          href="#"
          className="nav_mobile-btn w-inline-block"
          aria-expanded={open}
          data-nav-toggle=""
          data-nav-open={open ? 'true' : 'false'}
          onClick={(e) => {
            e.preventDefault()
            toggle()
          }}
        >
          <div className="nav_mobile-line-wrapper">
            <div className="nav_mobile-btn-line cc-top" />
            <div className="nav_mobile-btn-line cc-middle" />
            <div className="nav_mobile-btn-line cc-bottom" />
          </div>
          <div className="u-sr-only">Menu</div>
        </a>

        <div ref={menuRef} className={`nav_menu${mounted ? ' is-open' : ''}`}>
          <div className="nav_menu-card">
            {/* Primary link group — absent on `/`, which is why
                `.nav_menu-card`'s space-between has nothing to separate
                there. */}
            {!isHome && (
              <div className="nav_links-parent">
                {NAV_LINKS.map((l) => (
                  <NavContentLink
                    key={l.to}
                    to={l.to}
                    label={l.label}
                    onNavigate={close}
                  />
                ))}
              </div>
            )}

            {/* The original points these at app.withotter.com with
                target=_blank; we host the auth screens locally, so they route
                in-app on every chrome, homepage included. Classes, DOM order
                and copy are unchanged — only the href and the dropped
                target/rel differ, so the geometry audit still holds. */}
            <div className="nav_links-parent cc-buttons">
              <Link to="/log-in" onClick={close} className="nav_link cc-log-in">
                Log in
              </Link>
              <a
                href="https://app.withotter.com/sign-up"
                target="_blank"
                rel="noreferrer"
                onClick={close}
                className="btn cc-white w-button"
              >
                Sign up
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* click-to-close, per the inline jQuery in §7.3 */}
      <div
        className={`nav_menu-overlay${mounted ? ' is-open' : ''}`}
        onClick={close}
      />
    </nav>
  )
}
