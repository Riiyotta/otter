import PageHero from "../components/pst/PageHero.jsx";
import Tabs from "../components/pst/Tabs.jsx";
import CtaCard from "../components/pst/CtaCard.jsx";
import TestimonialsSlider from "../components/pst/TestimonialsSlider.jsx";
import CommonQuestions from "../components/pst/CommonQuestions.jsx";
import "../styles/parents-sitters-trust.css";

// DOM order per SPEC_parents_sitters_trust.md §1 (/sitters). The CTA here is a
// plain `section.section` with `.cc-wide-cta` on the inner container, unlike
// /parents which wraps it in `section.section.u-p-0.u-mb-3`.

const TAB_ITEMS = [
  {
    key: "sign-up",
    label: "Sign up",
    body: "Tell us about yourself, your availability, and your childcare experience. We'll have you pass a background check to ensure a trustworthy, reliable community of sitters.",
    img: {
      src: "/img/sitters-sign-up-2.webp",
      srcSet:
        "/img/sitters-sign-up-2-p-500.webp 500w, /img/sitters-sign-up-2.webp 528w",
      alt: "Woman checking phone",
    },
  },
  {
    key: "find-and-book-jobs",
    // Non-breaking space before "book", as in the source.
    label: "Find & book jobs",
    body: "We’ll match you with families and situations that fit your schedule, situation and experience. Care requests will come your way from parents that could use a hand.",
    img: {
      src: "/img/Sitters---Find-&-Book-Jobs.webp",
      srcSet:
        "/img/Sitters---Find-&-Book-Jobs-p-500.webp 500w, /img/Sitters---Find-&-Book-Jobs.webp 528w",
      alt: "Kid toys",
    },
  },
  {
    key: "give-care-and-get-paid",
    // Non-breaking space before "get", as in the source.
    label: "Give care & get paid",
    body: "When it’s time, head over to your family's place to give care. You'll receive payment for your time and care the Friday following your bookings.",
    img: {
      src: "/img/Sitters---Care-an-get-paid.webp",
      srcSet:
        "/img/Sitters---Care-an-get-paid-p-500.webp 500w, /img/Sitters---Care-an-get-paid.webp 528w",
      alt: "Kid having breakfast",
    },
  },
];

export default function Sitters() {
  return (
    <>
      <PageHero
        rowClassName="row row-justify-between row-align-center"
        copyColClassName="col col-lg-6 col-sm-12"
        topShape={{
          className: "shape stone-hero_bottom-right",
          img: {
            src: "/img/Sitters.webp",
            alt: "Kid playing with puzzle toys",
          },
        }}
        bottomShape={{ className: "shape stone-hero_middle-left u-bg-peach" }}
      >
        {/* `.u-mb-0` makes this h1 compute font-weight:400 / margin-bottom:0.
            Only RecklessNeue-Heavy (900) is self-hosted, so the browser still
            renders the 900 face — that is the original's look (spec §5). */}
        <h1 className="u-mb-0">Become a sitter, on your own time</h1>
        <p className="paragraph-1-25 u-mb-0">
          Otter is the childcare solution created for the people who need it as
          much as the people who provide it. We connect sitters with families
          who are in a pinch and need backup care.
        </p>
        <a
          href="https://app.withotter.com/sign-up/welcome"
          target="_blank"
          rel="noreferrer"
          className="btn w-button"
        >
          Join us
        </a>
      </PageHero>

      <main id="main">
        <section className="section">
          <div className="container cc-narrow">
            <Tabs
              eyebrow="how it works"
              heading="Be the extra set of hands every family needs"
              lede="Join us in making parents lives easier. Just follow these steps and you'll be all set to care with Otter."
              items={TAB_ITEMS}
            />
          </div>
        </section>

        <section className="section">
          <CtaCard
            wide
            heading="Make people’s day with kind, compassionate kidcare."
            ctaLabel="Sign up"
            imageContainClassName="cta-image-contain cc-extra-wide"
            imageAspectClassName="cta-image-aspect cc-wide"
            blobClassName="shape footer-shape-right u-bg-celeste"
            image={{
              src: "/img/holding-hands.webp",
              srcSet:
                "/img/holding-hands-p-500.webp 500w, /img/holding-hands-p-800.webp 800w, /img/holding-hands.webp 1445w",
              sizes:
                "(max-width: 479px) 90vw, (max-width: 767px) 85vw, (max-width: 991px) 76vw, 45vw",
              alt: "Illustration of a kid and sitter holding hands",
            }}
          />
        </section>

        <TestimonialsSlider
          heading="What our sitters are saying"
          lede="Otter sitters make $17/hour and up on average."
        />

        <CommonQuestions />
      </main>
    </>
  );
}
