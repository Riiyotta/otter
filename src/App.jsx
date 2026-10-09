import { lazy, Suspense } from 'react'
import { Routes, Route } from 'react-router-dom'
import Layout from './layouts/Layout.jsx'
import Home from './pages/Home.jsx'
import Parents from './pages/Parents.jsx'
import Sitters from './pages/Sitters.jsx'
import TrustSafety from './pages/TrustSafety.jsx'
import Faq from './pages/Faq.jsx'
import Contact from './pages/Contact.jsx'
import Careers from './pages/Careers.jsx'
import Blog from './pages/Blog.jsx'
import BlogPost from './pages/BlogPost.jsx'
const TermsOfUse = lazy(() => import('./pages/TermsOfUse.jsx'))
const PrivacyPolicy = lazy(() => import('./pages/PrivacyPolicy.jsx'))
import LogIn from './pages/LogIn.jsx'
import NotFound from './pages/NotFound.jsx'

export default function App() {
  return (
    <Routes>
      {/* `chrome` selects the nav/footer variant: the homepage ships empty nav
          link and footer link containers, every other route populates them. */}
      <Route element={<Layout chrome="home" />}>
        <Route path="/" element={<Home />} />
      </Route>
      <Route element={<Layout chrome="site" />}>
        <Route path="/parents" element={<Parents />} />
        <Route path="/sitters" element={<Sitters />} />
        <Route path="/trust-safety" element={<TrustSafety />} />
        <Route path="/faq" element={<Faq />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/careers" element={<Careers />} />
        <Route path="/blog" element={<Blog />} />
        <Route path="/blog-posts/:slug" element={<BlogPost />} />
        <Route
          path="/terms-of-use"
          element={
            <Suspense fallback={null}>
              <TermsOfUse />
            </Suspense>
          }
        />
        <Route
          path="/privacy-policy"
          element={
            <Suspense fallback={null}>
              <PrivacyPolicy />
            </Suspense>
          }
        />
        <Route path="*" element={<NotFound />} />
      </Route>
      {/* Only the log-in screen is rebuilt locally. Sign-up and welcome stay
          external links to the real app host. Separate design system
          (Mantine-derived); rebuilt inert, no credential collection. */}
      <Route path="/log-in" element={<LogIn />} />
    </Routes>
  )
}
