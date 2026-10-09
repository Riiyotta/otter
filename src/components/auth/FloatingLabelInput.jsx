import { useId, useState } from 'react'

// Mantine InputWrapper + TextInput as used on /log-in and /sign-up (SPEC_auth §6, §7).
//
// INERT BY DESIGN: the input is uncontrolled and nothing typed is ever read, stored,
// logged or transmitted. `onInput` only records a boolean ("is there anything in here")
// so the floating label can move; the value itself is never captured.
//
// The original drives the label position by toggling a class from React state (not by
// `:placeholder-shown`) and removes `data-empty` at the same time — reproduced here.
// `autocomplete` is forced to "off": the live values (tel-national / tel / given-name /
// family-name) are deliberately NOT reproduced so password managers ignore this clone.
export default function FloatingLabelInput({ label, type, name, className }) {
  // Mantine generates a random id per render; never hardcode one.
  const id = useId()
  const [focused, setFocused] = useState(false)
  const [hasText, setHasText] = useState(false)
  const floated = focused || hasText

  return (
    <div className={`auth-input-root${className ? ` ${className}` : ''}`}>
      <label
        htmlFor={id}
        id={`${id}-label`}
        className={`auth-input-label${floated ? '' : ' auth-input-label--as-placeholder'}`}
      >
        {label}
      </label>
      <div className="auth-input-wrapper">
        <input
          id={id}
          className="auth-input"
          type={type}
          name={name}
          autoComplete="off"
          aria-invalid="false"
          data-variant="default"
          data-label="true"
          data-empty={hasText ? undefined : 'true'}
          onFocus={() => setFocused(true)}
          onBlur={() => setFocused(false)}
          onInput={(e) => setHasText(e.currentTarget.value.length > 0)}
        />
      </div>
    </div>
  )
}
