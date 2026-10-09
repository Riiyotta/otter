import '../styles/blog.css'
import { featuredPost, listPosts } from '../data/posts.js'
import PostCard from '../components/blog/PostCard.jsx'
import LoadMore from '../components/blog/LoadMore.jsx'
import CtaBand from '../components/blog/CtaBand.jsx'

// /blog — CMS collection list. DOM order per SPEC_blog_legal.md §2.1.
// Nav, Footer and ClipPathDefs come from <Layout chrome="site">.
//
// There is no category filter, no tab bar and no search on this page (§2.1);
// the single "Load more" pill is the only control. No `.w-dyn-empty` block
// exists in the original markup for either list, so none is rendered.
//
// Grid: plain `.row`/`.col` flex — no CSS grid, no `gap`. The 40px gutter and
// 40px row gap come entirely from `.col{padding-inline:20px;margin-bottom:40px}`
// over `.row{margin-inline:-20px}`. 3-up at both 1440 and 1024 (1024 is >991 so
// it keeps desktop styles), 1-up at 390.
export default function Blog() {
  return (
    <>
      {/* §2.2 — `.u-p-0` zeroes the section padding at all three widths. */}
      <header className="section u-p-0">
        <div className="container cc-narrow">
          <div className="row row-justify-between row-align-center">
            <div className="col col-lg-5 col-md-7 col-sm-11 col-xs-12">
              <div className="section-header">
                {/* `.u-mb-0` also declares font-weight:400, so this computes
                    Reckless Neue 400, not 900 — only the 900 Heavy file is
                    hosted, so the browser synthesises a lighter face. That IS
                    the original's look; it is not a bug to fix. */}
                <h1 className="u-mb-0">Adventures with Otter</h1>
                <p className="paragraph-1-25 u-mb-0">
                  From parenting hacks to homemade slime recipes – we&apos;ve thought of everything
                  childcare so you don&apos;t have to.
                </p>
              </div>
            </div>
            <div className="col u-mb-0 col-lg-5 col-sm-12">
              {/* Bare <img>: no wrapper, no object-fit. Renders at its natural
                  1983×1752 aspect, width-limited by the column.
                  `alt=""` confirmed against the live DOM — the original's alt is
                  the empty string, so it is decorative beside the h1.
                  The single-candidate `srcset` + the original's `sizes` string
                  are load-bearing, not decoration: with `w` descriptors the
                  browser density-corrects the intrinsic width to the `sizes`
                  value, which is what makes the original render 358.39px wide
                  at 1024 instead of filling the 360.64px column. Without them
                  the clone was 2.25px wider / 1.8px taller there. */}
              <img
                src="/img/Blog-Hero.webp"
                srcSet="/img/Blog-Hero.webp 1983w"
                sizes="(max-width: 479px) 90vw, (max-width: 767px) 85vw, (max-width: 991px) 33vw, 35vw"
                alt=""
                loading="lazy"
              />
            </div>
          </div>
        </div>
      </header>

      <main id="main">
        <section className="section">
          <h2 className="u-sr-only">Blog posts</h2>
          <div className="container">
            {/* Featured list (limit 1). `.u-mb-2` = 32px, on top of the col's
                own 40px bottom margin. */}
            <div className="w-dyn-list">
              <div role="list" className="row u-mb-2 w-dyn-items">
                <div role="listitem" className="col col-lg-12 w-dyn-item">
                  <PostCard post={featuredPost} featured />
                </div>
              </div>
            </div>

            {/* Main list — 9 standard cards. The featured post is not
                duplicated here, so page 1 is 1 + 9 = all 10 posts. */}
            <div className="w-dyn-list">
              <div role="list" className="row w-dyn-items">
                {listPosts.map((post) => (
                  <div
                    role="listitem"
                    className="col col-lg-4 col-md-6 col-sm-12 w-dyn-item"
                    key={post.slug}
                  >
                    <PostCard post={post} />
                  </div>
                ))}
              </div>

              <LoadMore />
            </div>
          </div>
        </section>

        <CtaBand />
      </main>
    </>
  )
}
