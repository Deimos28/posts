# Essay 2b: Setting the cursor — plan (rewritten 2026-07-15)

# Setting the cursor

<!-- Faithful transcription of the author's manuscript (notebook, Tuscany, July
2026). The prose is the author's, verbatim, including constructions he may still
edit. Bracketed ALL-CAPS notes are transcription flags, not prose. Figures are
placeholders for the hand-drawn originals, to be photographed at home. -->

[FIGURE: the fader — what we delegate: none | the doing | the understanding]

In a previous essay I argued agents allow us to choose whether to pay for
comprehension and do something ourselves, or to borrow that comprehension by
delegating to an AI. That "comprehension cursor" is an ownership boundary between
the agent and ourselves.

I can choose never to be late on my projects: I can accelerate them by increasing
agent use, delegating more. The price I pay is that I stop topping up my leaky
comprehension reservoir, which will gradually increase my cognitive debt, the gap
between my model of the world and the world itself. [FLAG: 2a defines cognitive
debt artifact-relatively — the gap between what is shipped and what is understood;
decide at the desk whether to align.] This can be extremely valuable when trying
to rapidly test as many hypotheses as possible, e.g. when in the "Explore" phase
of Kent Beck's 3X model. But the human still owns the decision of which hypothesis
to check. When reaching the Expand phase, the stable areas can be fully delegated.
But the bottlenecks to growth, the one-way doors, should not be, lest we accrue
debt that will cap the expansion. In the last phase of the model, the Extract, we
should definitely delegate all routine work, such as standard operating
procedures, but keep a tight ownership and thorough understanding of critical
invariants. The areas where we keep ownership, where the comprehension cursor is
fully "to the left", are those where we take the risk of being proven wrong.

When I coded in C++ I used to sometimes joke that my job was being proven wrong by
a compiler all day. As Naur said, the programs I built were a theory; but Popper
says a theory is only knowledge if it is falsifiable, i.e. that it can be proven
wrong. So the "comprehension cursor" is not really about who writes the code (the
agent or the human) but where we accept the risk of being proven wrong. When we
delegate nothing, falsifiability happens continuously (through the type-checker,
the compiler). As we delegate more, falsifiability happens later (maybe at the
diff/PR level). If we delegate everything, the falsification does not benefit us,
because we stopped making calibrated predictions. Making those predictions,
risking being wrong, is a demonstration of care.

To distinguish themselves from AI slop, some authors hand-write and scan their
notes, as a proof of effort, of care. Care requires volition, which is why being
compelled to write thousands of lines of code by hand is not necessarily care.
Choosing the dispensable unpleasantness, the friction, for a longer-term benefit
is what turns it into care: "it's the time you lost for your rose which makes your
rose so important" says Saint-Exupéry's fox in Le Petit Prince. [FLAG: translation
lineage to decide — Woods has "wasted"; "lost" is the author's rendering of
"perdu"; consider "(my translation)" or the French.] That care does not need to be
evenly distributed, though.

We humans have a capped "amount" of care and attention we can spend. As the
potential objects of that care greatly exceed our attention budget, we should
allocate wisely to maximise its impact.

[FIGURE: attention bar — total attention needed vs human attention, remainder LLM]
[FIGURE: blast-radius histogram over modules — the allocation profile]

I deliberately offer no metrics or units here, as they would instantly become bad
targets: this allocation is a judgement call, not something that can be
programmatically optimised. Allocating judgement itself requires judgement, and as
we move up the abstraction layer (function, file, module, project, job, career),
time-to-falsifiability increases: high on the ladder we only consent to being
proven wrong slowly.

To summarise, setting the cursor is done region by region, by answering two questions:

- Q1, the epistemic clock: when will reality grade this region if we’re wrong — how large is the blast radius, and are there one-way doors that never reopen?
- Q2, the survival clock: what is the cost of being late — of missing the time to market? Each answer, on its own, implies a cursor position.

When they agree, no judgement is spent. When they disagree, judgement is what resolves the conflict.

Here are the tradeoffs:

| Stakes         | Nothing    | Doing      | Understanding              |
|----------------|------------|------------|----------------------------|
| Falsifiability | Continuous | Diff-level | Does not benefit you       |
| Speed          | Slow       | Fast       | Fastest                    |
| Cognitive debt | Low        | Medium     | High, if artifact survives |
| Understanding  | High       | Medium     | Low                        |

