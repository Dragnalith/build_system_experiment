setlocal
echo off

pushd %~dp0

rmdir /s /q out\build-gn

bin\windows\gn.exe --root=project -q gen out\build-gn || goto :error
bin\windows\ninja.exe -C out\build-gn || goto :error

echo Test "GN" is success
popd
exit /b 0

:error
echo Test "GN" has failed
popd

exit /b %errorlevel%

