# Spec: Login and Logout

## Overview
This step wires the existing `/login` page up to real authentication and adds a working
`/logout`. Right now `login()` only renders `login.html` on `GET`, and `/logout` is a placeholder
that returns plain text. This step adds session-backed login: a `POST /login` handler that
verifies the submitted email/password against the `users` table and starts a session, plus a
`/logout` route that clears the session. The shared nav in `base.html` also needs to become
session-aware so a logged-in visitor sees "Sign out" instead of "Sign in" / "Get started".
Expense CRUD and profile pages remain out of scope and stay as placeholders.

## Depends on
- Step 1 — Database setup (`database/db.py`'s `users` table and `get_db()`).
- Step 2 — Registration (`POST /register` must exist so accounts can be created to log into).

## Routes
- `POST /login` — validate submitted email/password against `users`, start a session on
  success — public
- `GET /logout` — clear the session and redirect to the landing page — logged-in (safe to hit
  while logged out too; it should just no-op and redirect)

`GET /login` already exists and is unchanged.

## Database changes
No database changes needed. The existing `users` table (id, name, email UNIQUE, password_hash,
created_at) already covers everything this step requires — verified against `database/db.py`.

## Templates
- **Create:** none
- **Modify:**
  - `templates/login.html` — already has an `{% if error %}` block wired to an `error` variable
    and reuses the existing `.auth-error` CSS rule — the new route just needs to pass `error` in
    on failure. No structural changes needed.
  - `templates/base.html` — nav currently hardcodes "Sign in" / "Get started" links. Make the
    `nav-links` block session-aware: if a user is logged in, show a "Sign out" link
    (`{{ url_for('logout') }}`) instead; otherwise show the existing "Sign in" / "Get started"
    links unchanged.

## Files to change
- `app.py`:
  - Set `app.secret_key` (from an environment variable, e.g. `os.environ.get("SECRET_KEY",
    "dev")`, since there is no secrets/config setup yet) so Flask sessions work.
  - Change `login()` to handle `GET` and `POST`. On `POST`, look up the user by email, verify the
    password with `werkzeug.security.check_password_hash`, store `user_id` in `session` on
    success, and redirect somewhere sensible (e.g. `/` — there is no dashboard/profile page built
    yet).
  - Replace the placeholder `/logout` route: clear the session (`session.clear()`) and redirect
    to `url_for('landing')`.
- `templates/base.html` — session-aware nav as described above.

## Files to create
- None

## New dependencies
No new dependencies. Uses `werkzeug.security.check_password_hash` (mirrors
`generate_password_hash`, already used in `database/db.py` and `app.py`) and Flask's built-in
`session`.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug — verify with `check_password_hash`, never compare plaintext
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Validate server-side even though the form has client-side `required`/`type` attributes:
  - email and password must both be non-empty
  - look up the user by email; if not found, or `check_password_hash` fails, treat both cases
    identically with one generic error ("Invalid email or password") — never reveal whether the
    email exists
- On any validation/auth failure, re-render `login.html` with `error` set and re-populate the
  `email` field only (never re-populate the password field)
- On success, store the authenticated user's id in `session["user_id"]` and redirect to `/`
- `/logout` must work even if no one is logged in (just redirect, no error)
- Do not build a `login_required` decorator or protect any other routes in this step — that is
  future work once profile/expense pages exist

## Definition of done
- [ ] Submitting the login form with a valid registered email/password redirects to `/` and
      starts a session
- [ ] Submitting with a correct email but wrong password re-renders `login.html` with a generic
      "Invalid email or password" error and does not start a session
- [ ] Submitting with an email that isn't registered re-renders `login.html` with the same
      generic error (no difference in message from a wrong password)
- [ ] Submitting with a missing email or password re-renders `login.html` with an error
- [ ] Visiting `/logout` while logged in clears the session and redirects to `/`
- [ ] Visiting `/logout` while logged out does not error and redirects to `/`
- [ ] After logging in, the nav in `base.html` shows a "Sign out" link instead of "Sign in" /
      "Get started"
- [ ] `GET /login` still renders the form exactly as before
- [ ] The app starts and runs without errors (`source venv/bin/activate && python app.py`)
