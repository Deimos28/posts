#!/usr/bin/env python3
"""Advisory publishing-risk review. NEVER gates.

Reviews changed essay files (draft.md, published.md) against the checklist in
shared/publishing-risks.md and writes a short report to the GitHub Actions step
summary. Findings are questions for the author, not verdicts. The author may
reject every one of them; the point is that the risks are surfaced, not that
they are obeyed.

Exit code is always 0. If the review cannot run, the summary says so."""
import os, sys, json, subprocess, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SUMMARY = os.getenv("GITHUB_STEP_SUMMARY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")

def out(md: str):
    print(md)
    if SUMMARY:
        with open(SUMMARY, "a") as f:
            f.write(md + "\n")

def changed_essays():
    base = os.getenv("BEFORE_SHA", "HEAD~1")
    try:
        diff = subprocess.run(["git", "diff", "--name-only", base, "HEAD"],
                              capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        diff = subprocess.run(["git", "show", "--name-only", "--format=", "HEAD"],
                              capture_output=True, text=True).stdout
    files = [f for f in diff.splitlines()
             if f.startswith("essays/") and f.endswith(("draft.md", "published.md"))]
    return [ROOT / f for f in files if (ROOT / f).exists()]

def main():
    targets = changed_essays()
    if not targets:
        print("No essay drafts changed; risk review skipped.")
        return 0
    key = os.getenv("GEMINI_API_KEY")
    checklist = (ROOT / "shared/publishing-risks.md").read_text()
    if not key:
        out("### Publishing-risk review\n\n_Could not run: no API key. "
            "Read shared/publishing-risks.md against the draft yourself._")
        return 0
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=key)

    rubric = f"""You are a careful, skeptical reader helping an author see risks in his
own draft. The author decides; you only surface.

Below is his own checklist of publishing failure modes, then the draft.

Return ONE JSON object, nothing else:
{{"findings": [{{"risk": "<checklist item name>", "quote": "<short verbatim passage>",
"question": "<one question for the author>"}}]}}

Rules: at most 3 findings, and only ones you can support with a verbatim quote.
Phrase each as a question, not a verdict. If the draft is clean against the
checklist, return {{"findings": []}} — that is a good outcome, not a failure.

--- CHECKLIST ---
{checklist}
"""
    for f in targets:
        rel = f.relative_to(ROOT)
        try:
            resp = client.models.generate_content(
                model=MODEL,
                contents=f"{rubric}\n--- DRAFT ({rel}) ---\n{f.read_text()}",
                config=types.GenerateContentConfig(temperature=0.0))
            t = resp.text.strip()
            t = t.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            findings = json.loads(t).get("findings", [])
        except Exception as e:
            out(f"### Publishing-risk review — {rel}\n\n_Could not run: {e}. "
                "Read shared/publishing-risks.md against the draft yourself._")
            continue
        out(f"### Publishing-risk review — {rel}\n")
        out("_Advisory. You may reject every item; the point is that you saw them._\n")
        if not findings:
            out("No findings against the checklist.\n")
        for i, x in enumerate(findings[:3], 1):
            out(f"**{i}. {x.get('risk','?')}**")
            out(f"> {x.get('quote','')}\n")
            out(f"{x.get('question','')}\n")
    return 0

if __name__ == "__main__":
    sys.exit(main())
