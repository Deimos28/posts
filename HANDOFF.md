# Handoff — state of work

For any agent joining or resuming. Read `CLAUDE.md` first (binding rules), then this
file (current state), then the primary sources it points to. Do not learn the ideas
from this file: it is logistics and pointers, kept deliberately thin so no agent's
summary becomes the option space.

## Reading order
1. `CLAUDE.md` — style, contribution boundary, writing domains, verification rule.
2. `shared/reviewed.md` — the author's own reconstructions. Author-only file.
3. `essays/02b-setting-the-cursor/notes.md` and `essays/02c-restoring-the-friction/notes.md`.
4. `scratchbook/` — raw agent contributions, per-agent files. Cite never; mine freely.
5. `shared/vocabulary.md`, `shared/claims-to-verify.md`, `shared/publishing-risks.md`.

## State (update the date when you change this file)
As of 2026-07-15:
- Published: essay 1 (Substack), essay 2a (Substack + mirror). Mirror:
  https://deimos28.github.io/posts/ — built by CI from `essays/**/published.md`.
- In progress: 2b ("setting the cursor") — thesis and establishing claims exist in
  `reviewed.md`; next action is the AUTHOR drafting prose. 2c ("the practices") —
  armoury framing settled, surprise-agent spec in reviewed.md + scratchbook analysis.
- Essay 3: stock only (`essays/03-token-economy/notes.md`, reviewed.md §3).
- CI: deterministic checks + LLM claim check GATE deploys; publishing-risk review is
  ADVISORY (run summary). All green as of this date.

## Working arrangement (summary; CLAUDE.md is authoritative)
- The author writes all essay prose. Agents: notes, structure, options, verification,
  figures, CI, critique of drafts.
- Adversarial stance, on the author's request: no ratifying openers; when the author
  compresses, ask him to unpack rather than offering candidate expansions; test his
  comprehension of load-bearing concepts; say wrong first, explain second.
- Agent-elaborated ideas go to `scratchbook/<agent>.md` only; notes may reference
  entries by title, never inline them.
- Personal-history material stays in conversation, never in the repo (standing rule,
  author's decision 2026-07-13).
- Commit as the author: user.name "Charles-Edouard Cady",
  user.email "Deimos28@users.noreply.github.com".

## Maintenance
Any agent making a change that alters this state (publishing, structural decisions,
new standing rules) updates the State section and its date in the same commit.
