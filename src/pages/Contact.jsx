import { useState } from 'react'
import '../styles/faq-contact-careers.css'

/* /contact — "Contact us"  (SPEC_faq_contact_careers.md §4)

   The original's <form> has method="get" and NO action: Webflow's
   webflow.js intercepts submit and AJAX-posts to Webflow's own endpoint.
   There is no endpoint to clone, so submit is handled locally: default is
   prevented, no network call is made, and the custom `.form-success` block
   replaces the form the way Webflow's `.w-form-done` does. The
   `.form-error` / `.w-form-fail` block is ported and kept in the DOM but
   can never fire locally (nothing can fail). Native HTML validation stays
   active — the original has no `novalidate`, and the browser validates
   before the submit event, so the three required fields still block.

   There is no author-written error styling anywhere on the original
   (verified across the whole CSSOM) — none is invented here. */

/* Inline icon SVGs (§4.5) — not network assets. Each is two paths: a body
   filled `currentColor` (resolves to --celeste inside `.contact-info_icon`)
   plus a hard-coded #00373E detail layer. Path data from the live markup. */
const ENVELOPE_PATHS = [
  'M1.64372 21.4512C1.88188 23.3668 3.42844 24.8796 5.3483 25.08C8.13886 25.3716 11.0331 25.6844 14.0001 25.6844C16.967 25.6844 19.8612 25.3716 22.6518 25.08C24.5716 24.8796 26.1182 23.3668 26.3564 21.4512C26.6558 19.0436 26.9552 16.5517 26.9552 14C26.9552 11.4483 26.6558 8.95647 26.3564 6.54879C26.1182 4.63321 24.5716 3.12051 22.6518 2.91999C19.8612 2.62851 16.967 2.31567 14.0001 2.31567C11.0331 2.31567 8.13886 2.62851 5.3483 2.91999C3.42842 3.12051 1.88188 4.63321 1.64371 6.54879C1.34436 8.95647 1.04492 11.4483 1.04492 14C1.04492 16.5517 1.34436 19.0436 1.64372 21.4512Z',
  'M1.5166 7.58946L10.7504 14.87C12.6568 16.3731 15.3451 16.3731 17.2515 14.87L26.4851 7.58962C26.4429 7.24098 26.4001 6.89402 26.3571 6.54878C26.2849 5.96764 26.0921 5.42358 25.8053 4.942L15.7036 12.9068C14.705 13.6942 13.2968 13.6942 12.2983 12.9068L2.19645 4.94188C1.90944 5.4235 1.71674 5.9676 1.64448 6.54878C1.60156 6.89396 1.55864 7.24088 1.5166 7.58946Z',
]

const PIN_PATHS = [
  'M2 10.2385C2 4.58396 6.58393 0 12.2385 0C17.8932 0 22.4771 4.58396 22.4771 10.2385C22.4771 13.9073 20.584 16.9934 18.5256 19.2709C16.4609 21.5556 14.1538 23.1123 13.1504 23.7371C12.5875 24.0876 11.8896 24.0876 11.3267 23.7371C10.3233 23.1123 8.01622 21.5556 5.95145 19.2709C3.89313 16.9934 2 13.9073 2 10.2385Z',
  'M12.25 15C14.7353 15 16.75 12.9853 16.75 10.5C16.75 8.01471 14.7353 6 12.25 6C9.76471 6 7.75 8.01471 7.75 10.5C7.75 12.9853 9.76471 15 12.25 15Z',
]

