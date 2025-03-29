# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['D:\\python_project\\2025.3.29\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('D:\\python_project\\2025.3.29\\generated_image_march_29__2025___8_33pm_ouV_icon.ico', '.')],
    hiddenimports=['borax', 'borax.calendars'],
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
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
