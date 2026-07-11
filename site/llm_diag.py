#!/usr/bin/env python3
"""One-shot diagnostic: what can this key actually do? Prints SDK version, the models
available to the key, and the result of a tiny generate call. Never gates."""
import os, sys, traceback
print("=== LLM diagnostic ===")
try:
    import google.genai as _g
    print("google-genai importable")
except Exception as e:
    print("import google.genai FAILED:", e); sys.exit(0)

key = os.getenv("GEMINI_API_KEY")
print("GEMINI_API_KEY present:", bool(key))
if not key:
    sys.exit(0)

from google import genai
from google.genai import types
client = genai.Client(api_key=key)

print("\n--- models available to this key (name : supported actions) ---")
try:
    for m in client.models.list():
        actions = getattr(m, "supported_actions", None) or getattr(m, "supported_generation_methods", None)
        print(f"  {m.name}  {actions}")
except Exception as e:
    print("models.list() error:", type(e).__name__, e)

for model in ("gemini-2.0-flash", "gemini-flash-latest", "gemini-1.5-flash"):
    print(f"\n--- tiny call: {model} ---")
    try:
        r = client.models.generate_content(
            model=model, contents="Reply with the single word OK.",
            config=types.GenerateContentConfig(temperature=0.0))
        print("  OK ->", repr(r.text[:60]))
    except Exception as e:
        print("  ERROR:", type(e).__name__, str(e)[:200])

# --- also exercise the real review path and print raw verdict ---
print("\n=== real review path (JSON verdict) ===")
try:
    import importlib.util, pathlib
    spec = importlib.util.spec_from_file_location("llm_check", "site/llm_check.py")
    lc = importlib.util.module_from_spec(spec); spec.loader.exec_module(lc)
    for f in sorted(pathlib.Path("essays").glob("**/published.md")):
        try:
            v, issues = lc.review_one(client, f.read_text())
            print(f"  {f}: verdict={v} issues={issues}")
        except Exception as e:
            print(f"  {f}: review_one ERROR {type(e).__name__}: {str(e)[:300]}")
except Exception as e:
    print("  diag review path error:", type(e).__name__, str(e)[:200])
