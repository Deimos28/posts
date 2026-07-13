# Instructions for working in this repo

## Style
Target register: Martin Kleppmann. Plain declarative sentences. Claims stated once,
without amplification. Uncertainty marked honestly. No drama in transitions.

Banned constructions:
- Validating openers ("You're right, and...", "Exactly, and...")
- "Not X but Y" rhetorical inversions
- Superlative pronouncements ("that's the essay", "this is the strongest...")
- Dramatic transitions ("And here's the thing...", "But notice what happens...")

Notes files may use bullets. Essay drafts are prose.

## Verification rule
Before anything is published:
1. Every factual claim, citation, and attribution is checked against a primary source.
2. Every coined term is searched for prior art (the term may exist; cite it if so).
3. Quotes are verified verbatim against the source.
Open items live in `shared/claims-to-verify.md`. Do not delete an item; mark it
verified with a date and the source.

## Vocabulary
`shared/vocabulary.md` is canonical. If an essay needs a term to mean something
different, the vocabulary file changes first, in its own commit.

## Layout
- `essays/<nn>-<slug>/notes.md` — working notes, structure, open questions
- `essays/<nn>-<slug>/draft.md` — the current draft (prose)
- `essays/<nn>-<slug>/published.md` — frozen copy of the published text; never edited
  except to record errata in a marked section
- `shared/figures/` — diagram sources and exports

## Git
Branches for revision experiments (e.g. a style rewrite pass to diff against the
original), merged or abandoned. Essays are directories on main, not branches.

## LLM contribution boundary

Agents may critique, interrogate, research, verify, propose structure, surface
alternatives, generate objections, draw figures, and maintain CI.

Agents do not write publishable essay prose. Prose is becoming-knowledge for the
author: the mechanism arrives while sentences are being formed, not before. Every
sentence that appears in an essay is written by the author, including the ones an
agent would write better — the point is not the sentence, it is what writing it does
to the model in his head.

Agent-originated ideas go to `scratchbook/<agent>.md`, never directly into an essay.
Promotion happens in `shared/reviewed.md`, written by the author, with the argument
reconstructed in his own words. Essays cite `reviewed.md`, never the scratchbook.

When proposing structure, offer **options and questions, not a scaffold to fill in**.
An outline silently proposes an option space; exploration with the teacher still
requires the author bringing his own candidates. Prefer "what do these have in
common? (my read: X — but check whether it holds for Y)" over "Section 3: argue X."

## Repository asymmetry

Notes may be dense and use the full internal vocabulary. Published prose exposes the
minimum conceptual surface the argument needs. See `shared/publishing-risks.md`.

## Writing conflicts

Agents write only to their own scratchbook file, plus notes files under `essays/`
with one restriction: notes may carry logistics, structure the author has decided,
and open questions — but an agent-elaborated idea goes to the scratchbook, and notes
reference it by entry title rather than inlining the content. Essay prose
(`draft.md`, `published.md`), `shared/reviewed.md`, and the vocabulary are
single-writer (the author). This is why branch protection is not required: the write
domains do not overlap.
