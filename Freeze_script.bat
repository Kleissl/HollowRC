:: call activate build_env2
pyinstaller main.py --upx-dir=%~dp0..\upx-3.95-win64 --name=HollowRC --icon=icon.ico --onedir --paths "C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x86"
:: call deactivate
xcopy .\dist\no_upx_files\VCRUNTIME140.dll .\dist\HollowRC\
xcopy .\dist\no_upx_files\MSVCP140.dll .\dist\HollowRC\
xcopy .\dist\no_upx_files\qwindows.dll .\dist\HollowRC\PySide2\plugins\platforms\
xcopy .\dist\no_upx_files\qwindowsvistastyle.dll .\dist\HollowRC\PySide2\plugins\styles\
pause
del .\dist\HollowRC\Qt5WebSockets.dll
del .\dist\HollowRC\_decimal.pyd
del .\dist\HollowRC\_lzma.pyd
del .\dist\HollowRC\_win32sysloader.pyd
del .\dist\HollowRC\HollowRC.exe.manifest
del .\dist\HollowRC\lib_arpack*
del .\dist\HollowRC\lib_blas_su*
del .\dist\HollowRC\lib_test_fo*
del .\dist\HollowRC\libansari*
del .\dist\HollowRC\libbanded5x*
del .\dist\HollowRC\libbispeu*
del .\dist\HollowRC\libblkdta*
del .\dist\HollowRC\libchkder*
del .\dist\HollowRC\libcobyla2*
del .\dist\HollowRC\libd_odr*
del .\dist\HollowRC\libdcosqb*
del .\dist\HollowRC\libdcsrch*
del .\dist\HollowRC\libdet*
del .\dist\HollowRC\libdfft_sub*
del .\dist\HollowRC\libdfitpack*
del .\dist\HollowRC\libdgamln*
del .\dist\HollowRC\libdop853*
del .\dist\HollowRC\libdqag*
del .\dist\HollowRC\libgetbreak*
del .\dist\HollowRC\libGLESv2.dll
del .\dist\HollowRC\liblbfgsb*
del .\dist\HollowRC\libmvndst*
del .\dist\HollowRC\libnnls*
del .\dist\HollowRC\libslsqp_op*
del .\dist\HollowRC\libspecfun*
del .\dist\HollowRC\libvode*
del .\dist\HollowRC\libwrap_dum*
del .\dist\HollowRC\mfc140u.dll
del .\dist\HollowRC\Qt5DBus.dll
del .\dist\HollowRC\Qt5Quick.dll
del .\dist\HollowRC\Qt5VirtualKeyboard.dll
del .\dist\HollowRC\win32pdh.pyd
del .\dist\HollowRC\win32trace.pyd
del .\dist\HollowRC\win32ui.pyd
del .\dist\HollowRC\win32wnet.pyd
rmdir /s /q .\dist\HollowRC\win32com
rmdir /s /q .\dist\HollowRC\scipy
rmdir /s /q .\dist\HollowRC\lib2to3
rmdir /s /q .\dist\HollowRC\Include
rmdir /s /q .\dist\HollowRC\PySide2\translations
rmdir /s /q .\dist\HollowRC\PySide2\PySide2
del .\dist\HollowRC\PySide2\libEGL.dll
del .\dist\HollowRC\PySide2\d3dcompiler_47.dll
del .\dist\HollowRC\PySide2\libGLESv2.dll
del .\dist\HollowRC\PySide2\opengl32sw.dll
del .\dist\HollowRC\PySide2\QtNetwork.pyd
pause
