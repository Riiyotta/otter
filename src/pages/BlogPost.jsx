import { Link, useParams } from 'react-router-dom'
import '../styles/blog.css'
import { getPost, heroCoverFor, relatedPosts } from '../data/posts.js'
import PostCard from '../components/blog/PostCard.jsx'
import RichText from '../components/blog/RichText.jsx'

// /blog-posts/:slug — the shared CMS post template.
// DOM order per SPEC_blog_legal.md §3.1. Nav/Footer come from <Layout>.
//
// Slots that EXIST (§3.2): title, 1–3 tag pills, a forced 1:1 cover with a 32px
// radius, the rich-text body, 3 related-post cards.
//
// Slots that DO NOT exist on the original and are deliberately NOT built:
// subtitle/deck/excerpt, author block, publish date (there is not a single
// <time> element on the page), read-time, share links, breadcrumb or
// "back to blog" link, inline body CTA, next/prev post navigation.
// Recon checked the raw HTML and the live DOM on two sample posts. None of that
// data exists, so none of it is invented here.
export default function BlogPost() {
  const { slug } = useParams()
  const post = getPost(slug)

  if (!post) return <PostNotFound />

  const related = relatedPosts(slug)

  return (
    <>
      {/* §3.3 — note this is a plain div, not a <header>, on the original.
          `.u-pb-0` gives 80px 0 0 (48px 0 0 at ≤479). */}
      <div className="section u-pb-0">
        <div className="container cc-narrow">
          <div className="row row-justify-between row-align-center">
            <div className="col col-lg-6 col-sm-12">
              <div className="section-header">
                {/* `h1.h2` takes `.h2`'s 4.5rem/1.1 scale but keeps h1's
                    Reckless Neue family and -.01em tracking; `.u-mb-0` drops it
                    to weight 400. Net: Reckless Neue 400, not 900. */}
                <h1 className="h2 u-mb-0">{post.title}</h1>
                <div className="w-dyn-list">
                  <div role="list" className="blog_item-tags-wrapper w-dyn-items">
                    {post.tags.map((tag) => (
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
            </div>

            <div className="col col-lg-6 col-sm-12 u-mb-0">
              {/* Forced 1:1 square, 32px radius at every breakpoint, image
                  letterboxed by object-fit: contain. alt="" on the original. */}
              <div className="b-radius-32">
                <div className="u-aspect-1x1">
                  <img className="u-img-cover" src={heroCoverFor(post)} alt="" loading="lazy" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <main id="main">
        <div className="section">
          <div className="container cc-narrow">
            <div className="row row-justify-center">
              <div className="col col-lg-8 col-md-12">
                <RichText blocks={post.body} />
              </div>
            </div>
          </div>
        </div>

        {/* §3.5 — "Similar articles". Uses the WIDE `.container` (1296px at
            1440), not `.cc-narrow`, so the grid is wider than the prose above
            it. Deliberate on the original; kept. Exactly 3 cards, no
            "view all" link, no pagination. */}
        <div className="section">
          <div className="container">
            <h2 className="h3 u-mb-1">Similar articles</h2>
            <div className="w-dyn-list">
              <div role="list" className="row w-dyn-items">
                {related.map((item) => (
                  <div
                    role="listitem"
                    className="col col-lg-4 col-md-6 col-xs-12 w-dyn-item"
                    key={item.slug}
                  >
                    <PostCard post={item} />
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </main>
    </>
  )
}

// Our own addition — the original has no 404 state for an unknown post slug
// (Webflow serves its own site-level 404 page). Built from existing primitives
// only, with no invented visual language.
function PostNotFound() {
  return (
    <main id="main">
      <div className="section">
        <div className="container cc-narrow">
          <div className="section-header">
            <h1 className="h2 u-mb-0">We couldn&apos;t find that post.</h1>
            <p className="paragraph-1-25 u-mb-0">
              The link may be out of date. Everything we&apos;ve published is on the blog.
            </p>
            <Link className="btn w-button" to="/blog">
              Back to the blog
            </Link>
          </div>
        </div>
      </div>
    </main>
  )
}
