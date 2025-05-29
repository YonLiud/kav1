# -*- mode: python ; coding: utf-8 -*-

import os

# Get version from environment variable or use default
version = os.getenv('VERSION', '0.0.0')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('app\\**\\*.py', 'app'),
        ('version.txt', '.')  # Keep if you still need this file
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    icon='clienticon.ico',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version=version,  # Add version info here
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)