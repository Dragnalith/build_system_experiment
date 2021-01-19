@echo off
setlocal enabledelayedexpansion

python %~dp0\build\tool\gbuild %* || goto :error

exit /b 0

:error
exit /b !errorlevel!
