import sys
import os

def get_version():
    if getattr(sys, 'frozen', False):
        # For PyInstaller builds
        try:
            if sys.platform == 'win32':
                import PyInstaller.utils.win32.versioninfo
                version_info = PyInstaller.utils.win32.versioninfo.GetFileVersionInfo(sys.executable)
                return version_info['StringFileInfo']['ProductVersion']
            else:
                # Linux/Mac alternative
                return os.getenv('VERSION', 'unknown')
        except:
            return os.getenv('VERSION', 'unknown')
    else:
        # For development mode
        try:
            with open('version.txt') as f:
                return f.read().strip()
        except:
            return 'dev'

print(f"Version: {get_version()}")