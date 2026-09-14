# Reference — Software Architecture: The Hard Parts

> Extraction document. Evidence, not doctrine. Principles are stated on this
> book's own terms; synthesis and reconciliation with other sources happens in
> `doctrine/`.

## Bibliographic Reference

*Software Architecture: The Hard Parts — Modern Trade-Off Analyses for
Distributed Architectures.* Neal Ford, Mark Richards, Pramod Sadalage, Zhamak
Dehghani. O'Reilly Media, 2021 (1st ed., ISBN 9781492086895).

## Core Thesis

For the genuinely hard problems in architecture there are **no best practices**,
because every real system is a "snowflake": a unique tangle of the
organization's constraints. The architect's actual job is therefore not to find
the best design but to find the **least-worst combination of trade-offs**, and to
document *why* that balance was chosen so the reasoning survives. The book teaches
a repeatable three-step method — **(1) find what is entangled, (2) analyze how
those parts are coupled, (3) assess the impact of change** — applied mostly to
data and communication in distributed systems.

## Principles Worth Adopting

### REF-01-P01 — Least-worst trade-offs, not best practices

**Meaning**
"Best" implies you maximized every competing concern at once; you can't. Every
consequential decision is a set of trade-offs weighed against a nearly equal set.

**Operational rule**
Never present a decision as objectively "best." Present it as the option whose
trade-offs are least harmful *in this context*, and name the concerns it sacrifices.

**Architect implication**
For any significant decision, produce a short trade-off table (options × the few
characteristics that actually matter here) and a one-line bottom line.

**Executor implication**
The Executor does not re-open trade-offs. If a spec's chosen option conflicts with
what the Executor sees in code, it escalates rather than substituting its own
"better" option.

**Spec implication**
Specs state the decision *and* the sacrificed characteristics, so downstream work
doesn't accidentally optimize the thing that was deliberately traded away.

**ADR implication**
Any decision with more than one viable option and lasting consequences becomes an
ADR whose "Consequences" section records what was given up.

**Verification implication**
Partially. The *sacrificed* characteristic often becomes a fitness function
("latency must stay under X even though we chose the flexible option").

**Use when**
Novel, high-consequence, hard-to-reverse decisions.

**Do not apply blindly when**
The choice is trivial or fully reversible — a trade-off table there is ceremony.

---

### REF-01-P02 — Coupling is "if X changes, might Y have to change?"

**Meaning**
The book deliberately uses the simplest definition of coupling: two artifacts are
coupled if a change to one may force a change to the other. It further separates
**static coupling** (how things are wired together to operate — OS, libraries,
databases, contracts) from **dynamic coupling** (how services call each other at
runtime in a workflow).

**Operational rule**
Before changing a boundary, ask concretely: "If I change X, what is forced to
change with it?" Distinguish wiring dependencies from runtime call dependencies.

**Architect implication**
Map static coupling (what must be deployed together) separately from dynamic
coupling (what talks at runtime). They have different remedies.

**Executor implication**
When editing shared contracts or shared libraries, the Executor must check who
else is statically coupled before changing a signature.

**Spec implication**
Feature specs list the artifact's dependencies split into "must deploy with" vs.
"calls at runtime."

**ADR implication**
Introducing a new static coupling point (a shared DB, a shared library) is ADR-worthy.

**Verification implication**
Yes — cyclic-dependency and layer-dependency fitness functions (see REF-01-P08).

**Use when**
Decomposition, contract design, choosing shared library vs. shared service.

**Do not apply blindly when**
A tiny app where everything is deliberately one deployable unit.

---

### REF-01-P03 — The architecture quantum bounds "independently deployable"

**Meaning**
An *architecture quantum* is an independently deployable artifact with high
functional cohesion, high static coupling internally, and synchronous dynamic
coupling. A shared database or a mandatory orchestrator pulls otherwise-separate
services back into a **single** quantum.

