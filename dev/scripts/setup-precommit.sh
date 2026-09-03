#!/usr/bin/env bash
# S-201 AtoN Studio — POSIX installer for pre-commit hook.
# Mirrors dev/scripts/setup-precommit.bat for Linux/macOS/git-bash users.
# Usage:
#   bash dev/scripts/setup-precommit.sh

set -e

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [ -z "$REPO_ROOT" ]; then
    echo "ERROR: not inside a git repository. Run 'git init' first."
    exit 1
fi

HOOK_DIR="$REPO_ROOT/.git/hooks"
HOOK_FILE="$HOOK_DIR/pre-commit"

mkdir -p "$HOOK_DIR"

cat > "$HOOK_FILE" <<'EOF'
#!/usr/bin/env bash
# S-201 AtoN Studio pre-commit hook (installed by dev/scripts/setup-precommit.sh)
REPO_ROOT="$(git rev-parse --show-toplevel)"
PY="$(command -v python3 || command -v python || true)"
if [ -z "$PY" ]; then
    echo "ERROR: pre-commit hook needs python on PATH."
    exit 1
fi
"$PY" "$REPO_ROOT/dev/scripts/precommit-check.py"
EOF

chmod +x "$HOOK_FILE"

echo "Installed pre-commit hook at: $HOOK_FILE"
echo "It will run: python3 dev/scripts/precommit-check.py on every git commit."
echo "To uninstall: rm '$HOOK_FILE'"
echo "To bypass once: git commit --no-verify"
