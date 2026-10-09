import LegalDocument from '../components/legal/LegalDocument.jsx'
import { termsOfUse } from '../data/legal/terms.js'
import '../styles/legal.css'

/**
 * /terms-of-use — spec/SPEC_blog_legal.md §4.
 * Nav + Footer come from Layout (chrome="site"); this renders page content only.
 */

/**
 * Link repairs for this route. The document copy in src/data/legal/terms.js is
 * verbatim, so every deviation from the original's hrefs is declared here.
 *
 * 1. `https://withotter.com/privacy` — dead on the live site (the real page is
 *    /privacy-policy). Remapped to the local route, which is unambiguous and
 *    keeps the clone self-contained rather than pointing at the live domain.
 *
 * 2. The one in-body `href="#"` placeholder, labelled "www.jamsadr.com", is
 *    LEFT INERT. The intended destination is guessable, but this sits inside
 *    the binding-arbitration clause and synthesising an outbound URL there is a
 *    legal-content decision, not a build decision. Flagged for content review.
 */
function resolveHref(href) {
  if (href === 'https://withotter.com/privacy') return '/privacy-policy'
  return href
}

export default function TermsOfUse() {
  return <LegalDocument title="Terms of use" doc={termsOfUse} resolveHref={resolveHref} />
}
