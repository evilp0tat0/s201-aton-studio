@echo off
REM S-201 AtoN Studio — Windows installer for pre-commit hook.
REM Mirrors dev/scripts/setup-precommit.sh for cmd.exe / PowerShell users.
REM Usage:
REM   dev\scripts\setup-precommit.bat

setlocal enabledelayedexpansion

for /f "delims=" %%i in ('git rev-parse --show-toplevel 2^>nul') do set REPO_ROOT=%%i
if "%REPO_ROOT%"=="" (
    echo ERROR: not inside a git repository. Run 'git init' first.
    exit /b 1
)

set HOOK_DIR=%REPO_ROOT%\.git\hooks
set HOOK_FILE=%HOOK_DIR%\pre-commit

if not exist "%HOOK_DIR%" mkdir "%HOOK_DIR%"

REM Write the hook (bash-style; git for windows ships bash)
> "%HOOK_FILE%" echo #!/usr/bin/env bash
>> "%HOOK_FILE%" echo # S-201 AtoN Studio pre-commit hook (installed by dev/scripts/setup-precommit.bat)
>> "%HOOK_FILE%" echo REPO_ROOT="$(git rev-parse --show-toplevel)"
>> "%HOOK_FILE%" echo PY="$(command -v python3 ^|^| command -v python ^|^| true)"
>> "%HOOK_FILE%" echo if [ -z "$PY" ]; then
>> "%HOOK_FILE%" echo   echo "ERROR: pre-commit hook needs python on PATH."
>> "%HOOK_FILE%" echo   exit 1
>> "%HOOK_FILE%" echo fi
>> "%HOOK_FILE%" echo "$PY" "$REPO_ROOT/dev/scripts/precommit-check.py"

echo Installed pre-commit hook at: %HOOK_FILE%
echo It will run: python dev\scripts\precommit-check.py on every git commit.
echo To uninstall: del "%HOOK_FILE%"
echo To bypass once: git commit --no-verify

endlocal
