setlocal
echo off

pushd %~dp0

rmdir /s /q ..\..\out\build-ninja
python.exe ..\..\project\build\script\configure_ninja_win.py || goto :error
..\..\bin\win\ninja.exe -C ..\..\project\build\ninja\win || goto :error

echo Test "Ninja" is success
popd
exit /b 0

:error
echo Test "Ninja" has failed
popd

exit /b %errorlevel%

