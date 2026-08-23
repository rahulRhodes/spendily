# Spec: Registration

## Overview
This step wires the existing `/register` page up to real account creation. Right now the
route only renders `register.html` — submitting the form does nothing. This step adds the
`POST` handler that validates the submitted name/email/password, hashes the password, and
inserts a new row into the `users` table, so a visitor can actually create a Spendly account.
Login and session handling are out of scope here and will be covered in a later step.

## Depends on
Step 1 — Database setup (`database/db.py`'s `users` table and `get_db()` must exist and work).

## Routes
- `POST /register` — validate submitted registration form and create the user — public

`GET /register` already exists and is unchanged.

## Database changes
No database changes needed. The existing `users` table (id, name, email UNIQUE, password_hash,
created_at) already covers everything this step requires — verified against `database/db.py`.

## Templates
- **Create:** none
- **Modify:** none required. `templates/register.html` already has an `{% if error %}` block
  wired to an `error` template variable and an `.auth-error` CSS rule already exists in
  `static/css/style.css` — the new route just needs to pass `error` into the existing template
  on validation failure.

## Files to change
- `app.py` — change `register()` to handle `GET` and `POST`, add validation, insert the user,
  and redirect to `/login` on success.

## Files to create
- None

## New dependencies
No new dependencies. Uses `werkzeug.security.generate_password_hash` (already used in
`database/db.py`) and the standard library.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (`generate_password_hash(..., method="pbkdf2:sha256")`, matching
  the convention already used in `database/db.py`)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Validate server-side even though the form has client-side `required`/`type` attributes:
  - name, email, and password must all be non-empty
  - password must be at least 8 characters (matches the field's placeholder text)
  - email must not already exist in `users` — check before inserting
- On any validation failure, re-render `register.html` with `error` set to a user-facing message
  and re-populate the `name`/`email` fields (never re-populate the password field)
- On success, insert the user and redirect to `/login` (do not auto-login — no session/secret key
  work happens in this step)

## Definition of done
- [ ] Submitting the register form with valid, unique details creates a new row in `users` with a
      hashed (not plaintext) password
- [ ] After a successful registration, the browser is redirected to `/login`
- [ ] Submitting with an email that's already registered re-renders `register.html` with an error
      and does not create a duplicate row
- [ ] Submitting with a password under 8 characters re-renders `register.html` with an error and
      does not create a row
- [ ] Submitting with a missing name, email, or password re-renders `register.html` with an error
      and does not create a row
- [ ] `GET /register` still renders the form exactly as before
- [ ] The app starts and runs without errors (`source venv/bin/activate && python app.py`)
