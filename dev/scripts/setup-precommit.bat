@echo off
REM S-201 AtoN Studio - Windows installer for the pre-commit hook. The hook's text is written in one place,
REM dev\scripts\setup-precommit.sh; this runs that installer with the bash Git for Windows ships, so both installers
REM write the same hook (the right shebang, LF line ends, the Python that has the gate's packages).
REM Usage:
REM   dev\scripts\setup-precommit.bat
setlocal
REM git's own folder (Git\mingw64\libexec\git-core): the Git for Windows folder is three levels above it
set "GIT_CORE="
for /f "delims=" %%i in ('git --exec-path 2^>nul') do set "GIT_CORE=%%i"
if not defined GIT_CORE (
    echo ERROR: git is not on PATH.
    exit /b 1
)
REM its bash, which runs the POSIX installer that sits beside this file
for %%i in ("%GIT_CORE%\..\..\..") do set "BASH_EXE=%%~fi\bin\bash.exe"
if not exist "%BASH_EXE%" (
    echo ERROR: no bash at %BASH_EXE%. From Git Bash, run: bash dev/scripts/setup-precommit.sh
    exit /b 1
)
REM the installer's exit code is this script's
"%BASH_EXE%" "%~dp0setup-precommit.sh"
exit /b %ERRORLEVEL%