export default function Contact() {
  const [submitted, setSubmitted] = useState(false)

  // No endpoint exists; show the success card locally.
  function handleSubmit(event) {
    event.preventDefault()
    setSubmitted(true)
  }

  return (
    <>
      <header className="section">
        <div className="container cc-narrow">
          <div className="row row-justify-between row-align-center">
            <div className="col col-lg-5 col-md-7 col-sm-11 u-mb-0">
              <div className="section-header">
                {/* `.u-mb-0` also sets font-weight:400, so this requests
                    Reckless Neue 400 while only the 900 Heavy face is
                    hosted. The synthesised face IS the original's look. */}
                <h1 className="u-mb-0">Contact us</h1>
                <p className="paragraph-1-25 u-mb-0">
                  Otter matches parents who need care with trusted sitters in their community, on
                  demand.
                </p>
              </div>
            </div>
            <div className="col u-mb-0 col-lg-5 col-sm-hide">
              <div>
                <div className="u-aspect-1x1">
                  <img
                    src="/img/Contact-Hero.webp"
                    srcSet="/img/Contact-Hero-p-500.png 500w, /img/Contact-Hero-p-800.png 800w, /img/Contact-Hero.webp 910w"
                    sizes="(max-width: 767px) 100vw, (max-width: 991px) 33vw, 35vw"
                    loading="lazy"
                    alt=""
                    className="u-img-cover"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main id="main">
        <section className="section">
          <div className="container cc-narrow">
            <h2 className="u-sr-only">Form</h2>
            <div className="row row-justify-between">
              <div className="col col-lg-7 col-md-12">
                <div className="u-mb-0 w-form">
                  <form
                    id="wf-form-Contact-Form"
                    name="wf-form-Contact-Form"
                    data-name="Contact Form"
                    method="get"
                    className="form"
                    aria-label="Contact Form"
                    onSubmit={handleSubmit}
                    style={submitted ? { display: 'none' } : undefined}
                  >
                    <div className="row">
                      <div className="col col-lg-6 col-xs-12">
                        <div className="input-group">
                          <label htmlFor="First-Name" className="input-label">
                            First Name*
                          </label>
                          <input
                            className="input w-input"
                            maxLength={256}
                            name="First-Name"
                            data-name="First Name"
                            placeholder="e.g. Jane"
                            type="text"
                            id="First-Name"
                            required
                          />
                        </div>
                      </div>
                      <div className="col col-lg-6 col-xs-12">
                        <div className="input-group">
                          {/* id/name mismatch is reproduced from the original:
                              id="Last-Name-2", name="Last-Name". The label's
                              `for` points at the id, so the association is
                              correct. */}
                          <label htmlFor="Last-Name-2" className="input-label">
                            Last name*
                          </label>
                          <input
                            className="input w-input"
                            maxLength={256}
                            name="Last-Name"
                            data-name="Last Name"
                            placeholder="e.g. Doe"
                            type="text"
                            id="Last-Name-2"
                            required
                          />
                        </div>
                      </div>
                      <div className="col col-lg-6 col-xs-12">
                        <div className="input-group">
                          <label htmlFor="Email" className="input-label">
                            Email*
                          </label>
                          <input
                            className="input w-input"
                            maxLength={256}
                            name="Email"
                            data-name="Email"
                            placeholder="hello@withotter.com"
                            type="email"
                            id="Email"
                            required
                          />
                        </div>
                      </div>
                      <div className="col col-lg-6 col-xs-12">
                        <div className="input-group">
                          <label htmlFor="Phone" className="input-label">
                            Phone
                          </label>
                          <input
                            className="input w-input"
                            maxLength={256}
                            name="Phone"
                            data-name="Phone"
                            placeholder="(123) 456-7890"
                            type="tel"
                            id="Phone"
                          />
                        </div>
                      </div>
                      <div className="col u-mb-0">
                        <div className="input-group cc-textarea">
                          <label htmlFor="Comments" className="input-label">
                            Comments
                          </label>
                          <textarea
                            id="Comments"
                            name="Comments"
                            maxLength={5000}
                            data-name="Comments"
                            placeholder="Leave us a message..."
                            className="input cc-text-area w-input"
                          />
                        </div>
                      </div>
                    </div>
                    <input
                      type="submit"
                      data-wait="Please wait..."
                      className="btn u-mt-1 w-button"
                      value="Submit"
                    />
                    <div className="form_required-note">*Required</div>
                  </form>

                  <div
                    className="form-success w-form-done"
                    tabIndex={-1}
                    role="region"
                    aria-label="Contact Form success"
                    style={submitted ? { display: 'block' } : undefined}
                  >
                    <div className="form-success_flex">
                      <div className="trust-card_icon">
                        <img src="/img/safety.webp" loading="lazy" alt="Dedicated support" />
                      </div>
                      <h4 className="u-mb-0">Thanks for reaching out! We’ll be in touch soon.</h4>
                    </div>
                  </div>

                  {/* Ported for fidelity; unreachable locally (no network call). */}
                  <div
                    className="form-error w-form-fail"
                    tabIndex={-1}
                    role="region"
                    aria-label="Contact Form failure"
                  >
                    <div>Oops! Something went wrong while submitting the form.</div>
                  </div>
                </div>
              </div>

              <div className="col col-lg-4 col-md-12">
                <div className="contact-info">
                  <div className="contact-info_icon">
                    <div className="icon-wrap-24">
                      <div className="w-embed">
                      <svg
                        width="100%"
                        height="100%"
                        viewBox="0 0 28 28"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                        aria-hidden="true"
                      >
                        <path d={ENVELOPE_PATHS[0]} fill="currentColor" />
                        <path d={ENVELOPE_PATHS[1]} fill="#00373E" />
                      </svg>
                      </div>
                    </div>
                  </div>
                  <div className="conta-info_emails">
                    <a href="mailto:support@withotter.com">support@withotter.com</a>
                    <a href="mailto:media@withotter.com">media@withotter.com</a>
                  </div>
                </div>
                <div className="contact-info">
                  <div className="contact-info_icon">
                    <div className="icon-wrap-24">
                      <div className="w-embed">
                      <svg
                        width="100%"
                        height="100%"
                        viewBox="0 0 24 24"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                        aria-hidden="true"
                      >
                        <path d={PIN_PATHS[0]} fill="currentColor" />
                        <path d={PIN_PATHS[1]} fill="#00373E" />
                      </svg>
                      </div>
                    </div>
                  </div>
                  <div className="conta-info_emails">
                    <div>San Francisco, CA 94114</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </>
  )
}
