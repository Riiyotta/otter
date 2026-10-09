import LegalDocument from '../components/legal/LegalDocument.jsx'
import { privacyPolicy } from '../data/legal/privacy.js'
import '../styles/legal.css'

/**
 * /privacy-policy — spec/SPEC_blog_legal.md §4.
 * Nav + Footer come from Layout (chrome="site"); this renders page content only.
 */

/**
 * Link repairs for this route. The document copy in src/data/legal/privacy.js
 * is verbatim, so every deviation from the original's hrefs is declared here.
 *
 * DELIBERATE DEVIATION — broken anchor fixed.
 * The live page has exactly one anchor target,
 * `<strong id="information-we-collect-automatically">`, and a link in a later
 * section whose label points back at it — but the live `href` is `"#"`, so the
 * anchor is orphaned and the link is genuinely broken on withotter.com.
 * Recon flagged it as reproduce-or-fix-deliberately; we FIX it by wiring the
 * link to the id that already exists. Purely a navigation repair: no visual
 * difference, no copy change.
 *
 * `scroll-behavior` stays `auto` (no smooth scroll on these routes), and this
 * is still the only id in the document — no TOC, no jump-link list was added.
 */
function resolveHref(href, label) {
  if (href === '#' && /Information We Collect Automatically/i.test(label)) {
    return '#information-we-collect-automatically'
  }
  return href
}

export default function PrivacyPolicy() {
  return <LegalDocument title="Privacy Policy" doc={privacyPolicy} resolveHref={resolveHref} />
}
