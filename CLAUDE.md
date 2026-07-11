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
