setlocal
echo off

pushd %~dp0

call test\win\test_cmd.cmd || goto :error
call test\win\test_ninja.cmd || goto :error
call test\win\test_gn.cmd || goto :error

echo All test are successful
popd
exit /b 0

:error
echo One test has failed
popd

exit /b %errorlevel%

