// ============================================================================
// Blog post data — /blog list + /blog-posts/:slug template
//
// ⚠️  ARTICLE BODIES ARE ORIGINAL PLACEHOLDER PROSE, NOT THE ORIGINAL ARTICLES.
//     Every `body` array below was written from scratch for this clone purely to
//     exercise the rich-text template's typography and vertical rhythm
//     (SPEC_blog_legal.md §3.4). None of it is transcribed from withotter.com.
//     Drop real copy in by replacing the `body` arrays — no component changes
//     are needed.
//
// Everything else IS recorded from the original:
//   • `slug`   — SPEC_blog_legal.md §2.7, the 10 posts rendered on page 1
//   • `title`  — verbatim from §2.7
//   • `tags`   — verbatim names + the CMS `color` token from §2.7 / §2.3
//   • `cover`  — the card cover, ASSETS_blog_legal.md §2
//   • `heroCover` — the 1:1 post-header cover, ASSETS_blog_legal.md §2
//
// GAP (flagged, not guessed): the post-header cover is a *separate* CMS field
// from the card cover, and recon only measured it on two posts (`series-a` →
// Backyard-Games.png, `infant-care-101` → same file as its card). For the other
// eight posts `heroCover` was unknown, so it falls back to `cover` via
// `heroCoverFor()` below.
//
// RESOLVED — all ten posts' hero covers were re-measured against the live site:
// nine of ten serve the SAME file as the card cover, so the fallback is exactly
// right and no extra assets are needed. `series-a` is the only post where the
// two fields differ (card `Playing_Colored_01 1.webp` vs hero `Backyard
// Games.png`), and that one is already pinned below. Do not re-open this.
//
// There is deliberately NO author, date, read-time, excerpt or deck field:
// SPEC §2.7 / §3.2 confirm none of that data exists on the original.
// ============================================================================

const CARD_ALT = 'Kid and sitter playing ' // single CMS default reused for all 10, trailing space included (§2.7)

