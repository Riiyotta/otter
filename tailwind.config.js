/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  // Preflight is off: it forces `img { height: auto }`, which would override the
  // Playdate.svg `height="180"` presentation hint, and it resets heading
  // font-sizes. src/index.css ships the Webflow normalize subset the spec was
  // measured against instead.
  // Tailwind's `container` plugin is off because the project defines its own
  // `.container` primitive (CLONE_SPEC §3).
  corePlugins: {
    preflight: false,
    container: false,
  },
  theme: {
    // Webflow uses max-width breakpoints; mirror them exactly.
    screens: {
      medium: { max: '991px' },
      small: { max: '767px' },
      tiny: { max: '479px' },
    },
    extend: {
      colors: {
        primary: '#00373e',
        celeste: '#cafff2',
        peach: '#fbd3b6',
        ivory: '#f8f6f5',
        olive: '#94954c',
        coral: '#fbad9c',
        sandstone: '#ac9e88',
        'btn-border': '#d6cfc4',
      },
      fontFamily: {
        sans: ['Jokker', 'sans-serif'],
        display: ['"Reckless Neue"', 'sans-serif'],
      },
      maxWidth: {
        container: '90rem',
        narrow: '75rem',
      },
      borderRadius: {
        hero: '72px',
        card: '32px',
        'footer-card': '24px',
        trust: '40px',
        pill: '99em',
      },
      boxShadow: {
        'white-btn-hover':
          '0 1px rgba(27,30,31,.08), 0 1px 5px rgba(27,30,31,.04)',
        'white-btn-active': '0 1px rgba(27,30,31,.08)',
      },
      transitionTimingFunction: {
        'out-quart': 'cubic-bezier(.165,.84,.44,1)',
      },
    },
  },
  plugins: [],
}
