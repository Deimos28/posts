# Setting the cursor

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

Human attention is capped and attempting to cover all the code regions risks diluting attention where it matters the most. Thanks to agents, we don't have to: we can set the comprehension cursor region by region, focusing our attention on the most critical modules and delegating execution of the rest.

![Attention allocated unevenly across modules: the critical few receive most of it](figures/cursor-allocation.svg)

I deliberately offer no metrics or units here, as they would instantly become [bad
targets](https://en.wikipedia.org/wiki/Goodhart%27s_law): this allocation is a judgement call, not something that can be
programmatically optimised. Allocating judgement itself requires judgement, and as
we move up the ladder — function, file, module, project, job, career —
evidence generally arrives later, noisier, and is harder to attribute. High on the ladder we only consent to being
 corrected slowly.

To summarise, setting the cursor is done region by region, by answering two questions:

- Q1, the epistemic clock: how long will we likely stay wrong, and at what cost? A proxy for this is the commit history (the lag between a change touching the region and the bug-fix, revert, or an incident that later referenced it).
- Q2, the survival clock: what is the cost of being late — of missing the time to market? We can estimate this using runway, committed dates, the [cost of delay](https://en.wikipedia.org/wiki/Cost_of_delay).

I deliberately offer no formula for converting these signals into a cursor position because whilst the clocks can be informed by evidence, their relative importance remains a judgement call.

Each clock pulls the cursor in one direction. When they pull in the same direction, cursor placement is easy. When they conflict, judgement is what resolves the conflict.

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

