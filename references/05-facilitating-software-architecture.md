# Reference — Facilitating Software Architecture

> Extraction document. Evidence, not doctrine.

## Bibliographic Reference

*Facilitating Software Architecture: Empowering Teams to Make Architectural
Decisions.* Andrew Harmel-Law. O'Reilly Media, 2024.

## Core Thesis

Traditional architecture concentrates decision power in a few "architects,"
producing either an **ivory tower** (teams wait in a queue for approval) or an
overloaded **hands-on** architect — both slow and both a bottleneck. The book's
answer is the **Architecture Advice Process**: *anyone* may take an architectural
decision, provided that, before deciding, they **seek advice from (a) everyone
meaningfully affected and (b) people with relevant expertise** — seeking *advice,
not permission*. One decision-taker, zero people who can veto. This is fast
(few people take it) and decentralized (anyone can initiate). It is held together
by a **social contract** of trust and made durable by **immutable ADRs**.
Alignment without central control is supplied by four mechanisms: a **technology
strategy** (directional), **testable cross-functional requirements (CFRs)**
(specific/non-directive), **collectively-sourced architectural principles**
(commitments), and a **technology radar** (recorded experience).

> **Translation note.** This is a book about *human organizations*. In our
> two-agent workflow we adopt its *decision discipline* — seek input before
> deciding, decide with one accountable taker, record immutably, align via
> principles/CFRs — not its literal social dynamics. See "Dangerous
> Misapplications."

## Principles Worth Adopting

### REF-05-P01 — Seek advice, not permission, before deciding

**Meaning**
The single rule: whoever needs a decision may take it, but *must first* seek advice
from the meaningfully-affected and the relevant experts, and genuinely listen.
No approval gate; no consensus required.

**Operational rule**
Before finalizing an architectural decision, gather and record input from (a) the
parties the decision affects and (b) the relevant expertise (here: the human, the
doctrine, the references, the existing code). Then one taker decides.

