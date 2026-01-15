# Copilot instructions for fitness-nutrition-tracker

Purpose: give AI coding agents just-enough context to be productive in this Flask REST API project.

- Architecture (big picture):
  - Flask app factory at `app/__init__.py` creates the app and initializes extensions (`app/extention.py`) and CLI commands via `manage.init_app`.
  - Blueprints are registered in `app/blueprint.py` (each `app/routers/*_router.py` defines a `blp` blueprint).
  - Request flow: `router` -> `service` -> `models` (+ `schemas` for input/output). Look at `app/routers/user_router.py` -> `app/services/user_service.py` -> `app/models/user_model.py` for an example.
  - DB: `app/db.py` exports `db = SQLAlchemy()` and migrations live in `migrations/` (use Flask-Migrate commands).

- Project-specific conventions and patterns:
  - ID fields are UUID strings (see `app/models/*_model.py`). Treat ids as strings everywhere.
  - Relationship cascade: many relationships use `cascade="all, delete-orphan"` — deleting parents cascades children.
  - Auth: JWT via `flask_jwt_extended`; helpers under `app/utils/auth.py`. Services call `create_access_token`, `get_jwt_identity`, etc.
  - Passwords use `passlib.hash.pbkdf2_sha256` for hashing and verification (see `app/services/user_service.py`).
  - Input/response schemas live in `app/schemas/*_schema.py` and are wired to endpoints via `flask_smorest` decorators (see `@blp.arguments` and `@blp.response`).
  - Error handling uses `flask_smorest.abort()` and logging via module-level loggers.
  - Tests use Python `unittest`. Tests usually set `APP_TEST_SETTINGS_MODULE` to a test config before creating app (see `tests/unit/tests_users_unit.py`).

- Helpful commands and developer workflows (what actually works here):
  - Run dev server: set `APP_SETTINGS_MODULE` then `flask run` (the project uses the Flask CLI; `app.create_app` is invoked at import). Example: `set APP_SETTINGS_MODULE=your.settings.Module` then `flask run` on Windows PowerShell.
  - Run unit tests: either `python -m unittest discover tests` or set `APP_TEST_SETTINGS_MODULE` and run the registered CLI command `flask tests` (these commands are added in `manage.init_app`).
  - Coverage HTML: `flask cov-html` (registered in `manage.py` as `cov_html`).
  - DB migrations: `flask db migrate -m "msg"` and `flask db upgrade` (Flask-Migrate is initialized in `app/__init__.py`).
  - Run a raw SQL migration file from `migrations/`: `flask run-migration migration_filename.sql` (see `manage.run_migration`).
  - Docker: there's a `docker-compose.yml` and `Dockerfile` for containerized local runs; `docker-compose up --build` is the typical flow.

- Integration points & external dependencies:
  - PostgreSQL (database) — configured via settings module and used by SQLAlchemy.
  - NGINX + Gunicorn for production (see `nginx/default.conf` and `gunicorn/gunicorn_config.py`).
  - OpenAI/AI message integration lives under `app/routers/ai_message_router.py` and `app/services/ai_message_service.py` (inspect before changing external calls).

- Small code examples to follow when implementing features:
  - New endpoint: create `app/routers/<resource>_router.py` with a `blp = Blueprint(...)`, call `service` functions in `app/services/<resource>_service.py`, and map I/O with `app/schemas/<resource>_schema.py`.
  - DB changes: add model in `app/models/`, add migration (`flask db migrate`), then `flask db upgrade`.

- What to avoid / gotchas discovered in the codebase:
  - Do not change ID types to integers — code and tests expect string UUIDs.
  - Many service functions expect to run inside Flask app context (they use `db.session` and `get_jwt_identity()`); run tests and scripts with an app context.
  - `manage.py` registers CLI commands only when `create_app`/`manage.init_app` runs — prefer using the Flask CLI for those management commands.

If anything here is unclear or you want more examples (e.g., a template for adding a new router+service+schema), tell me which area to expand. 
