setlocal
echo off

pushd %~dp0

call testCmd.cmd || goto :error
call testNinja.cmd || goto :error
call testGN.cmd || goto :error

echo All test are successful
popd
exit /b 0

:error
echo One test has failed
popd

exit /b %errorlevel%