**Operational rule**
Before claiming two services are independent, check for hidden shared coupling
points (a shared DB, a shared broker required to boot, a mandatory orchestrator).
If one exists, they are not actually independent.

**Architect implication**
Draw quantum boundaries explicitly; treat a shared database as evidence that a
"microservice" split is an illusion.

**Executor implication**
Do not introduce a shared database or shared mutable store between components the
architecture treats as separate quanta.

**Spec implication**
SPECS.md names each quantum and its coupling points.

**ADR implication**
Any decision that changes a quantum boundary (merging or splitting deployables)
is an ADR.

**Verification implication**
Partial — "no service reads another service's database" can be a fitness function.

**Use when**
Distributed / service-based systems.

**Do not apply blindly when**
Deliberately monolithic systems — a monolith is legitimately one quantum.

---

### REF-01-P04 — Modularity ≠ granularity; balance disintegrators and integrators

**Meaning**
Modularity is *how you split* a system; granularity is *how big the pieces are*.
Most distributed-system pain is granularity, not modularity. The book gives six
**disintegrators** (reasons to split: distinct scope/cohesion, code volatility,
scalability/throughput, fault tolerance, security, extensibility) and
**integrators** (reasons to keep together: database transactions, data
dependencies/relationships, shared workflow/choreography cost).

**Operational rule**
Never split "because microservices." Require at least one concrete disintegrator,
then check the integrators would not veto it. Right size = equilibrium of both.

**Architect implication**
Justify every service boundary against the explicit disintegrator/integrator lists.

**Executor implication**
The Executor does not split or merge services on its own; granularity is an
architectural decision.

**Spec implication**
Each service spec records which disintegrator justified its existence.

**ADR implication**
Every split/merge decision is an ADR citing the driver.

**Verification implication**
Weak/indirect — statement counts and number of public entrypoints are rough size
metrics, not pass/fail gates.

**Use when**
Deciding service boundaries.

**Do not apply blindly when**
The system is small enough that a single service is obviously correct.

---

### REF-01-P05 — Semantic coupling can only be increased by implementation, never decreased

**Meaning**
The inherent coupling of a business workflow (its semantics) is fixed by the
domain. Architecture choices can add accidental coupling on top, but cannot make
the essential workflow logic disappear — it just moves (into an orchestrator, into
each service, into choreography).

**Operational rule**
When a design seems to "remove" workflow complexity, find where it went. If you
can't, you've hidden it, not removed it.

**Architect implication**
Locate essential workflow logic deliberately (orchestrator vs. distributed) and
own that placement as a decision.

**Executor implication**
Don't "simplify" by deleting coordination logic; it is load-bearing.

**Spec implication**
Feature specs make the coordination point explicit.

**ADR implication**
Orchestration vs. choreography for a workflow is an ADR.

**Verification implication**
No, generally.

**Use when**
Distributed workflows, sagas, multi-service transactions.

**Do not apply blindly when**
Single-service workflows where coordination is local anyway.

---

### REF-01-P06 — Prefer the bottom line over overwhelming evidence

