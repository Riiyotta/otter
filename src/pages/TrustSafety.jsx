import PageHero from "../components/pst/PageHero.jsx";
import VideoFacade from "../components/pst/VideoFacade.jsx";
import "../styles/parents-sitters-trust.css";

// DOM order per SPEC_parents_sitters_trust.md §1 (/trust-safety):
// hero header → main[ one section: video block + 4 trust cards ].
// No tabs, no CTA card, no testimonials slider, no "Common questions".

const TRUST_CARDS = [
  {
    key: "universal-background-check",
    heading: "Universal background check",
    body: "Every member of the Otter community, including parents and sitters, is background checked so we can foster a safe and trustworthy community.",
    icon: {
      src: "/img/universal-screening.webp",
      srcSet:
        "/img/universal-screening-p-500.webp 500w, /img/universal-screening.webp 615w",
      sizes: "(max-width: 479px) 32vw, 104px",
      alt: "Background Check",
    },
  },
  {
    key: "dedicated-support",
    heading: "Dedicated Support",
    body: "Our support team is on standby during active care sessions. We're prepared to respond to any questions or concerns that come up before, during, or after a care session.",
    icon: { src: "/img/safety.webp", alt: "Dedicated support" },
  },
  {
    key: "payment-protection",
    heading: "Payment Protection",
    body: "Booking care? Our secure platform protects your payments. Providing care? Our cancellation and late arrivals policies ensure you get paid even if unexpected changes occur.",
    // width="96" is an HTML attribute in the source, which is why this icon
    // renders narrower than the 104px .trust-card_icon cap.
    icon: { src: "/img/payment.webp", alt: "Payment Protection", width: 96 },
  },
  {
    key: "healthy-care-standards",
    heading: "Healthy Care Standards",
    body: "Otter's healthy care guidelines are designed to promote the health of children, sitters, and parents. We stay up to date on the latest guidance from public health authorities, helping you make the best decisions for your family.",
    // alt text typo ("Standars") preserved from the source.
    icon: { src: "/img/health.webp", alt: "Healthy Care Standars" },
  },
];

function TrustCard({ card }) {
  return (
    <div className="col col-lg-5 col-md-6 col-sm-12">
      <div className="trust-card">
        <div className="trust-card_icon">
          <img
            src={card.icon.src}
            srcSet={card.icon.srcSet}
            sizes={card.icon.sizes}
            width={card.icon.width}
            alt={card.icon.alt}
            loading="lazy"
          />
        </div>
        <div className="trust-card_header">
          <h3 className="trust-bar_header">{card.heading}</h3>
          <p className="u-mb-0">{card.body}</p>
        </div>
      </div>
    </div>
  );
}

export default function TrustSafety() {
  return (
    <>
      <PageHero
        rowClassName="row row-align-center row-justify-between"
        copyColClassName="col col-lg-6 col-sm-10 col-xs-12"
        topShape={{
          className: "shape footer-shape-left",
          img: { src: "/img/FAQ.webp", alt: "Kid playing with puzzle toy" },
        }}
        bottomShape={{ className: "shape stone-hero_top-left u-bg-sandstone" }}
      >
        <h1>Complete kidcare peace of mind</h1>
        {/* `.paragraph-1-5` is text-align:center with margin-bottom:24px even
            inside this left-aligned hero — reproduced as measured (spec §2.3). */}
        <p className="paragraph-1-5">
          Our top priority is safety – providing your little ones with a safe
          and trustworthy environment.
        </p>
        <div className="buttons-wrapper">
          <a
            href="https://app.withotter.com/sign-up/welcome"
            target="_blank"
            rel="noreferrer"
            className="btn w-button"
          >
            Become a caregiver
          </a>
          <a
            href="https://app.withotter.com/sign-up/welcome"
            target="_blank"
            rel="noreferrer"
            className="btn cc-light w-button"
          >
            Find childcare
          </a>
        </div>
      </PageHero>

      <main id="main">
        <section className="section">
          <div className="container cc-narrow">
            <div className="u-mb-2">
              <div className="row row-justify-center row-md-justify-start row-align-end">
                <div className="col col-lg-10 col-md-12">
                  {/* .section-header wraps only the h2 here; the lede and the
                      video are its siblings inside .trust-content. */}
                  <div className="trust-content">
                    <div className="section-header">
                      <h2 className="h3 u-mb-0">
                        High-quality childcare, without question
                      </h2>
                    </div>
                    <p className="paragraph-1-25 u-mb-0">
                      Our community of caregivers is made up of highly vetted
                      sitters who have been selected based on their ability to
                      create a safe environment for your children. We can
                      confidently say, we'd leave our own kids with Otter in a
                      heartbeat.
                    </p>
                    <VideoFacade />
                  </div>
                </div>
              </div>
            </div>

            {/* 2 rows of 2 cards, not one 4-up wrap. */}
            <div className="u-mt-1">
              <div className="row row-justify-center">
                {TRUST_CARDS.slice(0, 2).map((card) => (
                  <TrustCard card={card} key={card.key} />
                ))}
              </div>
              <div className="row row-justify-center">
                {TRUST_CARDS.slice(2).map((card) => (
                  <TrustCard card={card} key={card.key} />
                ))}
              </div>
            </div>
          </div>
        </section>
      </main>
    </>
  );
}
