# Essay 2, part 2: Setting the cursor

Picks up the published cliffhanger: "We now get to set a cursor on whether to pay for
comprehension, or borrow and move faster. How to do this is the subject of the next
essay."

## Reframe (2026-07-11): calibration is the theory; falsifiability is the criterion

Thesis restated: design workflows so that humans continue making predictions that
reality can confirm or refute. Friction was one implementation of calibration —
incidental and default-on (every keystroke embeds micro-predictions, graded
instantly). Predict-before-reveal is a deliberate implementation; armies-with-
prediction a scheduled one; debugging and incidents episodic ones. This resolves
Chat's objection about implementation's privileged role: nothing was privileged
except the default-on schedule. "Top-up" is the metaphor; "calibration event" is
the mechanism under it.

The cursor is not deciding whether to use AI. It sets the boundary of where you
remain falsifiable: paying comprehension means generating expectations specific
enough for reality to violate; borrowing means never staking one. On the borrow
side you cannot be wrong — which is the self-masking condition.

Lineage: Naur (the program is a theory held in minds) + Popper (a theory is
knowledge only to the extent it is falsifiable). Composed: borrowed comprehension
is theory that risks nothing. The fitness program is conjectures-and-refutations
run deliberately; the fear signal is what a refutation feels like from inside.
Scope: Popper is for the epistemology, a paragraph, not a framework. Verify any
quote against Conjectures and Refutations directly.

Consequences for structure:
- The four rules demote from thesis to boundary-estimators: phase, asset class,
  and blast radius are three estimates of where you must remain falsifiable.
- The recursion section survives untouched (drawing the boundary requires the
  calibrated model).
- 2b states the principle; 2c inventories the mechanisms.

Design prediction (candidate ending): a good future agent is one that
continuously elicits and tests the user's predictions rather than merely
producing correct code. Discriminates the current market: Contral's Prove mode
and Thariq's merge quiz are elicitation; explanation-on-tap is anesthetic.

Two constraints to state (else readers supply them as objections):
1. Elicitation has a cost curve: demanded before every diff it becomes a
   confirmation dialog; habituation kills it, or users learn to emit vague —
   unfalsifiable — predictions, reintroducing self-masking through the front
   door. Predictions must be specific, and elicitation rationed (Surgical
   applies to the agent's questions: high blast radius, slow oracles).
2. The blind-faith boundary holds: where verification is cheap and complete,
   eliciting predictions is friction theater. The principle governs the
   no-oracle layer only.

## Structure (agreed order)

1. **The conveyor belt** (grounds everything that follows)
   Register allocation was once judgement, then the compiler's job; boilerplate was
   once typing, now the agent's. Each generation's substance becomes the next
   generation's mechanical layer. The narrative — argument structure, decision
   structure, the why — is not on that conveyor belt, or at least we are not willing
   to put it there. Connects to essay 1's no-oracle point: the mechanical layers all
   had oracles (the compiler is right about register allocation); the narrative layer
   doesn't. The test for what stays substance is the no-oracle test.

2. **Four rules for the cursor** (four views of the same territory: locating the
   no-oracle layer)
   - Phase: 3X — borrow freely in Explore, pay in Extract.
   - Asset: becoming vs doing knowledge — some understanding was never needed; not
     all friction is necessary.
   - Location: blast radius — pay where wrong answers are expensive, borrow in the
     disposable periphery.
   - Premise defense (Chat's objection): debugging, incidents, and reading also
     calibrate; implementation was the only *default-on* refresh. The others require
     intention — which is precisely what the cursor now governs.

3. **The recursion** (what the rules reveal — comes AFTER the rules, not before)
   Every rule consumes judgement: knowing which X you're in is a judgement;
   classifying becoming vs doing is a judgement; estimating blast radius runs on the
   mental model. The cursor's position is set by the very asset the cursor decides
   whether to maintain. Consequence: the cursor cannot be automated — no rule, no
   product, no meter can set it for you, because reading the rules requires the model.
   Every incentive (deadlines, the exhilaration of vibe coding, the unpleasantness of
   friction) pushes toward borrow.

4. **Dependency inversion** (the practice that lives with the recursion)
   Ask the teacher for structure — exploration, options, the mechanical surfacing —
   and do the substance yourself: the words, the code. You get exploration from the
   teacher and calibration from doing. The teacher is dangerous as a substitute and
   valuable as a companion. Completes the Adler thread from part 1. Purpose is better
   understanding, not speed. Caveat (one sentence): exploration with the teacher still
   requires bringing your own candidates, or the surfaced options quietly become the
   option space.

5. **Close**
   One-sentence gesture at economics as the chain to essay 3: all of this assumes
   tokens are cheap; what happens when they aren't is a later essay.

## Cut from this essay (moved to 03-token-economy)
- Human tokens appreciate with use / treasury vs pure outflow
- Inferior model = mediocre engineer (rework, misdirection)
- Amortization limit: comprehension has acquisition cost and decay rate; past a
  certain system-change rate no strategy works
- LLM memory as institutional memory (curated) — parked; may not need publishing

## Open questions
- Does "always on time" survive the pay-mode self-test? (When deliberately paying
  comprehension, does schedule pressure return?)

## Open question (2026-07-11): the recursion has levels, and they get worse

L0 judgement about the code — blast radius: the module; oracle: fast.
L1 judgement about when to borrow — blast radius: the mental model; oracle: slow, self-masking.
L2 judgement about which frictions to keep — blast radius: what kind of engineer you are;
oracle: a decade, arriving as obsolescence.

Blast radius grows and oracle quality degrades together. The decisions that matter most
are the ones you can least check.

Candidate principle: at high recursion levels, favour optionality over commitment.
Beck's answer to architectural uncertainty (cheap to change, rather than predicted
correctly), applied to skill acquisition. Calibrate on what stays load-bearing across
many futures rather than betting a decade on one faculty.

The sushi problem: do not spend ten years becoming a master if the seas empty in three.
This is the non-moral criterion — fit, not virtue. Nobody is lazy; someone is wrong, and
finds out too late.

Open, and needs testing before it goes in prose: is the L2 blast radius really the
largest? Careers may be more recoverable than architectures. If so the monotonic claim
breaks and only the oracle-degradation half survives.