Once the cursor is set, there are forces that will change its position if not
countered:

- deadlines, judgement erosion, and convenience push it to the right;
- sunk-cost fallacy, gold-plating, rabbit-holing push it to the left.

Controlling the cursor is the subject of the next essay.



---

# 🪦Graveyard


Supersedes the early-July plan, which predated the consent/care synthesis and exited
to essay 3 instead of 2c. Structure below is author-decided (conversation,
2026-07-15); open questions marked.

## Two purposes (author's words)
1. Bridge 2a → 2c: deliver 2a's promise (how to set the cursor, concretely) and end
   on "the inventory of practices is the subject of the next essay."
2. Cover falsifiability and care to clarify the attribution between agent and human —
   the role and scope of the agent. These discussions establish what the 2c
   techniques are FOR.

## Thesis (reviewed.md)
The link between care, falsifiability, attention, and judgement — that link is the
cursor. It sets the boundary of the domain where we consent to being proven wrong,
not "who writes the code."

## Structure (reconciled 2026-07-17 to the manuscript — the draft is now authority)

Draft exists in the author's notebook through the care section. Order as written:

1. Opening: 2a recap in first person; the cursor as ownership boundary; the price
   ("I stop topping up my leaky comprehension reservoir"). [DRAFTED]
2. Phase walk: Explore / Expand / Extract with the stakes-vs-routine partition
   inline (hypothesis; bottlenecks and 1-way doors; invariants vs SOP). [DRAFTED]
3. Falsification: compiler joke → Naur → Popper → the cursor restated as "where we
   accept the risk of being proven wrong" → the three delegation stops (continuous /
   diff-PR / does not benefit us — "we stopped making calibrated predictions").
   [DRAFTED]
4. Care: predictions-as-demonstration-of-care hinge → external door (hand-scanned
   notes vs slop) → volition (compelled lines ≠ care) → the rose ("time you lost")
   → "care does not need to be evenly distributed". [DRAFTED]
5. Allocation: capped care/attention; the attention bar and blast-radius histogram
   (two small hand-drawn figures); no metrics on purpose (instant bad targets;
   judgement call, not programmatically optimisable); recursion absorbed HERE —
   allocating judgement requires judgement; the ladder in time-to-falsifiability;
   consent-slowly at altitude. [DRAFTED]
6. The procedure: three questions, compact. [NEXT]
7. Force field as the close: curiosity and skin-in-the-game left, deadline gravity
   right; the ungripped fader drifts; what holds the middle detent → bridge to 2c.
   [NEXT]

Decisions recorded:
- WALKTHROUGH CUT (author, 2026-07-17): painful and risky to write, low value —
  its "concretely" job is now done by the phase walk, the procedure, and the
  histogram. Optimising time-to-ship given field convergence (Storey/Osmani/RCT).
  Optional one-sentence acknowledgment of the cut in §6.
- Recursion is NOT a separate closing section; it lives inside §5. The close is
  the force field.
- Figures: fader + attention bar + blast-radius histogram, all hand-drawn. Decide
  at assembly whether all three ship.
- Rose quote: decide translation lineage at typing (Woods "wasted" vs author's
  "lost" + note, vs French original).

Budget: ~1,500 words unchanged; walkthrough's ~400 redistributed (care and
allocation are running longer than planned, correctly).

## Moved out of this essay
- Dependency inversion → 2c (it is a practice, not a policy).
- Economics → essay 3 entirely; at most one chaining sentence, possibly none since
  the bridge now points at 2c.
- Elicitation cost-curve constraint → 2c (practice-level).
- Premise defense (implementation as the only default-on refresh; debugging,
  incidents, reading are episodic) — optional aside in §2 if space allows; cuttable.

## Open questions
- §2 scope of care (above).
- §6 walkthrough episode.
- The antirez altitude crux (scratchbook/claude.md: "Antirez divergence") is
  2b-adjacent — it is a question about cursor LEVEL. Include as one honest open
  paragraph near §5, or hold for later? [Author's call; the essay survives either
  way.]

## Register
2a's length and voice. Publishing-risks checklist applies; notes are dense, prose
exposes the minimum conceptual surface.
