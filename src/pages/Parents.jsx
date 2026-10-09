import PageHero from "../components/pst/PageHero.jsx";
import Tabs from "../components/pst/Tabs.jsx";
import CtaCard from "../components/pst/CtaCard.jsx";
import TestimonialsSlider from "../components/pst/TestimonialsSlider.jsx";
import CommonQuestions from "../components/pst/CommonQuestions.jsx";
import "../styles/parents-sitters-trust.css";

// DOM order per SPEC_parents_sitters_trust.md §1 (/parents):
// hero header → main[ tabs section, CTA section, testimonials, common questions ].
// Nav / Footer / ClipPathDefs belong to the Layout chrome, not this page.

const TAB_ITEMS = [
  {
    key: "sign-up",
    label: "Sign up",
    body: "We like to keep it simple. Tell us your contact information and a little bit about your kids. Just like that, you're all set.",
    img: {
      src: "/img/Sign-up-2.webp",
      srcSet: "/img/Sign-up-2-p-500.webp 500w, /img/Sign-up-2.webp 528w",
      alt: "Mom holding baby, checking iPad",
    },
  },
  {
    key: "book-a-sitter",
    label: "Book a sitter",
    // Trailing space is present in the source copy.
    body: "Let us know when you need care and we'll match you with a sitter based on your family's needs and their availability. ",
    img: {
      src: "/img/home-tabs-–-book.webp",
      srcSet:
        "/img/home-tabs-–-book-p-500.webp 500w, /img/home-tabs-–-book.webp 528w",
      alt: "Kid in parent's lap",
    },
  },
  {
    key: "get-care-and-pay",
    // Non-breaking space before "pay", as in the source.
    label: "Get care & pay",
    body: "We've got it from here. Your sitter will show up so you can head out. After your booking wraps up you'll receive a payment request through our app.",
    img: {
      src: "/img/home-tabs-–-heda-out.webp",
      srcSet:
        "/img/home-tabs-–-heda-out-p-500.webp 500w, /img/home-tabs-–-heda-out.webp 528w",
      alt: "Mom holding and kissing kid",
    },
  },
];

export default function Parents() {
  return (
    <>
      <PageHero
        rowClassName="row row-justify-between row-align-center"
        copyColClassName="col col-lg-6 col-md-6 col-sm-10 col-xs-12"
        topShape={{
          className: "shape stone-hero_middle-left u-bg-coral",
          img: { src: "/img/Parents.webp", alt: "Sitter playing with baby" },
        }}
        bottomShape={{
          className: "shape stone-hero_top-left u-bg-olive rotate-90",
        }}
      >
        <h1>Quality kidcare, when you need it</h1>
        <p className="paragraph-1-25 u-mb-0">
          Otter’s care options are designed to cater to both planned and
          unplanned schedule changes, with sitters available with as little as 2
          hours notice.
        </p>
        <a
          href="https://app.withotter.com/sign-up/welcome"
          target="_blank"
          rel="noreferrer"
          className="btn w-button"
        >
          Book kidcare
        </a>
      </PageHero>

      <main id="main">
        <section className="section">
          <div className="container cc-narrow">
            <Tabs
              eyebrow="how it works"
              heading="We help families find reliable, flexible kidcare"
              lede="We'll match you with sitters based on your family's needs and their availability."
              items={TAB_ITEMS}
            />
          </div>
        </section>

        <section className="section u-p-0 u-mb-3">
          <CtaCard
            heading="Experienced kidcare is right around the corner."
            ctaLabel="Book kidcare"
            imageContainClassName="cta-image-contain"
            imageAspectClassName="cta-image-aspect"
            blobClassName="shape footer-shape-right u-bg-peach"
            image={{
              src: "/img/mom-on-phone.webp",
              srcSet:
                "/img/mom-on-phone-p-500.webp 500w, /img/mom-on-phone.webp 907w",
              sizes:
                "(max-width: 479px) 72vw, (max-width: 767px) 43vw, (max-width: 991px) 42vw, 30vw",
              alt: "",
            }}
          />
        </section>

        <TestimonialsSlider
          heading="What our parents are saying"
          lede="We can confidently say, we'd leave our own kids with Otter in a heartbeat."
        />

        <CommonQuestions />
      </main>
    </>
  );
}
