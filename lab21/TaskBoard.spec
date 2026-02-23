# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all


flet_datas, flet_binaries, flet_hiddenimports = collect_all('flet')
desktop_datas, desktop_binaries, desktop_hiddenimports = collect_all('flet_desktop')

a = Analysis(
    ['c:/OPIaPZ/lab21/main.py'],
    pathex=[],
    binaries=flet_binaries + desktop_binaries,
    datas=flet_datas + desktop_datas,
    hiddenimports=flet_hiddenimports + desktop_hiddenimports,
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
    name='TaskBoard',
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