// Block types understood by BlogRichText:
//   { type: 'p',  text }        → plain body paragraph (16px/24px w500)
//   { type: 'h3', text }        → subhead; rendered inside <strong> (600 → 700), as on the original
//   { type: 'ul', items: [] }   → semantic list. DEVIATION: the original fakes
//                                 lists with <br> + " - " inside a <p> (§3.4).
//                                 We author real lists; the vertical rhythm of
//                                 those passages therefore differs from source.
export const posts = [
  {
    slug: 'series-a',
    title: "Announcing Otter's Series A",
    featured: true, // → the static celeste `div.tag` reading "Featured" (§2.3)
    // Re-measured live on /blog-posts/series-a: the post header carries THREE
    // CMS pills, not one. /blog's featured card hides them behind the static
    // "Featured" pill, which is why they were missed.
    tags: [
      { name: 'Otter news', color: 'midnight' },
      { name: 'Daycare', color: 'sandstone' },
      { name: 'Parenting', color: 'coral' },
    ],
    cover: '/img/Playing_Colored_01-1.webp',
    heroCover: '/img/Backyard-Games.png', // measured (513×344 into a 580×580 slot — soft on the original too)
    alt: CARD_ALT,
    body: [
      { type: 'p', text: 'Placeholder copy. This paragraph exists to show the body measure, the 16px/24px rhythm and the 16px gap between consecutive paragraphs at every breakpoint.' },
      { type: 'p', text: 'A second paragraph follows immediately, so the spacing between two blocks of prose is visible without a subhead interrupting it.' },
      { type: 'h3', text: 'What this means for families' },
      { type: 'p', text: 'Placeholder copy under the first subhead. Note the flat 64px space above the heading, which does not shrink on narrow viewports.' },
      { type: 'p', text: 'Another paragraph keeps the block long enough that the measure wraps on every one of the three reference widths.' },
      { type: 'h3', text: 'What comes next' },
      { type: 'p', text: 'Placeholder copy under the second subhead, demonstrating the heading-to-paragraph gap.' },
      { type: 'p', text: 'A closing paragraph. The last child has its bottom margin forced to zero, so the section padding below is the only space that remains.' },
    ],
  },
  {
    slug: 'how-to-be-an-amazing-babysitter',
    title: 'How to be an Amazing Babysitter',
    tags: [
      { name: 'Childcare', color: 'midnight' },
      { name: 'Tips', color: 'peach' },
    ],
    cover: '/img/shutterstock_1770121187.jpeg',
    alt: CARD_ALT,
    body: [
      { type: 'p', text: 'Placeholder copy for the opening paragraph of this post. It sets the body measure and the base 16px/24px weight-500 rhythm.' },
      { type: 'p', text: 'A second placeholder paragraph, long enough to wrap on all three reference widths so the line length is easy to check.' },
      { type: 'h3', text: 'Before the first booking' },
      { type: 'p', text: 'Placeholder copy under the first subhead. The 64px space above it is flat and does not scale down on mobile.' },
      {
        type: 'ul',
        items: [
          'A first placeholder list item.',
          'A second placeholder list item.',
          'A third placeholder list item.',
        ],
      },
      { type: 'h3', text: 'On the day' },
      { type: 'p', text: 'Placeholder copy under the second subhead, showing the tighter heading-to-paragraph gap.' },
      { type: 'p', text: 'A closing placeholder paragraph with its bottom margin zeroed out as the last child of the rich-text block.' },
    ],
  },
  {
    slug: 'infant-care-101',
    title: 'Infant Care 101',
    tags: [
      { name: 'Childcare', color: 'midnight' },
      { name: 'Tips', color: 'peach' },
    ],
    cover: '/img/kelly-sikkema-Z4GKcFAGck4-unsplash.jpeg',
    heroCover: '/img/kelly-sikkema-Z4GKcFAGck4-unsplash.jpeg', // measured: same file as the card cover
    alt: CARD_ALT,
    body: [
      { type: 'p', text: 'Placeholder copy opening this post. The original has 26 rich-text children here — 22 paragraphs, three subheads and a trailing paragraph.' },
      { type: 'p', text: 'A second placeholder paragraph so the paragraph-to-paragraph gap is visible.' },
      { type: 'h3', text: 'Feeding' },
      { type: 'p', text: 'Placeholder copy under the first subhead.' },
      { type: 'p', text: 'A follow-on placeholder paragraph to keep the rhythm honest.' },
      { type: 'h3', text: 'Sleep' },
      { type: 'p', text: 'Placeholder copy under the second subhead.' },
      { type: 'p', text: 'A closing placeholder paragraph, last child, bottom margin zero.' },
    ],
  },
  {
    slug: 'toddler-care-101',
    title: 'Toddler Care 101',
    tags: [
      { name: 'Childcare', color: 'midnight' },
      { name: 'Tips', color: 'peach' },
    ],
    cover: '/img/kazuend-ejlRp5ktpfY-unsplash.jpeg',
    alt: CARD_ALT,
    body: [
      { type: 'p', text: 'Placeholder copy opening this post, sized and spaced per the rich-text rules.' },
      { type: 'p', text: 'A second placeholder paragraph that wraps across the full measure.' },
      { type: 'h3', text: 'Routines' },
      { type: 'p', text: 'Placeholder copy under the first subhead.' },
      { type: 'h3', text: 'Play' },
      { type: 'p', text: 'Placeholder copy under the second subhead.' },
      { type: 'p', text: 'A closing placeholder paragraph.' },
    ],
  },
  {
    slug: 'how-to-set-your-sitter-up-for-success',
    title: 'How to Set Your Sitter Up for Success',
    tags: [
      { name: 'Childcare', color: 'midnight' },
      { name: 'Parenting', color: 'coral' },
      { name: 'Tips', color: 'peach' },
    ],
    cover: '/img/marisa-howenstine-Cq9slNxV8YU-unsplash.jpeg',
    alt: CARD_ALT,
    body: [
      { type: 'p', text: 'Placeholder copy opening this post. This is the only page-1 post with three tag pills, so it is the one to check the pill wrap against.' },
      { type: 'p', text: 'A second placeholder paragraph.' },
      { type: 'h3', text: 'Share the basics' },
      { type: 'p', text: 'Placeholder copy under the first subhead.' },
      {
        type: 'ul',
        items: [
          'A first placeholder list item.',
          'A second placeholder list item.',
        ],
      },
      { type: 'h3', text: 'Stay reachable' },
      { type: 'p', text: 'Placeholder copy under the second subhead.' },
      { type: 'p', text: 'A closing placeholder paragraph.' },
    ],
  },
  {
    slug: 'otter-featured-in-the-new-york-times',
    title: 'Otter Featured in the New York Times',
    tags: [{ name: 'Otter news', color: 'midnight' }],
    cover: '/img/Screen-Shot-2022-08-31-at-8.34.51-AM.png',
    alt: CARD_ALT,
    body: [
      { type: 'p', text: 'Placeholder copy opening this post. The cover here is a screenshot asset, 866×752, letterboxed by object-fit: contain in both the 4:3 card slot and the 1:1 header slot.' },
      { type: 'p', text: 'A second placeholder paragraph.' },
      { type: 'h3', text: 'The coverage' },
      { type: 'p', text: 'Placeholder copy under the subhead.' },
      { type: 'p', text: 'A closing placeholder paragraph.' },
    ],
  },
  {
    slug: 'how-to-change-a-diaper',
    title: 'How to Change a Diaper',
    tags: [
      { name: 'Childcare', color: 'midnight' },
      { name: 'Tips', color: 'peach' },
    ],
    cover: '/img/zelle-duda-uld7AdE36z4-unsplash.jpeg',
    alt: CARD_ALT,
    body: [
      { type: 'p', text: 'Placeholder copy opening this post.' },
      { type: 'p', text: 'A second placeholder paragraph.' },
      { type: 'h3', text: 'What to have ready' },
      { type: 'p', text: 'Placeholder copy under the first subhead.' },
      {
        type: 'ul',
        items: [
          'A first placeholder list item.',
          'A second placeholder list item.',
          'A third placeholder list item.',
        ],
      },
      { type: 'h3', text: 'Step by step' },
      { type: 'p', text: 'Placeholder copy under the second subhead.' },
      { type: 'p', text: 'A closing placeholder paragraph.' },
    ],
  },
  {
    slug: 'tackling-bedtime-routines',
    title: 'Tackling Bedtime Routines',
    tags: [
      { name: 'Childcare', color: 'midnight' },
      { name: 'Tips', color: 'peach' },
    ],
    cover: '/img/mark-zamora-mFqAeaZgWO8-unsplash.jpg', // the only portrait cover (2500×3741)
    alt: CARD_ALT,
    body: [
      { type: 'p', text: 'Placeholder copy opening this post. This is the only portrait cover in the collection, so it letterboxes left and right rather than top and bottom.' },
      { type: 'p', text: 'A second placeholder paragraph.' },
      { type: 'h3', text: 'Winding down' },
      { type: 'p', text: 'Placeholder copy under the first subhead.' },
      { type: 'h3', text: 'Staying consistent' },
      { type: 'p', text: 'Placeholder copy under the second subhead.' },
      { type: 'p', text: 'A closing placeholder paragraph.' },
    ],
  },
  {
    slug: 'baby-led-bottle-feeding',
    title: 'Baby-led Bottle Feeding',
    tags: [
      { name: 'Childcare', color: 'midnight' },
      { name: 'Tips', color: 'peach' },
    ],
    cover: '/img/lucy-wolski-sljmgxyzmqM-unsplash.jpeg',
    alt: CARD_ALT,
    body: [
      { type: 'p', text: 'Placeholder copy opening this post.' },
      { type: 'p', text: 'A second placeholder paragraph.' },
      { type: 'h3', text: 'Reading the cues' },
      { type: 'p', text: 'Placeholder copy under the first subhead.' },
      { type: 'h3', text: 'Pacing the bottle' },
      { type: 'p', text: 'Placeholder copy under the second subhead.' },
      { type: 'p', text: 'A closing placeholder paragraph.' },
    ],
  },
  {
    slug: 'how-to-set-parents-at-ease-while-babysitting',
    title: 'How to Set Parents at Ease While Babysitting',
    tags: [
      { name: 'Childcare', color: 'midnight' },
      { name: 'Tips', color: 'peach' },
    ],
    cover: '/img/kelly-sikkema-4l2Ml8-MLUg-unsplash.jpeg',
    alt: CARD_ALT,
    body: [
      { type: 'p', text: 'Placeholder copy opening this post. It is the longest title in the collection, so it is the one to check the card title wrap against.' },
      { type: 'p', text: 'A second placeholder paragraph.' },
      { type: 'h3', text: 'Check in early' },
      { type: 'p', text: 'Placeholder copy under the first subhead.' },
      { type: 'h3', text: 'Leave the place better' },
      { type: 'p', text: 'Placeholder copy under the second subhead.' },
      { type: 'p', text: 'A closing placeholder paragraph.' },
    ],
  },
]

/** The featured post — §2.1's first `w-dyn-list` (limit 1). */
export const featuredPost = posts.find((p) => p.featured) ?? posts[0]

/**
 * The 9 standard cards. The featured post is NOT duplicated in this grid
 * on the original (§2.7), so page 1 renders 1 + 9 = all 10 posts.
 */
export const listPosts = posts.filter((p) => p !== featuredPost)

export function getPost(slug) {
  return posts.find((p) => p.slug === slug)
}

/** Post-header 1:1 cover, falling back to the card cover where unmeasured. */
export function heroCoverFor(post) {
  return post.heroCover ?? post.cover
}

/**
 * The 3 "Similar articles" cards (§3.5).
 *
 * DEVIATION, flagged: on the original these are collection items from pages
 * 2–4 of the 36-post collection, which do not exist in this clone. We take the
 * next 3 posts in collection order instead, so all three links resolve to real
 * routes. Exactly 3 items, no "view all" link — as on the original.
 */
export function relatedPosts(slug) {
  const i = posts.findIndex((p) => p.slug === slug)
  const pool = i === -1 ? posts : [...posts.slice(i + 1), ...posts.slice(0, i)]
  return pool.slice(0, 3)
}
