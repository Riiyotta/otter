import { Link } from 'react-router-dom'

/**
 * Renders the inline run model used by src/data/legal/*.js.
 *
 * A run is one of:
 *   - a string                                  → a text node
 *   - { br: true }                              → <br />
 *   - { tag, children, href?, target?, id? }    → an inline element
 *
 * The data files reproduce the live DOM's `<br>`-separated pseudo-lists
 * verbatim (the original pages contain zero ul/ol/li/table), so this renderer
 * deliberately does nothing clever: no list detection, no " - " rewriting.
 *
 * `resolveHref(href, label)` lets a page remap the original's placeholder
 * `href="#"` links without editing the verbatim copy. It returns either a
 * string href or null to leave the link inert.
 */
export default function InlineRuns({ runs, resolveHref }) {
  return (
    <>
      {runs.map((run, i) => (
        <Run key={i} run={run} resolveHref={resolveHref} />
      ))}
    </>
  )
}

function Run({ run, resolveHref }) {
  if (typeof run === 'string') return run
  if (run.br) return <br />

  const children = <InlineRuns runs={run.children || []} resolveHref={resolveHref} />

  if (run.tag === 'a') {
    const label = plainText(run.children)
    const href = resolveHref ? resolveHref(run.href, label) : run.href

    // Internal route → react-router <Link> so navigation stays client-side.
    if (href && href.startsWith('/')) {
      return (
        <Link to={href} id={run.id}>
          {children}
        </Link>
      )
    }

    return (
      <a href={href || '#'} target={run.target} id={run.id}>
        {children}
      </a>
    )
  }

  const Tag = run.tag
  return <Tag id={run.id}>{children}</Tag>
}

/** Flattens a run list to its text content (used to identify a link by label). */
export function plainText(runs = []) {
  return runs
    .map((r) => {
      if (typeof r === 'string') return r
      if (r.br) return ''
      return plainText(r.children)
    })
    .join('')
}
