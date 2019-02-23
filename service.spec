# -*- mode: python -*-

block_cipher = None


a = Analysis(['service.py'],
             pathex=['c:\\ezpywinsvc'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=['c:\\ezpywinsvc'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='myservice',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='win.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='myservice')
