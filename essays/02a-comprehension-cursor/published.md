# The comprehension cursor
*Agents don't start the decay: they simply stop the top-up.*

Published 2026-07-10: https://deimos28.substack.com/p/the-comprehension-cursor
Frozen copy of the published text (images live on Substack).

---

> *No method nor discipline can supersede the necessity of being forever on the alert.*
> — Henry David Thoreau, Walden

As I argued in a previous essay, LLMs can erode judgement as we need more of it to
fight the complexity LLMs introduce. To clarify our options, I will go back to one of
the many things I learned from my former control-theory expert colleagues: "you must
model something before you can control it".

For the purpose of this essay, I propose this simplified model for software
development:

[figure: manual loop — feature request → judgement → manual coding → code; friction →
ŷ → comprehension → rated mental model → judgement]

Peter Naur (yes, the same Peter Naur from the "Backus-Naur Form") said *"programming
properly should be regarded as an activity by which the programmers form or achieve a
certain kind of insight, a theory, of the matters at hand"*. This is why the previous
diagram says software development transforms feature requests into code using
judgement. That judgement comes from our confidence-rated mental model, continuously
adjusted as our view of the world ŷ surprises us.

Now what happens when we have access to a good agent?

[figure: same loop with "Code or prompt?" router and Agent path — no friction on the
agent path]

When we let the agent code, we no longer experience the friction and hence we no
longer get the feeling of unease when we don't understand the code, the sense that our
model does not match reality, which can be used to recalibrate our model. This comes
for free when coding manually. When relying on agents, we cannot feel our judgment
slipping because the alarm that is supposed to warn us our comprehension is decaying
is itself computed from comprehension. This is what Nataliya Kosmyna *et al.* called
cognitive debt: *"Cognitive debt defers mental effort in the short term but results in
long-term costs, such as diminished critical inquiry, increased vulnerability to
manipulation, decreased creativity"*.

In addition, we can not only delegate the implementation but also never be in a
situation where we don't understand: we can now borrow comprehension from the agent
the same way we borrow coding. This is the point Adler carries (from How to Read a
Book): a live teacher can answer you, so with a book you must do the work of
interrogation yourself — and that unaided struggle is where the understanding gets
built. The LLM ends that condition permanently: there is now always a present teacher,
so you are never again alone with the book. But an explanation received is not
understanding.

Comprehension was always a leaky reservoir: even without agents, knowledge that has
not been used in a while gets garbage-collected. Manual coding is a continuous top-up
of that reservoir, like a spaced repetition mechanism, refreshing the knowledge that
is used the most. The agents don't start the decay: they simply stop the top-up. We
now get to set a cursor on whether to pay for comprehension, or borrow and move
faster. How to do this is the subject of the next essay.
