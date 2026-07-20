# Setting the cursor

<!-- Author's rewrite, 2026-07-19: care section, Saint-Exupéry, attention budget,
and the 3X phase walk cut; philosophers demoted to hyperlinks; cut material
preserved in the Graveyard below the rule. Placeholders: two figure slots, two
citation links. Author's desk flags: grammar "that we'll be hard to revisit";
"Or, on the contrary" Gallicism; antecedent of "it" in the price sentence;
optional single worked instance in the two-clock summary. -->

[FIGURE: the fader — what we delegate: none | the doing | the understanding]

In a previous essay I argued agents allow us to choose whether to pay for
comprehension and do something ourselves, or to borrow that comprehension by
delegating to an AI. That "comprehension cursor" is an ownership boundary between
the agent and ourselves.

I can now choose never to be late on my projects: I can accelerate them by increasing
agent use, delegating more. The price I pay is that it will gradually increase my cognitive
debt, the gap between what I have shipped and what I understand. Or, on the contrary, I can choose
to keep in close contact with the critical pieces, maintaining a tight ownership and a thorough
understanding. The difference is how fast I accept being proven wrong.

For instance, when I used to code in C++ I sometimes joked that my job was being proven wrong by
a compiler all day. Indeed, just like any model, [my internal understanding](https://pages.cs.wisc.edu/~remzi/Naur.pdf) of a system is [only ever "scientific" if it can be falsified](https://plato.stanford.edu/entries/popper/). Otherwise it's not much better than astrology.

So the "comprehension cursor" is not really about who writes the code (the
agent or the human) but where we accept the risk of being proven wrong. When we
delegate nothing, falsifiability happens continuously (through, e.g., a type-checker, a
compiler…). As we delegate more, falsifiability happens later (maybe at the
diff/PR level). If we delegate everything, the falsification still happens, but it no longer
benefits us: we stopped making calibrated predictions, so the signal arrives with
no expectation of ours to correct.

[FIGURE: blast-radius histogram over modules — the allocation profile]

I deliberately offer no metrics or units here, as they would instantly become bad
targets: this allocation is a judgement call, not something that can be
programmatically optimised. Allocating judgement itself requires judgement, and as
we move up the ladder — function, file, module, project, job, career —
time-to-falsifiability increases: high on the ladder we only consent to being
proven wrong slowly.

To summarise, setting the cursor is done region by region, by answering two questions:

- Q1, the epistemic clock: when will reality grade this region? If we’re wrong, how large is the blast radius, and are there decisions that we'll be hard to revisit?
- Q2, the survival clock: what is the cost of being late — of missing the time to market?

Each answer, on its own, implies a cursor position. When they agree, no judgement is spent. When they disagree, judgement is what resolves the conflict.

Here are the tradeoffs:

|                | Delegate nothing | Delegate the doing | Delegate the understanding |
|----------------|------------------|--------------------------|----------------------------|
| Falsifiability | Continuous       | At the diff — if we grade it | Does not benefit you    |
| Speed          | Slow             | Fast                     | Fastest                    |
| Cognitive debt | Low              | Depends on our verification | High, if artifact survives |
| Understanding  | High             | Retained, if deliberate  | Low                        |

As an illustration, let's consider [Kent Beck's "3X" framework](https://medium.com/@kentbeck_7670/the-product-development-triathlon-6464e2763c46) (eXplore, eXpand, eXtract).

A startup begins in *eXplore* mode, where the aim is to discover their value by testing many hypotheses very quickly. In that mode, the founders will probably delegate code to an agent because being fast is more important than being exactly right at that stage. Indeed, most of the code will not survive in this phase, whether written by a human or an LLM so it can be thought of as ["necessary waste"](https://www.leanproduction.com/essence-of-lean/#:~:text=is%20required.%20Create-,Necessary%20Waste,-?The%20customer%20would).
However, deciding which hypotheses to test is where they spend their judgement.

In the *eXpand* phase, scale problems start to appear. To solve the bottlenecks, some design and architectural changes will be necessary: we want to keep human judgement involved in deciding which ones are ["1-way doors"](https://www.producttalk.org/glossary-discovery-one-way-door-decision/?srsltid=AfmBOooIbhTkPa-OxVL0QiBvsBv9uSnykrJm5SfBDA1HbrTCloaSV6Y7) and keep a deep understanding of the trade-offs we are making.  Other areas are well-understood and gradually stabilising: these can be fully delegated.

When we reach the *eXtract* phase, we have standard operating procedures, which can be automated by agents. Humans should still preserve understanding and judgement of the system's key invariants.

Once the cursor is set, there are forces that will change its position if not
countered:

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
