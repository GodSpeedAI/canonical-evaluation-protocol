## DEBT-0001 — OKF Validator Warned On Example Links In AGENTS.md

- **ID**: DEBT-0001
- **Title**: OKF validator warns on example links in `AGENTS.md`
- **Date**: 2026-06-27
- **Found By**: Codex
- **Area**: OKF validation
- **Description**: `uv run python tools/validate_okf.py` previously exited successfully but warned that example links like `./CEP-0000-derivation-ladder.md` in `AGENTS.md` did not resolve from the repo root.
- **Why It Matters**: Non-fatal warning noise could hide future link warnings that do matter.
- **Recommended Repair**: Teach `tools/validate_okf.py` to ignore links inside fenced code blocks, or rewrite the example navigation block so its example links are not parsed as real repo links.
- **Priority**: Low
- **Scope Note**: Out of scope for phases 0-3 because validation exits zero and the warnings come from instructional examples, not public spec navigation.
- **Status**: Closed — fixed by ignoring fenced code blocks and making broken concept-document links fail in `tools/validate_okf.py`.
