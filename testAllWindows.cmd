setlocal
echo off

pushd %~dp0

call test\windows\testCmd.cmd || goto :error
call test\windows\testNinja.cmd || goto :error
call test\windows\testGN.cmd || goto :error

echo All test are successful
popd
exit /b 0

:error
echo One test has failed
popd

exit /b %errorlevel%

