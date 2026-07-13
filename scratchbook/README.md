# Scratchbook

Raw LLM contributions, quarantined. One file per agent — agents write only to their
own file, which removes write conflicts and keeps provenance a field rather than a
judgment.

- `claude.md`
- `chatgpt.md`
- `gemini.md`

## Rules

1. Conceptual contributions go only to the agent's own file. Agents do not write to
   `reviewed.md`, another agent's scratchbook, or essay prose. Essay notes may reference
   a scratchbook entry by title under the restrictions in `../CLAUDE.md`.
2. Agents propose scratchbook changes through a draft pull request and do not merge it.
3. Merging the pull request records the proposal. It does not promote the idea.
4. Promotion happens when the author writes the idea into `../shared/reviewed.md` in his
   own words, with the argument reconstructed. The reconstruction is the calibration
   event and the point where the borrowing gets paid back.
5. Essays may cite `reviewed.md`. Essays may not cite the scratchbook.

## Pull-request review

The pull request should identify:

- the question or task that produced the contribution;
- the entries added or changed;
- claims or analogies that remain uncertain;
- the judgment required from the author;
- files deliberately left untouched.

Author approval to merge means that the repository should retain the proposal. It does
not mean that the proposal is accepted as part of the argument.

## Intended use: adversarial elicitation

Put the same question to two models independently, without showing either the other's
answer. Convergence is weak evidence — they share training distributions and both
optimise for agreeableness. **Divergence is the signal**: it marks where judgment is
actually required, and the errors are less correlated there. Resolved disagreements
earn an entry in `reviewed.md` even when the resolution is easy, because a resolved
disagreement is a calibration event.

This protocol is affordable only because tokens are cheap — the same repricing that
made speculative-change probes possible.

## Health signal

A growing scratchbook with a stagnant `reviewed.md` is borrowed-but-unmetabolised
idea debt, and it is directly observable. Watch the ratio.

## Entry format

```
## <short claim or idea>
Date:
Raw contribution: what the model proposed.
Why it might matter: the problem it could solve or the distinction it draws.
Status: unresolved | promoted to reviewed.md | rejected (with reason)
```
