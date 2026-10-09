// SPEC_blog_legal.md §2.5 — the "Load more" pill.
//
// On the original this is Finsweet CMS Load v1 (`fs-cmsload-mode="load-under"`),
// not Webflow paging, pointed at `?77d76c3c_page=2`. The hidden
// `div.w-page-count` reads "1 / 4" → 4 pages × 9 posts.
//
// In this clone only the 10 real page-1 posts exist, so there is nothing to
// load: the pill is rendered for visual fidelity but is INERT. No extra posts
// are fabricated to give it something to reveal. `aria-disabled` + a
// preventDefault click keep it honest for assistive tech while leaving its
// appearance and `.btn:hover` colour swap untouched.
//
// The rendered metrics are a cascade accident worth preserving — see the
// `.w-pagination-next` note in src/styles/blog.css: 14px font/line-height,
// 12.25px/17.5px padding, 1386px radius, 110×40.5 box, because
// `.w-pagination-next{font-size:14px}` beats `.btn{font-size:1rem}` and `.btn`
// expresses its padding and radius in `em`.
//
// Kept from the original DOM: the `display:none` "previous" link and the
// `display:none` page count. The count still reads "1 / 4" because that is what
// the original ships; it describes the original collection, not this clone's 10
// posts, and it is never visible or exposed to the a11y tree.
export default function LoadMore() {
  return (
    <div role="navigation" aria-label="List" className="w-pagination-wrapper u-mt-3">
      <a className="w-pagination-previous u-d-none" aria-hidden="true" tabIndex={-1}>
        <div className="w-inline-block">Previous</div>
      </a>
      <a
        className="w-pagination-next btn"
        role="button"
        tabIndex={0}
        aria-disabled="true"
        onClick={(e) => e.preventDefault()}
      >
        <div className="w-inline-block">Load more</div>
      </a>
      <div className="w-page-count u-d-none">1 / 4</div>
    </div>
  )
}
