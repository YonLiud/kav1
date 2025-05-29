import os


def get_version():
    try:
        with open("version.txt", "r") as f:
            sha = f.read().strip()
    except (OSError, IOError):
        sha = "unknown"

    if os.getenv("RELEASE_BUILD") == "true":
        return sha
    return f"unreleased-{sha}"
