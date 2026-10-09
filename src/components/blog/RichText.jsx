// SPEC_blog_legal.md §3.4 — `div.blog-rich-text.w-richtext`, the post body.
//
// Type facts that are easy to get wrong:
//   • Paragraphs are BASE body type — 16px/24px weight 500, identical at 1440,
//     1024 and 390. NOT `.paragraph-1-25`. No class on the <p> at all.
//   • The measure (786.66 / 601.06 / 351px) comes from the surrounding
//     `.col.col-lg-8` inside `.container.cc-narrow`. `.blog-rich-text` has no
//     max-width of its own.
//   • `h3` gets a flat `margin-top: 4rem` (rem, not em) so the 64px does NOT
//     shrink on mobile, while its `margin-bottom: .3em` does.
//   • Every `h3` in the original body is wrapped in `<strong>`, which bumps
//     600 → 700. Reproduced here deliberately — it is the computed result on
//     the original, not an accident of our markup.
//   • First child margin-top and last child margin-bottom are forced to 0 by
//     the global embed rules in blog.css.
//
// Renders the structured blocks from src/data/posts.js. Unknown block types are
// skipped rather than guessed at.
export default function RichText({ blocks }) {
  return (
    <div className="blog-rich-text w-richtext">
      {blocks.map((block, i) => {
        switch (block.type) {
          case 'p':
            return <p key={i}>{block.text}</p>
          case 'h3':
            return (
              <h3 key={i}>
                <strong>{block.text}</strong>
              </h3>
            )
          case 'h4':
            return (
              <h4 key={i}>
                <strong>{block.text}</strong>
              </h4>
            )
          // DEVIATION, flagged in §3.4: the original fakes bullets with <br>
          // and a literal " - " inside a single <p>. We author semantic lists
          // instead, which changes the vertical rhythm of those passages
          // (disc marker, 35.2px indent, 4.8px between items).
          case 'ul':
            return (
              <ul key={i}>
                {block.items.map((item, j) => (
                  <li key={j}>{item}</li>
                ))}
              </ul>
            )
          case 'ol':
            return (
              <ol key={i}>
                {block.items.map((item, j) => (
                  <li key={j}>{item}</li>
                ))}
              </ol>
            )
          default:
            return null
        }
      })}
    </div>
  )
}
