import subprocess
import os


def get_git_version():
    try:
        # First try to get version from file (for PyInstaller bundled version)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        version_file = os.path.join(dir_path, 'version.txt')
        if os.path.exists(version_file):
            with open(version_file, 'r') as f:
                return f.read().strip()

        # If file doesn't exist or is empty, try to get directly from git
        git_hash = subprocess.check_output(
            ['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()
        return git_hash
    except Exception:
        return "unknown-version"
