// Mantine AppShell + the two-container pattern shared by all three auth screens
// (SPEC_auth §5.0, §5.1). There is no card/panel: content sits flat on #F8F6F5.
//
// `withHeader` only affects the top offset (/sign-up is the single screen with a
// <header>); /log-in and /welcome render no <header> element at all.
export default function AuthShell({ children, header = null, withHeader = false }) {
  return (
    <div className={`auth-screen${withHeader ? ' auth-screen--with-header' : ''}`}>
      {header}
      <main className="auth-main">
        <div className="auth-content">
          <div className="auth-column">{children}</div>
        </div>
      </main>
    </div>
  )
}
