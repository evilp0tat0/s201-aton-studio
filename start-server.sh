#!/usr/bin/env bash
# =============================================================================
#  S-201 AtoN Studio — Portable Launcher (macOS / Linux)
# =============================================================================
#  Run this script to start the app:
#      chmod +x start-server.sh
#      ./start-server.sh
#
#  It starts a local HTTP server on port 8080 and opens the app in your
#  default browser. The server must be running for the Annex D symbol
#  library to load — opening the HTML file directly (file://) falls back
#  to the legacy primitive renderer.
#
#  Press Ctrl+C to stop the server.
# =============================================================================

set -e
cd "$(dirname "$0")"

PORT=8080
URL="http://localhost:${PORT}/s201_aton_studio.html"

echo
echo "============================================================"
echo " S-201 AtoN Studio"
echo "============================================================"
echo
echo " Starting local HTTP server on port ${PORT}..."
echo " Open in your browser:"
echo "     ${URL}"
echo
echo " Press Ctrl+C to stop the server."
echo "============================================================"
echo

# Open the URL in the user's default browser after a brief delay
# (so the server has time to bind the port before the browser hits it)
open_browser() {
    sleep 1
    if   command -v xdg-open >/dev/null 2>&1; then xdg-open "$URL" >/dev/null 2>&1 || true
    elif command -v open     >/dev/null 2>&1; then open     "$URL" >/dev/null 2>&1 || true
    elif command -v wslview  >/dev/null 2>&1; then wslview  "$URL" >/dev/null 2>&1 || true
    fi
}

# Probe Python interpreters by actually running them, not just locating them.
# `command -v` (like Windows' `where`) reports a name as present even when it
# is a non-functional shim — e.g. the macOS Command Line Tools stub `python3`,
# which on a machine without the tools installed pops an install dialog and
# exits non-zero instead of serving. Requiring `--version` to succeed skips
# those dead shims and falls through to the next candidate.
for cand in python3 python; do
    if command -v "$cand" >/dev/null 2>&1 && "$cand" --version >/dev/null 2>&1; then
        open_browser &
        exec "$cand" -m http.server "$PORT"
    fi
done

# Fall back to Node.js http-server
if command -v npx >/dev/null 2>&1; then
    open_browser &
    exec npx --yes http-server -p "$PORT" -c-1
fi

# No suitable runtime — show install instructions
cat <<EOF

============================================================
 ERROR: No Python or Node.js found on this system.
============================================================

 This app needs a local HTTP server to load the Annex D
 symbol library. Please install one of the following:

   1. Python 3 (recommended):
        macOS:   brew install python
        Linux:   sudo apt install python3   (Debian/Ubuntu)
                 sudo dnf install python3   (Fedora)
        https://www.python.org/downloads/

   2. Node.js:
        https://nodejs.org/

 After installing, run this script again.

EOF
exit 1
