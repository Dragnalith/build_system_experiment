setlocal
echo off

pushd %~dp0

rmdir /s /q ..\..\out\build-ninja-windows
python.exe ..\..\project\build\script\configure_ninja_windows.py || goto :error
..\..\bin\windows\ninja.exe -C ..\..\project\build\ninja\windows || goto :error

echo Test "Ninja" is success
popd
exit /b 0

:error
echo Test "Ninja" has failed
popd

exit /b %errorlevel%

