@RD /S /Q "C:\Users\kekl\Dropbox\Python\HollowRC\dist"
@RD /S /Q "C:\Users\kekl\Dropbox\Python\HollowRC\dist_UPXed"
pause
call activate build_env
pyinstaller main.py --upx-dir=C:\Users\kekl\Dropbox\Python\upx394w
pause
RENAME C:\Users\kekl\Dropbox\Python\HollowRC\dist dist_UPXed
pause
pyinstaller main.py
call deactivate
xcopy .\dist\main\VCRUNTIME140.dll .\dist_UPXed\main\
xcopy .\dist\main\MSVCP140.dll .\dist_UPXed\main\
xcopy .\dist\main\PyQt5\Qt\plugins\platforms\qwindows.dll .\dist_UPXed\main\platforms\
pause
