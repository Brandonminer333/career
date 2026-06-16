#!/usr/bin/env python3
"""Validate deploy key format locally (no secret content written to logs)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

LOG_PATH = Path(__file__).resolve().parents[2] / ".cursor" / "debug-5c3c9d.log"
SESSION_ID = "5c3c9d"


def emit(hypothesis_id: str, message: str, data: dict) -> None:
    # #region agent log
    entry = {
        "sessionId": SESSION_ID,
        "timestamp": int(time.time() * 1000),
        "hypothesisId": hypothesis_id,
        "location": ".github/scripts/debug-deploy-key.py",
        "message": message,
        "data": data,
        "runId": os.environ.get("DEBUG_RUN_ID", "local-pre"),
    }
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry) + "\n")
    # #endregion


def main() -> int:
    key = os.environ.get("PROFILE_README_DEPLOY_KEY", "")
    if not key and len(sys.argv) > 1:
        key = Path(sys.argv[1]).read_text(encoding="utf-8")

    stripped = key.strip()
    emit(
        "A",
        "secret presence and shape",
        {
            "configured": bool(stripped),
            "byte_length": len(key),
            "stripped_byte_length": len(stripped),
            "line_count": 0 if not key else key.count("\n") + 1,
            "starts_with_begin": stripped.startswith("-----BEGIN"),
            "ends_with_private_end": stripped.endswith("-----END PRIVATE KEY-----")
            or stripped.endswith("-----END OPENSSH PRIVATE KEY-----"),
            "contains_literal_backslash_n": "\\n" in key,
            "contains_cr": "\r" in key,
        },
    )

    if not stripped:
        emit("A", "abort", {"reason": "PROFILE_README_DEPLOY_KEY missing"})
        print("PROFILE_README_DEPLOY_KEY is empty. Export it or pass a key file path.", file=sys.stderr)
        return 1

    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as tmp:
        tmp.write(key if key.endswith("\n") else key + "\n")
        tmp_path = tmp.name

    os.chmod(tmp_path, 0o600)
    probe = subprocess.run(
        ["ssh-keygen", "-l", "-f", tmp_path],
        capture_output=True,
        text=True,
    )
    Path(tmp_path).unlink(missing_ok=True)

    emit(
        "A",
        "ssh-keygen parse probe",
        {
            "returncode": probe.returncode,
            "fingerprint_stdout": probe.stdout.strip(),
            "fingerprint_stderr": probe.stderr.strip(),
        },
    )

    emit(
        "B",
        "echo write simulation",
        {
            "note": "workflow uses echo to write key; compare parse result above",
        },
    )

    if probe.returncode != 0:
        print("Deploy key failed local parse (matches libcrypto failure).", file=sys.stderr)
        print(probe.stderr.strip(), file=sys.stderr)
        return 2

    print(probe.stdout.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
