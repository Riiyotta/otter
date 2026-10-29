#!/usr/bin/env node
// Re-measure section heights at 1440px from a running build of the clone (BASELINE R9 evidence).
//
//   npm ci && npx vite build --outDir <dist> && npx vite preview --outDir <dist> --port 5712
//   NODE_PATH="$(npm root -g)" node extraction/measure_sections.mjs [--base http://localhost:5712] [--write]
//
// Playwright is resolved at RUNTIME (env PLAYWRIGHT_MODULE, else NODE_PATH entries, else `npm root -g`);
// no machine path is stored in this repo. Without --write the JSON is printed; with --write it replaces the
// "sectionHeights" key of extraction/measured-values.json (every other key is preserved).
//
// SELECTORS maps every (section[/variant]) of every template to the DOM element the section contract describes
// in the BUILT clone. Two sections share one DOM element on the homepage (process.numbered-cards and the join
// card are both inside section.how-it-works): they are measured as two vertical ranges of that element split at
// the join card's top edge, so their heights sum to the element's height and nothing is counted twice.
import fs from 'node:fs'
import path from 'node:path'
import { execSync } from 'node:child_process'
import { fileURLToPath, pathToFileURL } from 'node:url'

const HERE = path.dirname(fileURLToPath(import.meta.url))
const REPO = path.dirname(HERE)
const args = process.argv.slice(2)
const BASE = (args.includes('--base') ? args[args.indexOf('--base') + 1] : process.env.MEASURE_BASE_URL) || 'http://localhost:5712'
const WRITE = args.includes('--write')
const VIEWPORT = { width: 1440, height: 900 }
const BLOG_SLUG = 'series-a' // the first post in src/data/posts.js
const NOT_FOUND_PROBE = '/__not-a-route__' // any unknown path renders the catch-all '*' route

const SELECTORS = {
  'chrome.navbar': 'nav.nav_wrapper',
  'chrome.footer': 'footer.section.cc-footer',
  'hero.dark-rounded': '.page-wrapper > header.section.u-pt-0',
  'banner.beta-card': '.page-wrapper > header.section.hp-banner',
  'process.numbered-cards': { range: 'section.how-it-works', until: 'section.how-it-works .col.col-lg-12' },
  'conversion.join-card': { range: 'section.how-it-works', from: 'section.how-it-works .col.col-lg-12' },
  'trust.press-bar': 'main#main > section:has(.trust-bar)',
  'hero.light-split': '.page-wrapper > header.section',
  'disclosure.tabs-accordion': 'main#main > section:has(.cc-tabas-header)',
  'conversion.cta-card': 'main#main > section:has(.cc-cta)',
  'testimonials.slider-empty': 'main#main > section:has(.testimonials-contain)',
  'faq.common-questions-empty': 'main#main > section:last-of-type',
  'trust.video-and-cards': 'main#main > section',
  'faq.category-empty': 'main#main > section',
  'form.contact': 'main#main > section',
  'content.image-copy-split': 'main#main > section:nth-of-type(1)',
  'stats.grid/six-with-spacers': 'main#main > section:nth-of-type(2)',
  'values.principle-cards': 'main#main > section:nth-of-type(3)',
  'benefits.card-grid': 'main#main > section:nth-of-type(4)',
  'stats.grid/three-centered': 'main#main > section:nth-of-type(5)',
  'jobs.listing-rows': 'main#main > section#jobs',
  'blog.post-grid': 'main#main > section',
  'conversion.cta-band': 'main#main > div.section',
  'blog.post-header': '.page-wrapper > div.section.u-pb-0',
  'content.rich-text-body': 'main#main > div.section:nth-of-type(1)',
  'blog.related-posts': 'main#main > div.section:nth-of-type(2)',
  'legal.document-header': '.page-wrapper > div.section.u-pb-0',
  'legal.document-intro': 'main#main .col > div:first-child',
  'legal.document-part': 'main#main .col > div:not(:first-child)',
  'auth.login-form': 'div.auth-screen',
  'content.stub-notice': 'main#main.section',
}

async function loadPlaywright() {
  const cands = []
  if (process.env.PLAYWRIGHT_MODULE) cands.push(process.env.PLAYWRIGHT_MODULE)
  for (const p of (process.env.NODE_PATH || '').split(path.delimiter).filter(Boolean)) cands.push(path.join(p, 'playwright', 'index.mjs'))
  try { cands.push(path.join(execSync('npm root -g').toString().trim(), 'playwright', 'index.mjs')) } catch {}
  for (const c of cands) if (fs.existsSync(c)) { const m = await import(pathToFileURL(c).href); return m.default ?? m }
  return await import('playwright')
}

