#!/usr/bin/env python3
"""LLM gating check. Reviews each published.md for claim support and returns a
strict verdict. Gates publishing: exits non-zero on any FAIL.

Design notes:
- Deterministic-ish: temperature 0, explicit rubric, structured verdict.
- Fails CLOSED only on an explicit FAIL verdict, not on API errors (an API outage
  should not silently block a correct essay — it errors loudly instead, which is a
  visible CI failure the author can re-run, not a false content verdict).
- The model judges support/consistency, NOT truth. It flags unsupported claims for
  human review; it is a smoke detector, not an oracle.
"""
import os, sys, pathlib, json

ROOT = pathlib.Path(__file__).resolve().parent.parent
TARGETS = sorted(ROOT.glob("essays/**/published.md"))

RUBRIC = """You are a careful editor. Review the essay below for INTERNAL problems only:
1. Claims presented as fact that the essay itself neither supports nor attributes.
2. Internal contradictions.
3. Attributions or quotes that the essay presents as sourced but leaves dangling.

Do NOT judge whether claims are true in the world. Do NOT judge style or opinion.
Respond with a single JSON object, no prose, no code fence:
{"verdict": "PASS" | "FAIL", "issues": ["short issue", ...]}
PASS if you find no clear instance of 1-3. Be conservative: only FAIL on a clear,
specific problem you can name in "issues"."""

def main():
    if not TARGETS:
        print("No published.md files; LLM check skipped.")
        return 0
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        print("::error::GEMINI_API_KEY not set; cannot run gating LLM check.")
        return 1
    import google.generativeai as genai
    genai.configure(api_key=key)
    model = genai.GenerativeModel("gemini-1.5-flash",
        generation_config={"temperature": 0.0, "response_mime_type": "application/json"})
    failed = False
    for f in TARGETS:
        essay = f.read_text()
        try:
            resp = model.generate_content(f"{RUBRIC}\n\n---ESSAY---\n{essay}")
            data = json.loads(resp.text)
        except Exception as e:
            print(f"::error file={f.relative_to(ROOT)}::LLM check could not complete: {e}")
            return 1  # loud infra failure, not a content verdict; re-run
        verdict = str(data.get("verdict", "")).upper()
        issues = data.get("issues", [])
        if verdict == "FAIL":
            failed = True
            for it in issues:
                print(f"::error file={f.relative_to(ROOT)}::LLM: {it}")
            print(f"  {f.relative_to(ROOT)}: FAIL ({len(issues)} issue(s))")
        else:
            print(f"  {f.relative_to(ROOT)}: PASS")
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main())
