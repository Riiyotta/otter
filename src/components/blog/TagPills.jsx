// SPEC_blog_legal.md §2.3 — the CMS tag list.
//
// The original nests two `.blog_item-tags-wrapper`s: a static outer wrapper and
// an inner `div[role=list].w-dyn-items`. Both get `display:flex;gap:8px`, so it
// behaves as a single row. Mirrored here so the DOM matches 1:1.
//
// `color` is a CMS field written onto the pill as a real HTML attribute; the
// `.tag[color='…']` map in blog.css recolours from it. `midnight` is the only
// token that also flips the foreground.
export default function TagPills({ tags }) {
  return (
    <div className="blog_item-tags-wrapper">
      <div className="w-dyn-list">
        <div role="list" className="blog_item-tags-wrapper w-dyn-items">
          {tags.map((tag) => (
            <div
              role="listitem"
              className="tag w-dyn-item"
              color={tag.color}
              key={tag.name}
            >
              <div>{tag.name}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