const jl = (rel) => JSON.parse(fs.readFileSync(path.join(REPO, rel), 'utf8'))
const tpl = jl('templates/templates.json')
const pw = await loadPlaywright()
const browser = await pw.chromium.launch()
const page = await browser.newPage({ viewport: VIEWPORT, reducedMotion: 'no-preference' })
const out = {
  _note: 'Measured from a LOCAL vite preview of the BUILT clone (not the live site) at 1440x900 by extraction/measure_sections.mjs. heightPx = getBoundingClientRect().height of the element SELECTORS names for the section (or a vertical range of it, see the script header), after a full scroll pass; position fixed/sticky elements are inFlow:false and take no page height. Repeatable nodes are recorded once per DOM instance (instance index). Consumed by extraction/wrapper_gate.py.',
  viewport: VIEWPORT,
  measuredAt: new Date().toISOString().slice(0, 10),
  tool: 'playwright chromium (headless), extraction/measure_sections.mjs',
  baseUrl: 'local vite preview of the built clone',
  blogSlugMeasured: BLOG_SLUG,
  notFoundProbe: NOT_FOUND_PROBE,
  routes: {},
}

for (const [route, tid] of Object.entries(tpl.routeToTemplate)) {
  const url = BASE + (route === '*' ? NOT_FOUND_PROBE : route.replace(':slug', BLOG_SLUG))
  await page.goto(url, { waitUntil: 'networkidle' })
  await page.evaluate(() => document.fonts.ready)
  await page.evaluate(async () => {
    for (let y = 0; y < document.documentElement.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise((r) => setTimeout(r, 50)) }
    window.scrollTo(0, 0); await new Promise((r) => setTimeout(r, 300))
  })
  const nodes = tpl.templates[tid].nodes.map((n) => ({
    section: n.section, variant: n.variant || null, repeatable: !!n.repeatable,
    selector: SELECTORS[n.section + '/' + n.variant] || SELECTORS[n.section],
  }))
  const res = await page.evaluate((nodes) => {
    const flow = (el) => { const pos = getComputedStyle(el).position; return { position: pos, inFlow: !(pos === 'fixed' || pos === 'sticky') } }
    const top = (el) => el.getBoundingClientRect().top + window.scrollY
    const rows = []
    for (const n of nodes) {
      const base = { section: n.section, variant: n.variant, selector: typeof n.selector === 'string' ? n.selector : JSON.stringify(n.selector) }
      if (n.selector && typeof n.selector === 'object') {
        const el = document.querySelector(n.selector.range)
        const cut = document.querySelector(n.selector.until || n.selector.from)
        if (!el || !cut) { rows.push({ ...base, heightPx: null, missing: true }); continue }
        const a = top(el), b = top(cut), z = a + el.getBoundingClientRect().height
        rows.push({ ...base, heightPx: Math.round(n.selector.until ? b - a : z - b), ...flow(el), measuredAs: 'vertical range of ' + n.selector.range })
        continue
      }
      const els = n.selector ? [...document.querySelectorAll(n.selector)] : []
      if (!els.length) { rows.push({ ...base, heightPx: null, missing: true }); continue }
      const list = n.repeatable ? els : [els[0]]
      list.forEach((el, i) => rows.push({ ...base, ...(n.repeatable ? { instance: i } : {}), heightPx: Math.round(el.getBoundingClientRect().height), ...flow(el) }))
    }
    return { pageHeight: document.documentElement.scrollHeight, sections: rows }
  }, nodes)
  out.routes[route] = { template: tid, url: route === '*' ? NOT_FOUND_PROBE : route.replace(':slug', BLOG_SLUG), ...res }
}
await browser.close()

if (WRITE) {
  const file = path.join(HERE, 'measured-values.json')
  const mv = JSON.parse(fs.readFileSync(file, 'utf8'))
  mv.sectionHeights = out
  fs.writeFileSync(file, JSON.stringify(mv, null, 2) + '\n')
  console.log('wrote sectionHeights for', Object.keys(out.routes).length, 'routes')
} else {
  console.log(JSON.stringify(out, null, 2))
}
