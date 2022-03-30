@echo off
setlocal EnableDelayedExpansion

set "python=%~dp0\python\python.exe"
set "py=%~dp0\nfd2c.py"

"!python!" "!py!" -h

pause
exit /b
