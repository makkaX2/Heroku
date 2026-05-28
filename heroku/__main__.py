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

import getpass
import hashlib
import os
import subprocess
import sys

from ._internal import restart

if "--no-git" in sys.argv:
    os.environ["HEROKU_NO_GIT"] = "1"


def get_file_hash(filename):
    hasher = hashlib.sha256()
    try:
        with open(filename, "rb") as f:
            hasher.update(f.read())
        return hasher.hexdigest()
    except FileNotFoundError:
        return None


def deps():
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--upgrade",
            "-q",
            "--disable-pip-version-check",
            "--no-warn-script-location",
            "-r",
            "requirements.txt",
        ],
        check=True,
        timeout=600,
        capture_output=True,
    )
    with open(".requirements_hash", "w") as f:
        f.write(get_file_hash("requirements.txt"))


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
        pass
    else:
        try:
            import herokutl  # noqa: F811

            if tuple(map(int, herokutl.__version__.split("."))) < (1, 7, 2):
                raise ImportError
        except ImportError:
            print("\U0001f504 Installing dependencies...")
            deps()
            restart()

    try:
        from . import log

        log.init()
        from . import main
    except ImportError as e:
        print(
            f"{str(e)}\n\U0001f504 Attempting dependencies installation... Just wait ⏱"
        )
        deps()
        restart()

    if "HEROKU_DO_NOT_RESTART" in os.environ:
        del os.environ["HEROKU_DO_NOT_RESTART"]
    if "HEROKU_DO_NOT_RESTART2" in os.environ:
        del os.environ["HEROKU_DO_NOT_RESTART2"]

    prev_hash = None
    if os.path.exists(".requirements_hash"):
        with open(".requirements_hash", "r") as f:
            prev_hash = f.read().strip()

    if prev_hash != get_file_hash("requirements.txt"):
        print(
            "\U0001f504 Detected changes in requirements.txt, updating dependencies..."
        )
        deps()
        restart()

    main.heroku.main()
