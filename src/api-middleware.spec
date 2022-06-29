# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['./run.py'],
             pathex=[],
             binaries=[],
             datas=[
               ('./logging-api-middleware.conf', '.'),
               ('./logging.conf', '.'), 
               ('./lib', 'lib/'), 
             ],
             hiddenimports=[
                'psutil',
                'serial',
                'serial.tools',
                'serial.tools.list_ports',
                'uvicorn.lifespan.off',
                'uvicorn.lifespan.on',
                'uvicorn.lifespan',
                'uvicorn.protocols.websockets',
                'uvicorn.protocols.websockets.auto',
                'uvicorn.protocols.websockets.wsproto_impl',
                'uvicorn.protocols.websockets_impl',
                'uvicorn.protocols.http',
                'uvicorn.protocols.http.auto',
                'uvicorn.protocols.http.h11_impl',
                'uvicorn.protocols.http.httptools_impl',
                'uvicorn.protocols',
                'uvicorn.loops.auto',
                'uvicorn.loops.asyncio',
                'uvicorn.loops.uvloop',
                'uvicorn.loops',
                'uvicorn.logging'
             ],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='api-middleware',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon='./exe_icon_32.ico',
          version='version.rc')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=False,
               upx_exclude=[],
               name='api-middleware')
