import { useState } from 'react'

/**
 * /trust-safety video — SPEC_parents_sitters_trust.md §7 + asset manifest §3.
 *
 * The original is a cross-origin embedly -> Vimeo click-to-play facade: there
 * is no <video> element anywhere on the route and nothing autoplays. The
 * iframe interior (poster crop, play button, player chrome) was explicitly
 * NOT measurable, so only the outer box is spec-exact:
 *   .u-aspect-9x16  — ivory, 56% ratio, 32px radius (16px <=767), isolate
 *   inner wrapper   — inline padding-top:56.27659574468085%, as in the DOM
 *
 * The embedly URL carries the original site's embedly account key, which the
 * manifest says not to reuse, so this embeds player.vimeo.com directly and
 * only after a click. Autoplay is therefore user-initiated, never on load.
 */
const VIMEO_ID = '705608326'
const VIMEO_HASH = '131a48dcba'
const POSTER =
  '/img/trust-video-poster.jpg'

export default function VideoFacade() {
  const [playing, setPlaying] = useState(false)

  return (
    <div className="u-aspect-9x16">
      <div
        style={{ paddingTop: '56.27659574468085%' }}
        className="u-img-cover w-video w-embed"
      >
        {playing ? (
          <iframe
            title="Trust and Safety at Otter"
            src={`https://player.vimeo.com/video/${VIMEO_ID}?h=${VIMEO_HASH}&app_id=122963&autoplay=1`}
            scrolling="no"
            allow="autoplay; fullscreen; picture-in-picture"
            allowFullScreen
          />
        ) : (
          <button
            type="button"
            className="video-facade"
            aria-label="Play video: Trust and Safety at Otter"
            onClick={() => setPlaying(true)}
          >
            <img
              src={POSTER}
              alt=""
              loading="lazy"
              className="video-facade_poster"
            />
            <span className="video-facade_play" aria-hidden="true">
              <svg width="20" height="24" viewBox="0 0 20 24" fill="none">
                <path d="M19 10.27a2 2 0 0 1 0 3.46L3 22.99a2 2 0 0 1-3-1.73V2.74A2 2 0 0 1 3 1.01l16 9.26Z" fill="currentColor" />
              </svg>
            </span>
          </button>
        )}
      </div>
    </div>
  )
}
