@echo off
setlocal

REM START
pushd %~dp0

call ..\..\project\build.cmd || goto :error

echo Test "Cmd" is success
popd
exit /b 0

:error
echo Test "Cmd" has failed
popd

exit /b %errorlevel%

