# Scratchbook

Raw LLM contributions, quarantined. One file per agent — agents write only to their
own file, which removes write conflicts and keeps provenance a field rather than a
judgment.

- `claude.md`
- `chatgpt.md`
- `gemini.md`

## Rules

1. Agents append to their own file only. They do not write essays, `reviewed.md`,
   or each other's scratchbooks.
2. Nothing moves from here into an essay directly. An idea is promoted by the author
   writing it into `../shared/reviewed.md` **in his own words, with the argument
   reconstructed** — not by editing a status field. The reconstruction is the point;
   it is a calibration event, and it is where the borrowing gets paid back.
3. Essays may cite `reviewed.md`. Essays may not cite the scratchbook.

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
