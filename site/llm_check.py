#!/usr/bin/env python3
"""LLM gating check (current google-genai SDK).

Semantics:
  - A clear FAIL verdict on essay content -> gate fails (exit 1). Strict.
  - A PASS verdict -> ok.
  - A transient infrastructure failure (timeout, 429, 5xx, transport) is NOT a
    verdict: the check "did not run". Retry with backoff. If still unrun after all
    retries, exit code 2 (distinct from a content FAIL's exit 1) so the workflow can
    retry the whole step. Never treat "did not run" as pass or fail.

Only essays/**/published.md are checked.
"""
import os, sys, json, time, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TARGETS = sorted(ROOT.glob("essays/**/published.md"))
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

RUBRIC = """You are a careful editor. Review the essay for INTERNAL problems only:
1. Claims presented as fact that the essay itself neither supports nor attributes.
2. Internal contradictions.
3. Attributions or quotes presented as sourced but left dangling.

Do NOT judge whether claims are true in the world. Do NOT judge style or opinion.
Respond with ONE JSON object and nothing else:
{"verdict": "PASS" | "FAIL", "issues": ["short specific issue", ...]}
Be conservative: only FAIL on a clear, specific, nameable problem."""

# exit codes
OK, CONTENT_FAIL, DID_NOT_RUN = 0, 1, 2

TRANSIENT = ("timeout", "deadline", "429", "rate limit", "resource exhausted",
             "500", "502", "503", "504", "unavailable", "internal error",
             "connection", "temporarily")

def is_transient(err: Exception) -> bool:
    s = str(err).lower()
    return any(t in s for t in TRANSIENT)

def review_one(client, essay: str):
    """Return (verdict, issues) or raise for transient errors."""
    from google.genai import types
    resp = client.models.generate_content(
        model=MODEL,
        contents=f"{RUBRIC}\n\n---ESSAY---\n{essay}",
        config=types.GenerateContentConfig(
            temperature=0.0, response_mime_type="application/json"),
    )
    data = json.loads(resp.text)
    return str(data.get("verdict", "")).upper(), data.get("issues", [])

def main():
    if not TARGETS:
        print("No published.md files; LLM check skipped.")
        return OK
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        print("::error::GEMINI_API_KEY not set; check did not run.")
        return DID_NOT_RUN

    from google import genai
    client = genai.Client(api_key=key)

    content_failed = False
    for f in TARGETS:
        rel = f.relative_to(ROOT)
        essay = f.read_text()
        last_err = None
        for attempt in range(1, 5):          # up to 4 in-script attempts
            try:
                verdict, issues = review_one(client, essay)
                last_err = None
                break
            except Exception as e:
                last_err = e
                if is_transient(e) and attempt < 4:
                    wait = 2 ** attempt       # 2,4,8s backoff
                    print(f"  {rel}: transient error (attempt {attempt}), retrying in {wait}s: {e}")
                    time.sleep(wait)
                    continue
                break
        if last_err is not None:
            # could not obtain a verdict: did not run
            print(f"::error file={rel}::LLM check did not run: {last_err}")
            return DID_NOT_RUN
        if verdict == "FAIL":
            content_failed = True
            for it in issues:
                print(f"::error file={rel}::LLM: {it}")
            print(f"  {rel}: FAIL ({len(issues)} issue(s))")
        elif verdict == "PASS":
            print(f"  {rel}: PASS")
        else:
            # unparseable verdict = malformed run, treat as did-not-run and retry
            print(f"::error file={rel}::LLM returned no clear verdict; did not run.")
            return DID_NOT_RUN
    return CONTENT_FAIL if content_failed else OK

if __name__ == "__main__":
    sys.exit(main())
