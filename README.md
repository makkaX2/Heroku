# Heroku Userbot

Telegram userbot built to deploy from GitHub on Dokploy with Nixpacks.

## Deployment

1. Create a Dokploy app from this repository.
2. Select Nixpacks as the builder.
3. Set these environment variables:
   - `HEROKU_DEPLOYMENT=dokploy`
   - `HEROKU_DATA_ROOT=/data/heroku` or another mounted persistent path
   - `API_ID`
   - `API_HASH`
4. Mount persistent storage at the same path as `HEROKU_DATA_ROOT`.
5. Deploy. The Nixpacks start command is `python -m heroku`.

The app now starts directly from the GitHub checkout. It does not self-clone or reinstall dependencies at runtime.

## Local Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m heroku
```

If you want config, sessions, and loaded modules outside the repository, set `HEROKU_DATA_ROOT` before launch.

## Project Layout

- `heroku/` core runtime, commands, web UI, loaders, and utilities
- `assets/` text and font resources used by the bot
- `web-resources/` Jinja templates, static CSS, JS, and fonts
- `nixpacks.toml` Nixpacks build and start configuration
- `Procfile` compatibility start command

## Security

Treat third-party modules and command handlers as code execution. Install modules only from trusted sources and review anything that touches `.terminal`, `.eval`, or loader paths.

## Support

- Documentation: [heroku-ub.xyz](https://heroku-ub.xyz/)
- Developer docs: [dev.heroku-ub.xyz](https://dev.heroku-ub.xyz/)
- Telegram support: [@heroku_talks](https://t.me/heroku_talks)
