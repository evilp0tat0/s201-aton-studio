#!/usr/bin/env bash
# S-201 AtoN Studio — POSIX installer for the pre-commit hook, and the one place the hook's text is written:
# setup-precommit.bat runs this script with the bash Git for Windows ships.
# Usage:
#   bash dev/scripts/setup-precommit.sh

set -e

# the repository this runs in
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [ -z "$REPO_ROOT" ]; then
    echo "ERROR: not inside a git repository. Run 'git init' first."
    exit 1
fi
# its hooks folder as git names it: one folder for every worktree, core.hooksPath respected
HOOK_DIR="$(git rev-parse --path-format=absolute --git-path hooks)"
HOOK_FILE="$HOOK_DIR/pre-commit"

# the hook: the pre-commit gate, run with the first Python on PATH that has the gate's packages
mkdir -p "$HOOK_DIR"
cat > "$HOOK_FILE" <<'EOF'
#!/usr/bin/env bash
# S-201 AtoN Studio pre-commit hook (installed by dev/scripts/setup-precommit.sh)
REPO_ROOT="$(git rev-parse --show-toplevel)"
# the first Python on PATH with the gate's packages (py_mini_racer, lxml): one without them, such as a Windows Store
# python3, would report the checks that need them as skipped, and a skip blocks the commit
PY=
for c in python3 python py; do
    if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import py_mini_racer, lxml' >/dev/null 2>&1; then PY="$c"; break; fi
done
# none has them: the first Python found runs the gate, which names what is missing
if [ -z "$PY" ]; then PY="$(command -v python3 || command -v python || true)"; fi
if [ -z "$PY" ]; then
    echo "ERROR: pre-commit hook needs python on PATH."
    exit 1
fi
"$PY" "$REPO_ROOT/dev/scripts/precommit-check.py"
EOF

# executable, then how to use it
chmod +x "$HOOK_FILE"
echo "Installed pre-commit hook at: $HOOK_FILE"
echo "It runs dev/scripts/precommit-check.py on every git commit, with the first Python on PATH that has its packages."
echo "To uninstall: rm '$HOOK_FILE'"
echo "To bypass once: git commit --no-verify"
