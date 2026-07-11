# Essay 3: The token economy (working title)

Fuel vs calories. Benefits from arriving after the framework is fully published; its
force comes from re-pricing concepts the reader already holds.

## 1. The triangle
Cost/quality/delay "pick two" held because all three vertices were observable and one
production process (humans typing) underlay them. Personal observation: "I'm now
always on time." Rejected framing: comprehension as a hidden fourth vertex (too clean;
comprehension was never tradeable before — it was a byproduct). Retained framing: the
triangle was a proxy for the economics of a single token source, and a second source
appeared. Corrections to keep: cost re-denominated (tokens + attention + an efficiency
game); delay compressed only where prompting is good; quality is conditional on
intent-capture (Clear).

## 2. Two currencies
Human attention and LLM tokens are both token-emitting processes with rate and
capacity. Differences: human tokens appreciate with use (spending on substance
refreshes the reservoir and improves future tokens) and mint understanding as a side
effect; LLM tokens are constant-quality and mint nothing. A currency whose expenditure
regenerates the treasury, versus one that is pure outflow. Non-fungible *because* LLMs
don't meaningfully learn; if that changes, the production asymmetry weakens first, the
judgment asymmetry (understanding located in the humans who must judge) last. Date the
claim explicitly. Externalized learning (CLAUDE.md files, memory, RAG) is
institutional memory: compounds only where a human curates, same failure mode.

## 3. Why "always on time"
Conceptual dead-ends were the dominant schedule cost and used to burn the scarce
currency; now they burn the abundant one. Also explains why speculative probes became
affordable at all.

## 4. Model quality = engineer quality
Tokens on an inferior model waste like salary on a mediocre engineer: not linearly but
through rework and misdirection — bad cheap tokens consume expensive human review
tokens downstream. The funnel restated in currency terms: everything in it protects
human tokens.

## 5. The pendulum
Compute constraint → cheap → re-constrained through scale, repeatedly. Constraint is
generative (90s game-engine ingenuity — VERIFY: Doom used trig lookup tables; the
famous approximation is Quake III's fast inverse square root). Efficiency knowledge
pays proportional to volume; agent swarms put ordinary engineers at scale. Oil-shock
analogy (1970s: efficiency reordered the auto industry) for the coming binding phase
(energy prices, subsidy end) — but pendulum, not permanent regime: skills minted in
the tight phase persist, like big-O did. Open empirical question: is inference cost
trending to scarcity or to zero — determines "when" vs "if" framing. Caveat: scarcity
restores discipline on the production side (sharp intent) but not the comprehension
side effect.

## 6. The inversion (candidate thesis)
Today comprehension competes with throughput; under binding token prices comprehension
IS throughput, because the dominant waste is misdirection and only understanding
prevents it. Understanding as compression: the two-token one-liner. Side effect:
cognitive debt becomes partially legible upward as a token bill — connects to the
concession/latency argument in 02c.

## 7. The coming efficiency layer
Compiler analogy: efficiency knowledge packages into a layer (context compression,
caching, routing, model selection) so the mass of users don't need it; the residual
moves up to judgment — the layer optimizes tokens on the path you chose, not the
choice of path. Disanalogy to keep honest: compilers optimize under a
provable-equivalence contract; context optimization has none — heuristic and silently
lossy. Video-compression comparison: codecs compress against a measured, stable
receiver model and degrade gracefully and visibly; context compression targets an
opaque, moving receiver, and text importance is heavy-tailed (one "not" outweighs a
thousand tokens), so it breaks discretely and invisibly. Blast radius is the right
compression criterion. One-line formal version: rate-distortion where the distortion
metric ("change in downstream behaviour") is uncomputable.

## 8. The blind-faith objection (shared with 02c; economic form lives here)
The fitness program assumes cheap tokens and buys understanding — but understanding is
a means. Alternative: generate-test-regenerate against an oracle, no comprehension
acquired. Legitimate wherever verification is cheap and complete. The boundary is
verification cost: blind faith is exactly as viable as the oracle is fast, so
comprehension spend concentrates where oracles are weak or slow. Resolves into essay
1's no-oracle argument via economics. Amortization caveat cutting both ways:
comprehension has acquisition cost and decay rate; above some system-change rate it
never pays back — then neither strategy works.

## Related but separate essay (parked)
The LLM-vs-car analogy as its own piece: fuel vs calories, fitness unbundled from
locomotion, gyms as deliberate substitutes, getting lost as becoming-knowledge.
Currently slated as the organizing frame of 02c instead; decide once 02c is drafted.

## Pre-draft verifications (also in shared/claims-to-verify.md)
- Inference-cost trajectory (scarcity or zero?)
- Prior art: "tokenomics for engineers" pieces — the differential is §6
- Doom/Quake trig detail
- Current state of prompt-compression research (LLMLingua and successors)
- "Always on time" pay-mode self-test
