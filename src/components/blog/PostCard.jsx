import { Link } from 'react-router-dom'
import TagPills from './TagPills.jsx'

// SPEC_blog_legal.md §2.3 — the post card, both variants.
//
// Shared parts, two variants:
//   • featured (`cc-featured`): 50/50 row, 64px gap, static celeste "Featured"
//     pill, title is `h3.h3` (56px/67.2px w600). Column + 16px gap at ≤991.
//   • standard: column, 16px gap, CMS tag pills, title is `h3.h4.u-mb-0`
//     (40px/44px w600, 20px/24px at ≤479).
//
// Both variants put `cc-featured` on the aspect div, so BOTH are 4:3 — there is
// no 1:1 card on these routes even though `.blog_item-image-aspect` defaults to
// 1:1. Not a typo; §2.3 calls it out explicitly.
//
// The card has NO hover state and NO transition (§2.3, verified against every
// :hover rule in the compiled stylesheet and against computed `transition:
// all 0s`). The only interactive affordance is the focus ring on `.u-link-cover`.
// Do not add one. Nothing here needs motion either — §6 confirms zero
// scroll-reveal on these routes.
export default function PostCard({ post, featured = false }) {
  return (
    <div className={featured ? 'blog_item cc-featured' : 'blog_item'}>
      <div className={featured ? 'blog_item-image cc-featured' : 'blog_item-image'}>
        <div className="blog_item-image-aspect cc-featured">
          {/* `.u-img-cover` is object-fit: CONTAIN, so covers letterbox rather
              than crop. Matches the homepage primitive. */}
          <img className="u-img-cover" src={post.cover} alt={post.alt} loading="lazy" />
        </div>
      </div>

      <div className={featured ? 'blog_heading-wrapper cc-featured' : 'blog_heading-wrapper'}>
        {featured ? (
          // Hand-authored static pill, not a CMS tag list — celeste default.
          <div className="blog_item-tags-wrapper">
            <div className="tag">
              <div>Featured</div>
            </div>
          </div>
        ) : (
          <TagPills tags={post.tags} />
        )}
        <h3 className={featured ? 'h3' : 'h4 u-mb-0'}>{post.title}</h3>
      </div>

      {/* Whole-card overlay link; the visible title is the h3, so the link's own
          label is screen-reader-only (the original repeats the title here). */}
      <Link className="u-link-cover w-inline-block" to={`/blog-posts/${post.slug}`}>
        <div className="u-sr-only">{post.title}</div>
      </Link>
    </div>
  )
}
