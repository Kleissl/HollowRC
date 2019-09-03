:: call activate build_env2
pyinstaller main.py --upx-dir=%~dp0..\upx-3.95-win32 --name=HollowRC --icon=icon.ico --onedir --paths "C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x86"
:: call deactivate
xcopy .\dist\no_upx_files\VCRUNTIME140.dll .\dist\HollowRC\
xcopy .\dist\no_upx_files\MSVCP140.dll .\dist\HollowRC\
xcopy .\dist\HollowRC\qt5_plugins\platforms\qwindows.dll .\dist\HollowRC\platforms\
pause
