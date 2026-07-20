# Setting the cursor

<!-- Author's essay, July 2026. Figures live in shared/figures (inlined at
build). The Graveyard below the horizontal rule is working stock and must NOT be
copied into published.md — CI now checks for this. -->

![The comprehension cursor: a fader from paying for comprehension to borrowing it](figures/cursor-fader.svg)

In [a previous essay](https://deimos28.substack.com/p/the-comprehension-cursor) I argued agents allow us to choose whether to pay for
comprehension and do something ourselves, or to borrow that comprehension by
delegating to an AI. That "comprehension cursor" is an ownership boundary between
the agent and ourselves.

I can now choose never to be late on my projects: I can accelerate them by increasing
agent use, delegating more. The price I pay is a gradual increase in my cognitive
debt, the gap between what I have shipped and what I understand. I can instead retain ownership and a thorough understanding of the critical pieces. The difference is how quickly I can identify and correct errors.

For instance, when I used to code in C++ I sometimes joked that my job was being proven wrong by
a compiler all day. Indeed, just like any model, [my internal understanding](https://pages.cs.wisc.edu/~remzi/Naur.pdf) of a system [cannot be calibrated if it never risks contradiction](https://plato.stanford.edu/entries/popper/). Otherwise it's not much better than astrology.

So the "comprehension cursor" is not really about who writes the code (the
agent or the human) but when and where we accept being checked and corrected. When we
delegate nothing, our internal model is tested continuously, through many small decisions, challenged by the type system, the tests, the executions. As we delegate more, our model is tested later, at selected checkpoints (maybe at the
diff/PR level). If we delegate everything, reality can still expose errors, but the signal no longer calibrates us: we formed no expectation of our own for it to revise.

![Attention allocated unevenly across modules: the critical few receive most of it](figures/cursor-allocation.svg)

I deliberately offer no metrics or units here, as they would instantly become bad
targets: this allocation is a judgement call, not something that can be
programmatically optimised. Allocating judgement itself requires judgement, and as
we move up the ladder — function, file, module, project, job, career —
evidence generally arrives later, noisier, and is harder to attribute. High on the ladder we only consent to being
 corrected slowly.

To summarise, setting the cursor is done region by region, by answering two questions:

- Q1, the epistemic clock: how long will we likely stay wrong, and at what cost? A proxy for this is the commit history (the lag between a change touching the region and the bug-fix, revert, or an incident that later referenced it).
- Q2, the survival clock: what is the cost of being late — of missing the time to market? We can estimate this using runway, committed dates, the [cost of delay](https://en.wikipedia.org/wiki/Cost_of_delay).

I deliberately offer no formula for converting these signals into a cursor position because whilst the clocks can be informed by evidence, their relative importance remains a judgement call.

Each clock pulls the cursor in one direction. When they point in the same direction, cursor placement is easy. When they conflict, judgement is what resolves the conflict.

Here are the tradeoffs:

|                | Delegate nothing | Delegate the doing | Forgo understanding |
|----------------|------------------|--------------------------|----------------------------|
| Corrections | Continuous       | At the diff — if we grade it | Does not calibrate us   |
| Potential acceleration | None      | Some                     | Most                       |
| Cognitive debt | Low              | Depends on our verification | High, if artifact survives |
| Understanding  | High             | Retained, if deliberate  | Low                        |

As an illustration, let's consider [Kent Beck's "3X" framework](https://medium.com/@kentbeck_7670/the-product-development-triathlon-6464e2763c46) (eXplore, eXpand, eXtract).

A startup begins in *eXplore* mode, where the aim is to discover what creates value for its customers by testing many hypotheses very quickly. In that mode, the founders will probably delegate code to an agent because being fast is more important than being exactly right: the implementation needs only enough fidelity to test the hypothesis so the survival clock dominates. Indeed, most of that experimental code will not survive, whether written by a human or an LLM.
However, deciding which hypotheses to test is where they spend their judgement.

In the *eXpand* phase, scale problems start to appear. This is the phase where the clocks conflict most sharply because the cost of delay remains acute and the cost of remaining wrong rises due to scale, dependencies, and increasingly irreversible choices. To solve the bottlenecks, some design and architectural changes will be necessary: the founders will want to keep human judgement involved in identifying which architectural choices are ["one-way doors"](https://www.producttalk.org/glossary-discovery-one-way-door-decision/?srsltid=AfmBOooIbhTkPa-OxVL0QiBvsBv9uSnykrJm5SfBDA1HbrTCloaSV6Y7) and keep a deep understanding of the trade-offs they are making. Other areas are well-understood and gradually stabilising: 
routine work in these areas can be delegated more aggressively.

When the startup reaches the *eXtract* phase, there might be standard operating procedures, which can be automated by agents. Humans should still preserve understanding and judgement of the system's key invariants.


Even after you make a deliberate choice about where to place the cursor, the environment will actively try to move it:

- deadlines, judgement erosion, and convenience push it to the right;
- sunk-cost fallacy, gold-plating, rabbit-holing push it to the left.

How to maintain the cursor in the position we want is the subject of the next essay.



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
