"""Entry point. Checks for user and starts main script"""

# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# 🌐 https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

# ©️ Codrago, 2024-2030
# This file is a part of Heroku Userbot
# 🌐 https://github.com/coddrago/Heroku
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

import os
import sys

if "--no-git" in sys.argv:
    os.environ["HEROKU_NO_GIT"] = "1"
if os.environ.get("HEROKU_DEPLOYMENT", "").lower() in {"dokploy", "nixpacks"}:
    os.environ["HEROKU_NO_GIT"] = "1"


# Проверка на root полностью отключена для совместимости с контейнерами Dokploy
os.environ["NO_SUDO"] = "1"

if sys.version_info < (3, 10, 0):
    print("\U0001f6ab Error: you must use at least Python version 3.10.0")
elif __package__ != "heroku":
    print(
        "\U0001f6ab Error: you cannot run this as a script; you must execute as a package"
    )
else:
    try:
        import herokutl
    except Exception:
        print(
            "🚫 Missing runtime dependency: herokutl.\n"
            "Install requirements during the build stage and redeploy."
        )
        sys.exit(1)
    else:
        if tuple(map(int, herokutl.__version__.split("."))) < (1, 7, 2):
            print(
                "🚫 herokutl is too old for this build.\n"
                "Update requirements.txt and redeploy the app."
            )
            sys.exit(1)

    try:
        from . import log

        log.init()
        from . import main
    except ImportError as e:
        print(
            f"{str(e)}\n"
            "🚫 Import failed during startup.\n"
            "Build dependencies in Dokploy/Nixpacks and redeploy."
        )
        sys.exit(1)

    if "HEROKU_DO_NOT_RESTART" in os.environ:
        del os.environ["HEROKU_DO_NOT_RESTART"]
    if "HEROKU_DO_NOT_RESTART2" in os.environ:
        del os.environ["HEROKU_DO_NOT_RESTART2"]

    main.heroku.main()
