#!/usr/bin/env bash
# Claude Code hook: run `pytest --eo` and, when it is red, give the
# findings back to Claude (exit code 2) so it fixes them before going on.
# Used for PostToolUse (after editing a Python or config file) and Stop.
set -u

payload=$(cat)
root="${CLAUDE_PROJECT_DIR:-$PWD}"
cd "$root" || exit 0
python=".venv/bin/python"
if [ ! -x "$python" ]; then
  echo "pytest --eo gate skipped: no .venv here, run python3 -m venv .venv && .venv/bin/pip install -e ." >&2
  exit 1
fi

field() {
  printf '%s' "$payload" | "$python" -I -c '
import json, sys
value = json.load(sys.stdin)
for key in sys.argv[1].split("."):
    value = value.get(key, "") if isinstance(value, dict) else ""
print(value)
' "$1"
}

event=$(field hook_event_name)
if [ "$event" = "PostToolUse" ]; then
  case "$(field tool_input.file_path)" in
    *.py|*.toml|*.ini|*.cfg) ;;
    *) exit 0 ;;
  esac
fi

report=$("$python" -m pytest --eo -q --tb=short 2>&1)
if [ $? -eq 0 ]; then
  exit 0
fi

findings=$(printf '%s\n' "$report" | tail -n 120)
summary=$(printf '%s\n' "$report" | tail -n 1)

if [ "$event" = "Stop" ] && [ "$(field stop_hook_active)" = "True" ]; then
  printf '{"systemMessage": %s}\n' \
    "$(printf 'pytest --eo is still red after a retry: %s' "$summary" | "$python" -I -c 'import json, sys; print(json.dumps(sys.stdin.read()))')"
  exit 0
fi

{
  echo "pytest --eo is red; fix every finding below, never suppress it without a reason"
  printf '%s\n' "$findings"
  echo "$summary"
} >&2
exit 2
