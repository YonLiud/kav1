import sys


def get_version():
    if getattr(sys, "frozen", False):  # Check if running as PyInstaller bundle
        import PyInstaller.utils.win32.versioninfo

        try:
            version_info = PyInstaller.utils.win32.versioninfo.GetFileVersionInfo(
                sys.executable
            )
            return version_info["StringFileInfo"]["ProductVersion"]
        except Exception:
            pass

    # Fallback for non-PyInstaller runs (dev mode)
    try:
        import subprocess

        return (
            subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
            .decode()
            .strip()
        )
    except Exception:
        return "unknown-version"


print(f"App version: {get_version()}")
