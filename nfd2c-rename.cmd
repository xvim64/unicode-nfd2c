@echo off
setlocal EnableDelayedExpansion

set "python=%~dp0\python\python.exe"
set "py=%~dp0\nfd2c.py"

for /f "delims=" %%a in (dirs.txt) do (
    set "nfd=%%~a"
    if "!nfd:~1,1!"==":" (
        "!python!" "!py!" -r -x "!nfd!"
    )
)
echo.
pause
exit /b