**Meaning**
Stakeholders can't absorb every technical detail. Reduce a trade-off analysis to
a few decision-driving points, sometimes aggregates ("responsiveness vs.
guaranteed start").

**Operational rule**
End every analysis with a one- or two-line "which matters more here?" bottom line
in domain terms.

**Architect implication**
Translate technical trade-offs into business-legible choices before deciding.

**Executor implication**
None directly.

**Spec implication**
The spec records the bottom-line rationale, not the whole research trail.

**ADR implication**
The ADR "Decision" is the bottom line; detail lives in "Alternatives."

**Verification implication**
No.

**Use when**
Communicating or recording any non-trivial decision.

**Do not apply blindly when**
Never — but keep the discarded evidence retrievable for audit.

---

### REF-01-P07 — Keep decisions in context (avoid the "out-of-context" trap)

**Meaning**
A generic comparison (shared library vs. shared service) can point one way until
situation-specific context (rate of change, security, team boundaries) flips it.
Finding the correct narrow context lets you consider *fewer* options — this is how
"simple design" is actually achieved.

**Operational rule**
Add the concrete domain/operational context *before* concluding; model 2–3 likely
scenarios against each option.

**Architect implication**
Do iterative "what-if" scenario modeling rather than trusting generic advice.

**Executor implication**
None directly, but the Executor benefits: fewer live options = clearer spec.

**Spec implication**
Specs record the context that narrowed the decision.

**ADR implication**
The ADR "Context" section is what makes the decision correct or wrong later.

**Verification implication**
No.

**Use when**
Any decision where generic advice and local reality might diverge.

**Do not apply blindly when**
Never harmful; just don't over-model trivial choices.

---

### REF-01-P08 — Govern architecture with fitness functions

**Meaning**
A fitness function is any mechanism that gives an **objective** integrity
assessment of an architecture characteristic. Test = domain knowledge required;
fitness function = no domain knowledge required. They turn design principles into
an executable checklist that developers can't silently skip.

**Operational rule**
For every structural rule you care about (no cycles, layer access, no cross-service
DB reads), write an automated check that fails the build on violation.

**Architect implication**
Define the characteristics *objectively and measurably*; "high performance" is not
a fitness function, "p99 < 200ms at 500 rps" is. Beware composite characteristics
that hide non-measurable claims.

**Executor implication**
The Executor runs fitness functions as part of verify; a red fitness function
blocks commit exactly like a failing test.

**Spec implication**
Non-functional acceptance criteria are written as fitness functions where possible.

**ADR implication**
An ADR's "Verification" section names the fitness function that guards it.

**Verification implication**
This *is* the verification mechanism.

**Use when**
Any structural or characteristic rule you want to survive team pressure.

**Do not apply blindly when**
Don't build an ivory-tower cabal of interlocking checks that only frustrate teams;
guard the important-but-not-urgent, not everything.

---

### REF-01-P09 — Testing is the engineering rigor of software; qualitative→quantitative

**Meaning**
Software lacks structural engineering's predictive math, but it is "softer": you
can incrementally build and test. Objective tests move a trade-off analysis from
speculation to engineering. Prefer **qualitative** comparison (ratings across
representative examples) because two architectures rarely permit true quantitative
comparison — but make objective wherever you can.

**Operational rule**
When a trade-off is contested, build a small spike/test with an objective outcome
rather than argue from anecdote.

**Architect implication**
Model with rating matrices; validate contested assumptions with cheap experiments.

**Executor implication**
Verification is objective and test-driven, not opinion.

**Spec implication**
Acceptance criteria are objective and testable.

**ADR implication**
Prefer decisions backed by a spike over decisions backed by conviction.

**Verification implication**
Central.

**Use when**
Contested or high-risk decisions.

**Do not apply blindly when**
Cheap reversible choices — just decide and move.

---

## Decision Heuristics

- **Three-step method:** find entangled dimensions → analyze their coupling →
  assess impact of change. What's left after the hard parts are resolved is
  "just design."
- **Fix the fundamental dimension first** (e.g., sync vs. async), then iterate on
  the choices it forces or forbids.
- **Shared DB test:** if two services share a database with its own deployment
  cadence, they are one quantum — stop calling them independent.
- **Split test:** name the disintegrator; if you can't, don't split.
- **Merge test:** if a transaction or tight data relationship spans the split,
  an integrator may veto it.
- **Sync vs. async:** async buys responsiveness/fault-tolerance, costs guarantees
  and error-handling simplicity.
- **Contract breadth:** one broad shared contract for many consumers = stamp
  coupling; individual contracts decouple consumers but cost extensibility.

## Questions the Architect Should Ask

- If X changes, what is *forced* to change with it (statically? dynamically?)
- What is the single most important characteristic for *this* decision, in domain
  terms?
- What am I trading *away* by choosing this option?
- Where did the workflow's essential coordination logic go?
- Is this comparison MECE — mutually exclusive and collectively exhaustive — or am
  I comparing a message queue to an entire ESB?
- Can I state the bottom line in one sentence a non-technical sponsor understands?
- Which of my claimed characteristics are objectively measurable, and which are
  vague composites hiding an unmeasurable wish?

## Anti-Patterns

- **Big Ball of Mud / cyclic component dependencies** — components mutually
  referencing so nothing is reusable in isolation.
- **Stamp coupling for workflow management** — forcing many consumers onto one
  overly broad contract, creating accidental coupling.
- **Shared-topic broadcast where consumers need different contracts / security /
  scaling** — couples consumers operationally.
- **Splitting services with no disintegrator** ("microservices because
  microservices").
- **Ivory-tower governance** — a frustrating web of fitness functions detached
  from real risk.

## Dangerous Misapplications

- Treating **microservices / distribution as the goal**. The book is emphatically
  about trade-offs; an AI that reads it as "always distribute" has inverted it.
- Turning "least-worst trade-off" into **decision paralysis** — endless matrices
  for trivial, reversible choices.
- Reading fitness functions as a mandate to **gate everything**, choking delivery.
- Using **statement counts / entrypoint counts as hard granularity gates** — the
  book calls them rough, subjective aids, not thresholds.
- Assuming the book's **sync/async, saga, contract patterns are prescriptions**;
  they are a starting menu for *your own* trade-off analysis, not answers.

## Useful Techniques

- **Trade-off ratings matrix**: patterns/options as rows, the few relevant
  characteristics as columns; compare only at the end.
- **MECE lists** to keep comparisons honest.
- **Scenario / "what-if" modeling** on 2–3 likely domain cases per option.
- **Static coupling diagram** per service (OS/container deps, transitive deps,
  persistence, bootstrap integration points, messaging infra).
- **Fitness functions**: cycle checks (JDepend/ArchUnit/NetArchTest), layer-access
  rules, security/zero-day version checks in the pipeline.
- **ADRs** with Context / Decision / Consequences.

## Candidate Rules for Our Doctrine

*(Candidates only — promote to `doctrine/` after cross-book synthesis.)*

1. No decision is recorded as "best"; every significant decision names what it
   trades away.
2. Every service/component boundary must cite an explicit driver (disintegrator)
   and survive the integrators.
3. A shared database or mandatory orchestrator collapses "independent" services
   into one unit — the Architect must say so.
4. Structural rules the Architect cares about become fitness functions the
   Executor runs on every build.
5. Non-functional requirements must be stated objectively/measurably or they are
   not requirements.
6. Every non-trivial, hard-to-reverse decision ends in an ADR with a Consequences
   section.
7. The Executor never re-opens a recorded trade-off; it escalates instead.

## Concepts We Explicitly Reject or Limit

- The specific saga/pattern catalog (Epic, Phone Tag, Fairy Tale, …) is **not**
  imported as prescription — it's illustrative. We keep the *method*, not the menu.
- Statement/entrypoint counts are kept only as *soft signals*, never as CI gates.

## Relationship to Other References

- **Evolutionary Architectures (04)** — fitness functions originate there; deep
  synergy on governance and "architecture as continuously verified."
- **Metrics (06)** — supplies the objective measures that make characteristics
  testable; coupling/cohesion metrics operationalize P02/P04.
- **Domain-Driven Design (03)** — bounded contexts are the natural seams for
  quantum/granularity decisions; DDD supplies the "why here" for boundaries.
- **Facilitating Software Architecture (05)** — ADRs and decoupled decision-making
  are the social counterpart of this book's technical trade-off analysis.

## Source

*Software Architecture: The Hard Parts.* Ford, Richards, Sadalage, Dehghani.
O'Reilly, 2021. Referenced for analysis only; no source text reproduced.
