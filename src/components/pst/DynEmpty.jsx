/**
 * Webflow's empty-CMS-collection placeholder.
 *
 * Both CMS collections on /parents and /sitters (the testimonials slider and
 * the "Common questions" list) are empty upstream, so this grey box is what
 * the live production site actually renders — see spec §6 and §11.1. It is
 * reproduced verbatim rather than filled with invented copy.
 */
export default function DynEmpty() {
  return (
    <div className="w-dyn-empty">
      <div>No items found.</div>
    </div>
  )
}
