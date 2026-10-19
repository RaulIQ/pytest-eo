import sys
from pathlib import Path

import pytest

HOOK = Path(__file__).parent.parent / ".claude" / "hooks" / "eo-gate.sh"


def test_keeps_the_failure_section_of_a_test(
    pytester: pytest.Pytester,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    (pytester.path / "tests").mkdir()
    (pytester.path / "tests" / "test_wobbly.py").write_text(
        "def test_wobbles():\n    assert 7 == 13\n",
    )
    python = pytester.path / ".venv" / "bin" / "python"
    python.parent.mkdir(parents=True)
    python.write_text(f'#!/bin/sh\nexec "{sys.executable}" "$@"\n')
    python.chmod(0o755)
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(pytester.path))
    result = pytester.run(
        str(HOOK), stdin=b'{"hook_event_name": "Stop"}', timeout=180
    )
    assert "_ test_wobbles _" in result.stderr.str()
