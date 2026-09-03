@echo off
REM ============================================================================
REM  S-201 AtoN Studio — Portable Launcher (Windows)
REM ============================================================================
REM  Double-click this file to start the app.
REM  It starts a local HTTP server on port 8080 and opens the app in your
REM  default browser. The server must be running for the Annex D symbol
REM  library to load — opening the HTML file directly (file://) falls back
REM  to the legacy primitive renderer.
REM
REM  Press Ctrl+C in this window to stop the server.
REM
REM  Runtime detection: each candidate is *probed* (actually run with
REM  --version) instead of merely being located with `where`. Windows ships
REM  "App execution alias" stubs for python.exe / python3.exe (Settings >
REM  Apps > App execution aliases) that `where` reports as present, but which
REM  — when no real interpreter backs them — only print "Python was not
REM  found..." and exit non-zero. The old `where`-only check accepted those
REM  dead stubs and produced a false "no Python" at run time. Probing skips
REM  them, and the `py` launcher (a real binary, never an alias stub) is
REM  tried first for that reason.
REM ============================================================================

setlocal enabledelayedexpansion
cd /d "%~dp0"

echo.
echo ============================================================
echo  S-201 AtoN Studio
echo ============================================================
echo.
echo  Starting local HTTP server on port 8080...
echo  Open in your browser:
echo      http://localhost:8080/s201_aton_studio.html
echo.
echo  Press Ctrl+C in this window to stop the server.
echo ============================================================
echo.

REM Probe interpreters in order of reliability. `py -3` is the real Windows
REM launcher (never an alias stub); `python` / `python3` may resolve to the
REM Microsoft Store alias, so they are accepted only if they actually run.
set "PYCMD="
call :probe py -3
if not defined PYCMD call :probe python
if not defined PYCMD call :probe python3

if defined PYCMD (
    echo  Using interpreter: !PYCMD!
    echo.
    REM Delay the browser open by ~2 s so the server has time to bind port 8080
    start "" /b cmd /c "timeout /t 2 /nobreak >nul 2>&1 && start "" http://localhost:8080/s201_aton_studio.html"
    !PYCMD! -m http.server 8080
    goto :end
)

REM Fall back to Node.js http-server via npx
where npx >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo  Using interpreter: npx http-server
    echo.
    start "" /b cmd /c "timeout /t 2 /nobreak >nul 2>&1 && start "" http://localhost:8080/s201_aton_studio.html"
    npx --yes http-server -p 8080 -c-1
    goto :end
)

goto :nopython

REM --------------------------------------------------------------------------
REM  :probe <command...>  — run "<command> --version"; if it exits cleanly
REM  (a real interpreter, not a dead Store-alias stub or a missing command),
REM  remember the command in PYCMD. Reached only via `call`.
REM --------------------------------------------------------------------------
:probe
%* --version >nul 2>&1
if not errorlevel 1 set "PYCMD=%*"
exit /b

:nopython
echo.
echo ============================================================
echo  ERROR: No working Python or Node.js runtime found.
echo ============================================================
echo.
echo  This app needs a local HTTP server to load the Annex D
echo  symbol library.
echo.
echo  If you believe Python IS already installed but still see
echo  this, a Windows "App execution alias" may be shadowing it:
echo    Open Settings ^> Apps ^> Advanced app settings ^> App
echo    execution aliases and turn OFF "python.exe" / "python3.exe",
echo    then reinstall Python from python.org with the PATH option
echo    ticked (this also installs the "py" launcher this script
echo    prefers).
echo.
echo  Or install one of the following, then double-click again:
echo.
echo    1. Python 3 (recommended, ~30 MB):
echo       https://www.python.org/downloads/
echo       Make sure to check "Add python.exe to PATH" during install.
echo.
echo    2. Node.js:
echo       https://nodejs.org/
echo.
echo    3. VS Code with "Live Server" extension:
echo       https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer
echo       Open this folder in VS Code, right-click s201_aton_studio.html,
echo       then choose "Open with Live Server".
echo.
pause
exit /b 1

:end
endlocal
