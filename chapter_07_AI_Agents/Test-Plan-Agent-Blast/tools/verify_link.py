"""Phase 2 (Link) handshake verification.

Confirms, before any full logic is written, that:
  1. Jira credentials work            -> GET /rest/api/3/myself
  2. The Acceptance Criteria field can be discovered -> GET /rest/api/3/field
  3. Groq is reachable and the configured model is available -> GET /openai/v1/models

Reads credentials from .env only. Never prints secrets.
Exit code 0 = all links healthy, 1 = at least one link is broken.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import requests
from dotenv import dotenv_values

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
TIMEOUT = 15

AC_HINTS = ("acceptance", "definition of done", "dod")


def load_env() -> dict[str, str]:
    if not ENV_PATH.exists():
        print(f"[FAIL] .env not found at {ENV_PATH}")
        sys.exit(1)
    values = {k: (v or "").strip() for k, v in dotenv_values(ENV_PATH).items()}
    required = ["JIRA_URL", "JIRA_EMAIL", "JIRA_API_TOKEN", "GROQ_API_KEY", "GROQ_MODEL"]
    missing = [k for k in required if not values.get(k)]
    if missing:
        print(f"[FAIL] Missing required .env keys: {', '.join(missing)}")
        sys.exit(1)
    return values


def check_jira_auth(env: dict[str, str]) -> tuple[bool, str]:
    base = env["JIRA_URL"].rstrip("/")
    try:
        resp = requests.get(
            f"{base}/rest/api/3/myself",
            auth=(env["JIRA_EMAIL"], env["JIRA_API_TOKEN"]),
            headers={"Accept": "application/json"},
            timeout=TIMEOUT,
        )
    except requests.exceptions.RequestException as exc:
        return False, f"network error: {exc}"

    if resp.status_code == 401:
        return False, "401 Unauthorized - check JIRA_EMAIL and JIRA_API_TOKEN"
    if resp.status_code >= 400:
        return False, f"HTTP {resp.status_code}"

    data = resp.json()
    return True, f"authenticated as {data.get('displayName')} ({data.get('accountId')})"


def find_acceptance_fields(env: dict[str, str]) -> tuple[bool, list[tuple[str, str]]]:
    base = env["JIRA_URL"].rstrip("/")
    try:
        resp = requests.get(
            f"{base}/rest/api/3/field",
            auth=(env["JIRA_EMAIL"], env["JIRA_API_TOKEN"]),
            headers={"Accept": "application/json"},
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
    except requests.exceptions.RequestException as exc:
        return False, []

    matches = []
    for field in resp.json():
        name = (field.get("name") or "").lower()
        if any(hint in name for hint in AC_HINTS):
            matches.append((field.get("id", ""), field.get("name", "")))
    return True, matches


def check_groq(env: dict[str, str]) -> tuple[bool, str]:
    try:
        resp = requests.get(
            "https://api.groq.com/openai/v1/models",
            headers={"Authorization": f"Bearer {env['GROQ_API_KEY']}"},
            timeout=TIMEOUT,
        )
    except requests.exceptions.RequestException as exc:
        return False, f"network error: {exc}"

    if resp.status_code == 401:
        return False, "401 Unauthorized - check GROQ_API_KEY"
    if resp.status_code >= 400:
        return False, f"HTTP {resp.status_code}"

    ids = {m.get("id") for m in resp.json().get("data", [])}
    model = env["GROQ_MODEL"]
    if model not in ids:
        return False, f"model '{model}' not available ({len(ids)} models listed)"
    return True, f"model '{model}' available ({len(ids)} models total)"


def main() -> int:
    env = load_env()
    ok = True

    print("=== Phase 2 (Link) handshakes ===")

    passed, detail = check_jira_auth(env)
    ok &= passed
    print(f"[{'PASS' if passed else 'FAIL'}] Jira auth       -> {detail}")

    passed, fields = find_acceptance_fields(env)
    ok &= passed
    if not passed:
        print("[FAIL] Jira fields     -> could not read /rest/api/3/field")
    elif fields:
        print(f"[PASS] Jira fields     -> acceptance-related fields found: {len(fields)}")
        for field_id, name in fields:
            print(f"                        {field_id}  {name}")
    else:
        print("[PASS] Jira fields     -> readable, but no Acceptance Criteria field on this site")

    passed, detail = check_groq(env)
    ok &= passed
    print(f"[{'PASS' if passed else 'FAIL'}] Groq models     -> {detail}")

    print("=== result:", "ALL LINKS HEALTHY" if ok else "LINK(S) BROKEN", "===")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
