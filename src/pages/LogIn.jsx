import AuthShell from '../components/auth/AuthShell.jsx'
import AuthWordmark from '../components/auth/AuthWordmark.jsx'
import FloatingLabelInput from '../components/auth/FloatingLabelInput.jsx'
import '../styles/auth.css'

// app.withotter.com/log-in — rebuilt from spec/SPEC_auth.md §11.1.
// No header, no links, one field. Copy on this screen is complete as written:
// "Welcome back!", "Phone Number", "Continue" — nothing else.
//
// INERT: the <form> has no action and no method; onSubmit only preventDefault()s.
// No endpoint, no fetch, no storage, no logging of anything typed.
export default function LogIn() {
  return (
    <AuthShell>
      <div className="auth-stack auth-login-stack">
        <div className="auth-stack auth-login-head">
          <div className="auth-center auth-login-logo-center">
            <AuthWordmark idSuffix="login" className="auth-login-logo" />
          </div>
          <div className="auth-center">
            {/* Hard 400px at every width; at 390 it overflows the 326px column
                to x = -5 and is clipped by overflow-x:hidden on the shell. That
                is the original's behaviour, reproduced on purpose. */}
            <img
              className="auth-img auth-illo-children"
              src="/img/illo-children-of-different-ages.svg"
              alt=""
              width="2804"
              height="1777"
            />
          </div>
        </div>
        <form onSubmit={(e) => e.preventDefault()}>
          <div className="auth-stack auth-login-form-stack">
            <h3 className="auth-h3">Welcome back!</h3>
            {/* "Phone Number" with a capital N here; /sign-up says "Phone
                number" — a cross-screen copy inconsistency in the original. */}
            <FloatingLabelInput label="Phone Number" type="tel" name="phoneNumber" />
            <button className="auth-btn" type="submit" disabled>
              <span className="auth-btn-inner">
                <span className="auth-btn-label">Continue</span>
              </span>
            </button>
          </div>
        </form>
      </div>
    </AuthShell>
  )
}
