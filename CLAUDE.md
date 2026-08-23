# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Spendly is a Flask expense tracker built as a step-by-step learning project. Only the
landing/marketing pages and auth *forms* are built; the actual expense-tracking backend
(database, auth logic, CRUD) is intentionally unimplemented scaffolding for later steps.

## Environment

This project uses a virtualenv at `./venv`. Every Bash tool call runs in a fresh shell, so a
`source venv/bin/activate` in one command does NOT carry over to the next command. Always
either chain activation into the same command, or call the venv's interpreter directly:

```bash
source venv/bin/activate && python app.py
# or
./venv/bin/python app.py
```

## Common commands

```bash
# install dependencies
source venv/bin/activate && pip install -r requirements.txt

# run the dev server (Flask's built-in reloader, debug on, port 5001)
source venv/bin/activate && python app.py

# run tests (pytest-flask is installed, but no test files exist yet)
source venv/bin/activate && pytest
```

There is no build step, linter, or frontend tooling — templates and CSS/JS are served directly
by Flask with no bundler.

## Architecture

- **`app.py`** — the single Flask entry point. All routes are defined directly on `app`
  (no blueprints). Real routes (`/`, `/register`, `/login`, `/terms`, `/privacy`) render Jinja2
  templates; placeholder routes (`/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`,
  `/expenses/<id>/delete`) return plain "coming in Step N" text and have no template or logic yet.
- **`database/db.py`** — currently just a comment describing the not-yet-implemented data layer:
  `get_db()` (SQLite connection with row_factory + foreign keys), `init_db()` (create tables),
  `seed_db()` (sample data). Nothing in the app queries a database yet — don't assume any table
  schema exists until this file is written.
- **`templates/`** — server-rendered Jinja2 templates. `base.html` defines the shared shell (nav,
  footer, font/CSS links, `{% block content %}` / `{% block scripts %}`); `landing.html`,
  `login.html`, `register.html`, `terms.html`, `privacy.html` all `{% extends "base.html" %}`.
  Use `{{ url_for('<endpoint>') }}` for internal links rather than hardcoded paths — the endpoint
  names match the `app.py` function names (e.g. `url_for('landing')`, `url_for('terms')`).
- **`static/css/style.css`** — single stylesheet for the whole site (no per-page CSS files, no
  `landing.css`). **`static/js/main.js`** — single vanilla-JS file, no framework, no build step;
  currently just wires up the "How it works" video modal (open/close, stops the YouTube iframe by
  clearing `iframe.src` on close so the video doesn't keep playing in the background).
- Login/register forms POST to `/login` and `/register` respectively but those routes only do a
  `GET` render today — form submission isn't wired to any backend logic yet.

## Notes for future work

- The project is meant to be filled in incrementally in the order implied by the placeholder
  routes: database setup → auth → profile → expense CRUD.
- Before referencing a file path, confirm it exists (e.g. there is no `main.py` — the entry point
  is `app.py`; there is no `static/css/landing.css` — all styles live in `static/css/style.css`).
