# Repository Guidelines

## Project Structure & Module Organization
This repository is a Python Telegram userbot. Core runtime code lives in [`heroku/`](heroku), with entry points in [`heroku/__main__.py`](heroku/__main__.py) and [`heroku/main.py`](heroku/main.py). Supporting assets are split between [`assets/`](assets) for text/font resources and [`web-resources/`](web-resources) for Jinja templates, static JS, CSS, and fonts. Keep Docker and deployment files at the repo root (`Dockerfile`, `docker-compose.yml`, `Procfile`).

The nested [`oh-my-codex/`](oh-my-codex) tree is a separate toolchain with its own Node, Rust, and test setup. Only touch it when the task explicitly targets that subtree.

## Build, Test, and Development Commands
- `python3 -m venv .venv && source .venv/bin/activate`: create an isolated Python environment.
- `pip install -r requirements.txt`: install the runtime dependencies for the userbot.
- `python3 -m heroku`: start the application locally, matching the README install flow.
- `bash install.sh`: interactive installer for VPS, venv, or Docker-based setup.
- `bash docker.sh`: build and run the Docker-based deployment path.

There is no repo-level automated Python test runner configured in the root, so verify changes by running the app and checking the relevant command flow manually.

## Coding Style & Naming Conventions
Follow Black-style Python formatting and the existing `flake8` rules in [`.flake8`](.flake8): 4-space indentation, `snake_case` for functions/modules, and `PascalCase` for classes. The root lint config ignores long lines (`E501`) and a few spacing warnings, so do not fight the local style if nearby code already follows it.

## Testing Guidelines
Root-level automated tests are not defined here. When changing behavior, prefer focused manual verification:
- startup and module loading via `python3 -m heroku`
- installer paths via `install.sh` or `docker.sh`
- feature-specific checks in the affected module under `heroku/modules/`

If you add tests, keep names descriptive and colocate them near the code they exercise.

## Commit & Pull Request Guidelines
Commit history uses short, imperative messages such as `Fix ping on arch based system` or `Update main.py`. Keep commits similarly direct and scoped to one change.

Pull requests should include a clear summary, the user-visible impact, and any setup or migration notes. Link related issues when available, and add screenshots or log excerpts for UI/installer changes.

## Security & Configuration Tips
Treat module installation and shell-executed commands as sensitive. Avoid committing secrets, API credentials, or machine-specific configuration. Review changes to blacklist, security, or deployment code carefully, since they can affect account safety and server behavior.
