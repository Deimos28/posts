# Essay 2, part 3: Restoring the friction

The techniques essay: how to keep the alarm alive when you borrow. Contains the
material Chat flagged as overloaded; the fixes below are agreed.

## Organizing frame (candidate)
The vehicle analogy. Cars unbundled fitness from locomotion the way agents unbundled
comprehension from production; fitness now requires deliberate exercise. Each
technique is introduced as "the deliberate substitute for what the old workflow gave
you free" — one repeated sentence-shape instead of nine coinages. Keep the register
mechanical (fuel, calories, fitness, gyms); no scenery wistfulness. The cursor in this
frame: nobody walks everywhere or drives everywhere; walk the neighbourhoods you want
to know (blast radius).

## Renames (per Chat's feedback: techniques stronger than names)
- Keep: predict-before-reveal; Small, Clear, Early
- Inquisition → scheduled interrogation
- Flexer Army → speculative-change probes
- Re-injection → replaying known bugs through the funnel (the canary: distinguishes
  "no debt found" from "debt-finding is broken")
- Defect/Stressor Army → plain fault injection and load injection, one nod to the
  Simian Army lineage

## Table
Shrink from eight rows to three failure surfaces — your model, the system, the
architecture — with the funnel and the canary as the meta-layer keeping detection
honest.

## Stability section
Three bullets, plain words: gain limiting (smaller reviewable steps), delay reduction
(feedback as early as possible), lead compensation (speculative-change probes).
Comprehension acts as a filter; filters introduce delay; the risk is the system
evolving faster than the ability to comprehend. Note the two-audience hazard: control
engineers read "gain limiting" literally; keep the terms but define each in one plain
clause.

## The blind-faith objection (include at full strength)
Generate-test-regenerate against an oracle, no comprehension acquired. Legitimate
wherever verification is cheap and complete; the comprehension spend is waste there.
Boundary: blind faith is exactly as viable as the oracle is fast. The fitness program
is for the layer where the test suite cannot tell you you are wrong (architecture,
security, slow rot). Concession to make plainly: half the techniques don't need
defending for daily coding, because daily coding is mostly on the verifiable side.

## The concession (closes the essay)
Engineering does not decide; the business holds allocation and observes only
behavioural signals (speed, defects, world response), all lagged. The engineer's one
lever is latency: convert the slow catastrophic debt signal into a fast legible one
the business can act on before foreclosure. This is why the instrumentation matters to
someone with a manager.

## Ending
The fuller Thoreau passage ("...the language which all things and events speak without
metaphor... Will you be a reader, a student merely, or a seer?") as the cold shower
after the fitness program: no method supersedes the alertness.

## Citations to place
- Thariq Shihipar's artifact collection (merge-gate quiz, blindspot pass, blast-radius
  interview): https://thariqs.github.io/html-effectiveness/unknowns/ — below the
  table, as evidence the practices are emerging convergently; the essay's differential
  is the mechanism.
- contral.ai — already cited in part 1; optional here as the anesthetic case
  (explanation-on-tap vs prediction-demanded).
