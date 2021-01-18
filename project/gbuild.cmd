@echo off
setlocal enabledelayedexpansion

pushd %~dp0

python build\tool\gbuild %* || goto :error

popd
exit /b 0

:error
popd
exit /b !errorlevel!
