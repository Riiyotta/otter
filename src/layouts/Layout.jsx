import { Outlet } from 'react-router-dom'
import ClipPathDefs from '../components/ClipPathDefs.jsx'
import Nav from '../components/Nav.jsx'
import Footer from '../components/Footer.jsx'

// `chrome`: "home" ships the homepage's empty nav-link / footer-link
// containers; "site" populates both, which is what every other route does.
export default function Layout({ chrome = 'site' }) {
  return (
    <>
      <ClipPathDefs />
      <div className="page-wrapper">
        <Nav chrome={chrome} />
        <Outlet />
        <Footer chrome={chrome} />
      </div>
    </>
  )
}