**Architect implication**
This *is* the Architect's decision discipline. The Architect is the accountable
decider; it must actively solicit the affected/expert perspectives (especially the
human's) rather than decide in a vacuum, and record that it did.

**Executor implication**
Direct and bounded: the Executor may take *implementation* decisions the same way
(inspect affected code, follow expertise encoded in specs/CODESTYLE) but must seek
advice — i.e., escalate to the Architect — before taking anything *architecturally
significant*.

**Spec implication**
Specs/ADRs record whose advice was sought and how it shaped the decision.

**ADR implication**
The advice sought and considered is part of the ADR.

**Verification implication**
No (governs the decision process, not an output metric).

**Use when**
Any decision with cross-cutting impact.

**Do not apply blindly when**
Trivial, self-contained choices — don't stage an advice ritual for a variable name.

---

### REF-05-P02 — Know what makes a decision *architectural*

**Meaning**
All architectural decisions are technical, but not all technical decisions are
architectural. A decision is architecturally significant if it affects
**structure, non-functional characteristics, dependencies, interfaces, or
construction techniques**. These are the decisions worth the advice process and an
ADR.

**Operational rule**
Apply the five-criteria test. If a decision touches any of the five, treat it as
architectural (Architect owns it, ADR required); otherwise it's an ordinary
implementation choice (Executor owns it).

**Architect implication**
Use the test to decide what deserves deep reasoning and a record.

**Executor implication**
Direct: this is the **escalation boundary**. A change that alters structure,
a non-functional characteristic, a dependency, an interface, or a construction
technique is *not* the Executor's to make alone.

**Spec implication**
Specs flag which decisions within them are architecturally significant.

**ADR implication**
The test decides whether an ADR is required.

**Verification implication**
Partial — "no new external dependency without an ADR" can be a fitness function.

**Use when**
Triaging any decision.

**Do not apply blindly when**
Never harmful; it's the core triage rule.

---

### REF-05-P03 — ADRs are immutable; supersede, never edit

**Meaning**
An ADR records one taken decision with its context and the advice behind it. Once
accepted it is **never changed** — later decisions **supersede** it. The decision
*history* (including what's no longer true) is itself valuable: it tells you the
priorities in force when a decision was made. ADRs are written for the reader,
target ~two pages, and carry a status lifecycle (Draft → Proposed → Accepted →
Superseded → Retired).

**Operational rule**
Never rewrite an accepted ADR. To change a decision, write a new ADR that
supersedes it and link the two.

**Architect implication**
Maintain an append-only decision log; the Architect's decisions survive context
loss precisely because they are recorded and immutable.

**Executor implication**
Direct: the Executor reads relevant ADRs as binding constraints and never edits
them; if reality contradicts an ADR, it escalates so the Architect can supersede.

**Spec implication**
Specs cite the ADRs that constrain them by id.

**ADR implication**
This is the ADR lifecycle rule itself.

**Verification implication**
Weak — ADR presence/immutability can be checked in review or CI.

**Use when**
Any significant decision.

**Do not apply blindly when**
Never — but keep ADRs lightweight; not every choice needs one (see P02).

---

### REF-05-P04 — Align without central control via CFRs, principles, strategy, radar

**Meaning**
Decentralized deciding needs *just enough* shared agreement so teams don't diverge.
Four complementary mechanisms provide it:
- **Testable CFRs** — specific, non-directive: *what* the system must achieve
  (e.g., "every action < 500 ms"), with time budgets allocated across components.
- **Architectural principles** — collectively sourced commitments: title +
  call-to-action + rationale + implications.
- **Technology strategy** — directional, non-specific: the *how/where we're going*.
- **Technology radar** — recorded collective experience (adopt/trial/assess/hold).

**Operational rule**
Encode the minimum-viable agreement as testable CFRs and shared principles; let
those (not a person) align independent decisions.

**Architect implication**
Owns/curates CFRs and principles; makes them *testable* and specific enough that
misalignment is a visible surprise.

**Executor implication**
Direct: CFRs are acceptance criteria; principles are constraints the Executor's
work must satisfy without being told each time.

**Spec implication**
Specs inherit CFRs as measurable acceptance criteria and reference principles.

**ADR implication**
Principles/CFRs are the backdrop every ADR is judged against.

**Verification implication**
Strong — CFRs are *testable* by design; they become fitness functions
(direct bridge to books 01/04).

**Use when**
Any multi-decision / multi-component effort.

**Do not apply blindly when**
Tiny single-component work where one spec suffices.

---

### REF-05-P05 — Sharper boundaries make decisions faster (the reinforcing dynamic)

**Meaning**
Because you must seek advice from everyone *affected*, teams are naturally pushed
to **reduce the number of affected parties** — by defining decisions more sharply
and decoupling. Good boundaries are rewarded with decision speed.

**Operational rule**
When a decision touches many parties, first narrow its scope / improve the boundary
so it touches fewer. Coupling shows up as a slow decision.

**Architect implication**
Treat "how many parties does this decision affect?" as a design smell detector;
decouple to localize decisions.

**Executor implication**
Moderate — a task that keeps forcing changes across many areas signals a boundary
problem to surface, not to push through.

**Spec implication**
Specs scoped to minimize cross-cutting impact.

**ADR implication**
A decision that affects an unexpectedly large blast radius is itself worth an ADR
(and maybe a boundary fix).

**Verification implication**
Indirect — coupling/blast-radius metrics.

**Use when**
Structuring decisions and boundaries.

**Do not apply blindly when**
Genuinely cross-cutting concerns (security, observability) that *should* involve
many parties.

---

### REF-05-P06 — Decouple permission from progress

**Meaning**
Much delivery drag is **permission coupling** — waiting for a decision or for
approval of one already effectively made. Removing the approval gate (advice, not
permission) removes the bottleneck while keeping accountability with the decider.

**Operational rule**
Don't insert approval gates where advice + a recorded decision suffice; keep the
accountable taker close to the need.

**Architect implication**
Design the process so the Architect is not a blocking queue for every choice —
delegate implementation decisions to the Executor with clear boundaries (P02).

**Executor implication**
Direct: within its boundary the Executor proceeds without asking permission for
every step; it escalates only architecturally-significant matters.

**Spec implication**
Specs pre-authorize the implementation decision space so the Executor isn't blocked.

**ADR implication**
ADRs remove future permission-seeking by settling the decision once.

**Verification implication**
Indirect — cycle time / wait time.

**Use when**
Designing the division of labour.

**Do not apply blindly when**
High-risk/irreversible actions that genuinely warrant a gate.

---

## Decision Heuristics

- **Advice, not permission:** seek input from affected + experts, then one taker
  decides.
- **Five-criteria test** for "is this architectural?" — structure, non-functional
  characteristics, dependencies, interfaces, construction techniques.
- **Immutable ADRs; supersede, don't edit.**
- **Make agreements testable** (CFRs) so misalignment is a visible surprise.
- **Minimize affected parties** by sharpening scope and decoupling — speed follows.
- **Permission coupling is drag** — remove approval gates that add no value.
- Principles = title + call-to-action + rationale + implications; source them
  broadly.

## Questions the Architect Should Ask

- Whose advice must I seek here — who is affected, and who has expertise?
- Is this decision architecturally significant by the five criteria, or is it the
  Executor's to make?
- Have I recorded the advice and the decision so it survives context loss?
- What is the smallest scope that makes this decision affect the fewest parties?
- Which CFRs / principles constrain this, and are they testable?
- Am I acting as a bottleneck (permission coupling) where advice would suffice?
- If this decision changes later, what will supersede it?

## Anti-Patterns

- **Ivory tower** — all decisions queued behind distant architects.
- **Overloaded hands-on architect** — the architect as a single point of decision
  for every team.
- **Permission coupling** — waiting for approval of already-made decisions.
- **Consensus/democracy for everything** — everyone entitled to every decision;
  nobody accountable; nothing decided.
- **Mutable/rewritten ADRs** — destroying decision history.
- **Vague, imposed principles** — principles handed down, untestable, ignored.
- **Untestable CFRs** — "must be fast" with no number.

## Dangerous Misapplications

- **Literal social process onto AI.** The advice process is a human trust system.
  An AI must not simulate a fake "forum," invent stakeholders, or claim it
  "consulted the team." What transfers is the *discipline*: gather real input
  (from the human user, doctrine, references, code), decide with one accountable
  taker, record immutably. Fabricating advice offerers is a serious failure.
- **"Anyone can decide" → the Executor redesigns architecture.** In our workflow
  the Executor's autonomy is *bounded by P02*. "Anyone can decide" does **not**
  license the cheap model to take architecturally-significant decisions; it must
  seek advice (escalate). This is the single most important guardrail from this
  book for our two-agent split.
- **Skipping ADRs because "we're moving fast."** The process depends on the record;
  no record = no decentralization, just chaos.
- **Consensus-seeking paralysis.** The book explicitly rejects requiring agreement;
  don't turn "seek advice" into "get everyone to agree."
- **Principles as bureaucracy.** If a principle doesn't help decide, it's noise.

## Useful Techniques

- **Architecture Advice Process** (one rule, two advice groups, one social
  contract).
- **ADRs** — immutable, reader-oriented, ~2 pages, status lifecycle, supersession.
- **Testable CFRs** with allocated budgets across components.
- **Collectively-sourced architectural principles** (title / call-to-action /
  rationale / implications).
- **Technology strategy** + **technology radar** (adopt / trial / assess / hold).
- **Advice forum** — a lightweight venue for offering advice on in-flight decisions.

## Candidate Rules for Our Doctrine

1. Decisions are made by seeking advice (from the human, doctrine, references,
   code), not permission; one accountable taker decides and records it.
2. The five-criteria test defines the Architect/Executor boundary: structure,
   non-functional characteristics, dependencies, interfaces, or construction
   techniques ⇒ architectural ⇒ Architect + ADR.
3. ADRs are immutable and reader-oriented; changes supersede, never edit.
4. Alignment is carried by testable CFRs and collectively-sourced principles, not
   by a human gate; CFRs become fitness functions.
5. Sharpen scope and decouple to shrink a decision's blast radius (speed follows).
6. Remove permission coupling: the Executor proceeds unblocked within its bounded
   decision space and escalates only architecturally-significant matters.

## Concepts We Explicitly Reject or Limit

- The organizational/leadership/power-transition material (Chs 7, 15–17) is for
  human orgs and is **out of scope** for agent doctrine. We keep the decision
  mechanics (advice discipline, ADRs, CFRs, principles), not the org-change
  program.

## Relationship to Other References

- **The Hard Parts (01)** & **Evolutionary (04)** — CFRs *are* the objective
  characteristics those books turn into fitness functions; ADRs are shared.
- **Systems Thinking (02)** — "advice with reasons" operationalizes systemic
  reasoning; Conway's Law underlies "who is affected."
- **DDD (03)** — "minimize affected parties / decouple" mirrors bounded contexts
  and context maps aligned to team structure.
- **Metrics (06)** — testable CFRs need the measurements metrics defines.

## Source

*Facilitating Software Architecture.* Andrew Harmel-Law. O'Reilly, 2024.
Referenced for analysis only; no source text reproduced.
