# -*- mode: python -*-
a = Analysis(['C:\\Users\\wen\\Documents\\GitHub\\SX-UrlImgPackage\\run.py'],
             pathex=['C:\\Users\\wen\\Documents\\GitHub\\SX-UrlImgPackage\\UrlImgPackage'],
             hiddenimports=["flask",
					 "flask_restful",
					 "flask_sqlalchemy",
					 "flask.views",
					 "flask.signals",
					 "flask_restful.utils",
					 "flask.helpers",
					 "flask_restful.representations",
					 "flask_restful.representations.json",
							],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='UrlImgPackage.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True , version='C:\\Users\\wen\\Documents\\GitHub\\SX-UrlImgPackage\\docs\\file_version_info.txt', icon='C:\\Users\\wen\\Documents\\GitHub\\SX-UrlImgPackage\\icons\\logo.ico')
