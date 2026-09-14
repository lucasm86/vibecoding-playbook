# Architecture Principles — Core Doctrine

> **This file is normative.** It is the synthesis of the six `references/`
> extractions after reading them together and resolving their tensions with
> explicit context. Where a reference disagrees with doctrine, doctrine wins for
> *this* project; where doctrine is silent, fall back to the references.
>
> Each principle carries an `AP-xxx` id. Cite them in specs, ADRs, and agent
> reasoning. Traceability tags (e.g. `[01-P02, 04-P06]`) point back to the
> evidence.
>
> **How synthesis was done.** Converging ideas (supported independently by
> several books) became principles. Tensions (reuse vs. decoupling, upfront design
> vs. deferral, "anyone decides" vs. a bounded Executor) were resolved by naming
> the *context* that decides, not by picking the loudest book. Ideas that are
> correct only sometimes are stated with their `Exceptions`.

---

## Reading order

- **AP-001 … AP-003** — disposition (simplicity, trade-offs, proportionality).
- **AP-004 … AP-009** — structure (domain, boundaries, coupling, distribution).
- **AP-010 … AP-014** — decisions (reasoning, ADRs, the Architect/Executor line).
- **AP-015 … AP-019** — change & verification (evolvability, fitness functions,
  measurement).
- **AP-020 … AP-023** — coherence & flow (conceptual integrity, spec-first,
  consequences, Conway).

---

## AP-001 — Strive for the least-worst set of trade-offs, not "best practice"

### Rule
There is no universally best design. For any consequential decision, choose the
option whose trade-offs are least harmful *in this context*, and state explicitly
what it sacrifices.

### Rationale
Real systems are unique; "best" implies maximizing every competing concern at once,
which is impossible. Naming the sacrifice is what makes a decision honest and
reviewable. `[01-P01, 02-P02]`

### Architect behavior
Produce a short trade-off comparison (options × the few characteristics that matter
here) and a one-line bottom line in domain terms for any significant decision.

### Executor consequence
Never re-open a recorded trade-off. If the code contradicts the chosen option,
escalate (AP-013), don't substitute a "better" one.

### Verification
The *sacrificed* characteristic frequently becomes a fitness function (AP-017).

### Exceptions
Trivial, fully reversible choices — decide and move; no trade-off table.

---

## AP-002 — Everything is a trade-off; decide in context

### Rule
"It depends" is the honest starting point. Add the concrete domain and operational
context *before* concluding, so the decision is correct for the real situation, not
a generic one.

### Rationale
Generic advice flips when context (rate of change, security, team boundaries,
scale) is added. Finding the right narrow context lets you consider fewer options —
this is how simple design is actually achieved. `[01-P07, 02-P04, 03 (heuristics)]`

### Architect behavior
Model 2–3 likely scenarios against each option; capture the context that makes the
answer correct.

### Executor consequence
The Executor inherits a *narrowed* decision space, which is why specs are concrete.
It does not re-generalize a context-specific decision.

### Verification
Indirect — recurring surprises signal the context was wrong.

### Exceptions
Don't over-model trivial or reversible choices; "it depends" is not a license to
avoid deciding (see AP-010, AP-014).

---

## AP-003 — Match solution sophistication to problem complexity ("how little design can you afford?")

### Rule
Use the simplest structure, pattern, and tooling that fits. Advanced patterns
(distribution, event sourcing, CQRS, heavy governance) are *costs* that require a
complexity justification.

### Rationale
Scale dictates architecture: a dog house needs materials, a skyscraper needs
design. Over-engineering is as harmful as under-engineering, and elaborate patterns
applied everywhere are "wasteful and ineffective." `[03-P07, 04-P05, 06-P05]`

### Architect behavior
Default to the simplest viable option; require an explicit reason (usually
core-subdomain complexity or a measured characteristic) to escalate. Right-size
upfront design to scale and risk.

### Executor consequence
Do not introduce patterns, abstractions, infrastructure, or dependencies the spec
did not call for.

### Verification
Indirect — complexity/coupling metrics trending up without justification is a smell.

### Exceptions
Irreversible or safety-critical decisions genuinely warrant more upfront rigor.

---

## AP-004 — Classify by strategic value before designing

### Rule
Classify each part of the system as **core** (competitive advantage — build,
invest), **supporting** (necessary but simple — build cheaply), or **generic**
(commodity — buy/adopt, don't build). Design investment is proportional to the
classification.

### Rationale
Strategic value, not technical difficulty, decides where to spend. Building a
generic subdomain or gold-plating a supporting one wastes the effort that core
subdomains need. `[03-P01, 03-P07]`

### Architect behavior
Start domain analysis with subdomain classification; record it and its rationale;
revisit it as the business evolves (subdomains change type).

### Executor consequence
Do not gold-plate supporting/generic areas; treat core-subdomain specs as the
demanding ones. The spec states the subdomain type.

### Verification
Indirect — a "core" area that is trivial CRUD (or vice versa) means the
classification is wrong.

### Exceptions
Tiny single-purpose tools with one obvious concern.

---

## AP-005 — Model the domain and its boundaries before the infrastructure

### Rule
Design from the business domain outward. Establish the ubiquitous language and
context boundaries first; choose technology and infrastructure to serve them, never
the reverse.

### Rationale
Software should be driven by the domain, not by technology fashion; a vendor or
framework placed at the center dictates all future decisions (Vendor King).
`[03-P02, 04-P06, 02-P05]`

### Architect behavior
Define contexts and their ubiquitous language; treat every external tool as an
integration point behind an anticorruption layer.

### Executor consequence
Use the domain's own vocabulary in code and tests; integrate external tools through
the boundary the spec defines, not by importing their models directly.

### Verification
Partial — "context A must not import context B's / a vendor's internal model" can be
a fitness function.

### Exceptions
Purely technical/infrastructural components with no business language.

---

## AP-006 — Understand the whole before decomposing it

### Rule
Describe the system as a whole — its purpose and the relationships/behaviors that
*emerge* from the parts — before breaking it into components. Decomposition must
preserve required emergent behavior.

### Rationale
Analysis (splitting) produces knowledge; synthesis (seeing the whole) produces
understanding. A complex system's important behavior lives in the relationships, not
the parts. `[02-P01, 02-P03]`

### Architect behavior
Model relationships and information flow first; treat the component list as an
output of understanding, not the starting point.

### Executor consequence
Flag when a local change produces a surprising system-wide effect rather than
absorbing it silently.

### Verification
Weak — emergent behavior often shows only in integration/production; watch via
feedback loops (AP-016/AP-018).

### Exceptions
Genuinely simple, isolated components.

---

## AP-007 — Modularity before distribution; distribution is a trade-off, not a goal

### Rule
Achieve clean modular boundaries first. Distribute (services, microservices) only
when a concrete driver justifies it and the integrators don't veto it. Never
distribute "because microservices."

### Rationale
Most distributed-system pain is granularity, not modularity. Distribution buys
independent scaling/deployment/fault-isolation at the cost of coupling, complexity,
and consistency. Microservices also require ecosystem support. `[01-P03, 01-P04,
04-P01]`

### Architect behavior
Justify each service boundary against explicit disintegrators (scope/cohesion,
volatility, scalability, fault tolerance, security, extensibility) and integrators
(transactions, data relationships, workflow cost). A shared database or mandatory
orchestrator means the "services" are really one unit — say so.

### Executor consequence
Do not split or merge services, or introduce a shared datastore between separate
units, on your own — that's an architectural decision (AP-012).

### Verification
Partial — "no service reads another's database"; no component cycles.

### Exceptions
Systems deliberately kept as a single deployable (a monolith is one legitimate
quantum).

---

## AP-008 — Manage coupling deliberately

### Rule
Treat coupling ("if X changes, might Y have to change?") as a first-class, managed
quantity. Prefer decoupled designs; when reuse or a shared component becomes a
bottleneck to change, break the coupling (fork, duplicate, abstract, or wrap).

### Rationale
Inappropriate coupling is the primary enemy of evolvability and the road to the big
ball of mud. Sometimes duplication is cheaper than coordination. `[01-P02, 04-P06,
06-P05, 05-P05]`

### Architect behavior
Map static (deploy-together) vs. dynamic (runtime-call) coupling separately;
decide reuse vs. duplication by comparing cost of coordination against cost of
duplication; insulate external dependencies behind ACLs.

### Executor consequence
Do not create new tight couplings or cycles; when changing a shared contract, check
who else is coupled first.

### Verification
Strong — coupling, cycle, and dependency-direction fitness functions.

### Exceptions
Early on, a small shared kernel (limited to contracts) can be cheaper than
duplication when coordination cost < duplication cost.

---

## AP-009 — Boundaries follow the model; start coarse, split on evidence

### Rule
Size a boundary to the model it encompasses, not to a target service size. Start
with wider boundaries (especially around volatile core subdomains) and decompose as
domain knowledge grows.

### Rationale
Refactoring logical boundaries is far cheaper than refactoring physical ones, so
being wrong about a wide boundary is safer. A change that repeatedly spans many
boundaries signals they're drawn wrong. `[03-P03, 01-P04, 05-P05]`

### Architect behavior
Resist premature micro-granularity; record which boundaries are provisional and
expected to split.

### Executor consequence
Never redraw a boundary on your own; surface "this change keeps touching many
areas" as a boundary smell.

### Verification
Indirect — blast-radius / cross-boundary-change frequency.

### Exceptions
Well-understood, stable domains where the right small boundaries are already known.

---

## AP-010 — Decisions are propositions with reasons, not opinions

### Rule
Every significant recommendation must be a proposition: **claim + justifying reasons
+ the perspectives/alternatives considered**. "I prefer X" is not acceptable.

### Rationale
Decentralized, trustworthy decision-making depends on reasons, not authority or
taste. This is the intellectual content an ADR captures. `[02-P02, 05-P01]`

### Architect behavior
State reasons and rejected alternatives for every architectural decision; this is
the standard an ADR must meet.

### Executor consequence
When escalating, give reasons ("this fails because…"), not just "this feels wrong."

### Verification
No — governs how decisions are made, not an output metric.

### Exceptions
Trivial, reversible choices don't need a written justification.

---

## AP-011 — Record significant decisions as immutable ADRs so they survive context loss

### Rule
Capture every architecturally-significant decision in an ADR (context, decision,
alternatives, trade-offs, consequences, verification). ADRs are immutable — to
change a decision, write a new ADR that supersedes the old one.

### Rationale
Decisions that live only in someone's head (or a lost chat) don't survive. The
decision *history*, including what's no longer true, records the priorities in force
at the time. This is what lets a cheap Executor — or a future session — act without
re-deriving everything. `[01 (ADRs), 04-P07, 05-P03]`

### Architect behavior
Write the ADR when the decision is taken; keep it reader-oriented and ~1–2 pages;
link supersessions.

### Executor consequence
Read relevant ADRs as binding constraints; never edit them; if reality contradicts
one, escalate so the Architect can supersede it.

### Verification
Weak — ADR presence/immutability checkable in review.

### Exceptions
Ordinary implementation choices (see AP-012) don't need ADRs.

---

## AP-012 — Define the architectural decision boundary (the five-criteria test)

### Rule
A decision is **architectural** — and belongs to the Architect, with an ADR — if it
affects **structure, non-functional characteristics, dependencies, interfaces, or
construction techniques**. Everything else is an ordinary implementation decision
the Executor owns.

### Rationale
This is the single most important guardrail of the two-agent workflow: it keeps
expensive reasoning with the Architect and lets the Executor move fast within safe
bounds. `[05-P02, 05-P06]`

### Architect behavior
Apply the test to triage; pre-authorize the Executor's implementation decision space
in specs so it isn't blocked.

### Executor consequence
Before acting, self-check against the five criteria. Touching any of them ⇒ stop and
escalate (AP-013). Otherwise proceed without asking permission for every step.

### Verification
Partial — e.g. "no new external dependency without an ADR" as a fitness function.

### Exceptions
None — this is the core triage rule. Borderline cases resolve toward escalation.

---

## AP-013 — Seek advice (input) before deciding, not permission

### Rule
Before taking a decision, gather input from those it affects and those with relevant
expertise — for us: the human user, this doctrine, the references, and the existing
code and tests. Then one accountable role decides and records it.

### Rationale
Advice (not permission) removes bottlenecks while keeping accountability. It also
means decisions are informed by real constraints, not made in a vacuum. Input must
be *real* — never fabricate stakeholders or invent advice. `[05-P01, 02-P02]`

### Architect behavior
Actively solicit the human's intent and constraints on significant decisions;
consult code/tests for ground truth; record what shaped the decision.

### Executor consequence
Within its bounded space, proceed unblocked; for architecturally-significant matters,
"seeking advice" means escalating to the Architect.

### Verification
No.

### Exceptions
Self-contained trivial choices.

---

## AP-014 — Prefer reversible decisions; defer to the last responsible moment

### Rule
Favor decisions that are reversible and that create fast feedback. Defer hard-to-
reverse decisions to the **last responsible moment** — the point past which
deferring costs you options — and attach an explicit trigger for re-deciding.

### Rationale
Under uncertainty you cannot know the right answer up front; reversible + fast-
feedback decisions let you learn. But it's the *last responsible* moment: deferral
has a deadline, not "forever." `[02-P06, 04-P05]`

### Architect behavior
Mark provisional decisions as provisional; record reversibility (one-way vs. two-way
door) in the ADR; install threshold fitness functions as future decision points.

### Executor consequence
Ship in small, reversible increments; report what implementation reveals so deferred
decisions can be made with real information.

### Verification
A threshold fitness function can *be* the deferred decision point.

### Exceptions
Irreversible/safety-critical decisions that must be made carefully up front.

---

## AP-015 — Architecture must support guided, incremental change (evolvability)

### Rule
Evolvability is an explicit design goal. Prefer designs that permit small, safe,
independently deliverable changes with a small blast radius over designs that are
"correct" but rigid.

### Rationale
The ecosystem is a moving target; no long-horizon plan survives. Preventing bit rot
means making change cheap and continuously governed — *guided* change, not
unplanned drift. `[04-P01, 02-P06, 06-P04]`

### Architect behavior
Favor modularity, decoupling, and continuous delivery; treat "how easily can this
evolve?" as a first-class characteristic.

### Executor consequence
Work in small increments behind tests; each change independently verifiable and
deployable; keep the four key metrics (throughput + stability) balanced.

### Verification
Yes — cycle time, deployment frequency, change failure rate, time to restore.

### Exceptions
True throwaway prototypes.

---

## AP-016 — Characteristics must be objective and measurable, or they aren't requirements

### Rule
Any characteristic the system commits to (performance, scalability, security,
maintainability…) must be expressed objectively and measurably. "Fast" is not a
requirement; "p99 < 200 ms at 500 rps" is. Decompose composite characteristics
(reliability, agility) until each part is measurable.

### Rationale
Unmeasurable characteristics can't be verified, governed, or agreed on; vagueness
usually hides a composite. Testable CFRs are what let independent work stay aligned.
`[01-P08, 04-P02, 05-P04, 06-P02]`

### Architect behavior
Turn each committed characteristic into a measurable CFR with a threshold; state the
goal it serves (GQM).

### Executor consequence
Treat these thresholds as acceptance criteria; a breach fails the work.

### Verification
Central — these become fitness functions (AP-017).

### Exceptions
Exploratory work where you're still discovering the right metric.

---

## AP-017 — Govern with fitness functions — a checklist, not a stick

### Rule
Encode the structural and characteristic rules that matter into objective,
automated checks that run in the build/pipeline and fail it on violation. Keep the
suite lean and collaboratively owned.

### Rationale
Principles stated only in a wiki get skipped under pressure. Fitness functions are
an executable checklist that stops capable actors from accidentally skipping
important-but-not-urgent rules — not a tool to torture implementers with an
ivory-tower web of gates. `[04-P02, 04-P03, 04-P07, 01-P08, 06-P02]`

### Architect behavior
For each committed characteristic/structural rule, define a fitness function; choose
its category (atomic/holistic, triggered/continual/temporal, automated/manual)
deliberately; document it in the governing ADR.

### Executor consequence
A red fitness function blocks the change exactly like a failing test; fix it (or
escalate if intent is unclear), never bypass it.

### Verification
This *is* the verification mechanism.

### Exceptions
Don't build checks that add burden without corresponding value; scale the suite to
the system (this playbook itself is Markdown — it needs almost none).

---

## AP-018 — Measure with purpose; beware vanity metrics and Goodhart's law

### Rule
Every metric must trace to a goal and a question (Goal-Question-Metric). Watch
trends, not just snapshots. Never optimize a metric in a way that harms the goal it
proxies.

### Rationale
The easy-to-measure is often not the thing that matters. A metric made into a target
gets gamed (Goodhart). Trends catch structural erosion early, while it's cheap to
fix. `[06-P01, 06-P03, 06-P06]`

### Architect behavior
Define metrics top-down from goals; catch rising coupling/complexity/cycle time as
early warnings; keep each metric tied to its purpose.

### Executor consequence
Understand *why* a metric exists before optimizing for it; report adverse trends
rather than absorbing them.

### Verification
The metrics themselves, read as trends.

### Exceptions
Obvious standard operational metrics where the goal is self-evident.

---

## AP-019 — Optimize the whole; avoid local optimization that harms the system

### Rule
Prefer decisions that improve the system as a whole over ones that optimize a part
at the whole's expense. Beware counterintuitive effects where the "obvious" local
fix worsens the overall behavior.

### Rationale
Systems behave nonlinearly; a locally optimal change (a clever cache, a hoarded
metric, a team's convenience) can degrade a system-wide characteristic. Balance —
across the four key metrics, across characteristics, across teams — beats local
maxima. `[02-P01, 02-P04, 06-P04, 01 (holistic)]`

### Architect behavior
Use holistic fitness functions for critical interactions; judge changes by
system-level outcome (POSIWID — what the system actually does), not local intent.

### Executor consequence
Raise it when a requested local change looks like it will harm a system-wide
characteristic.

### Verification
Holistic fitness functions; system-level (external/operational) measurements.

### Exceptions
Genuinely isolated changes with no system-wide interaction.

---

## AP-020 — Protect conceptual integrity

### Rule
Prefer a small set of coherent, interdependent concepts applied consistently over
many locally-clever but inconsistent ones. New concepts must fit the existing set or
explicitly replace part of it. Coherence beats completeness.

### Rationale
A system's understandability and evolvability come from conceptual integrity;
fragmentation by many unrelated good ideas is worse than a few integrated ones. At
the code level this *is* pattern consistency. `[02-P03, 03-P02]`

### Architect behavior
Own the conceptual model and vocabulary; reject additions that fragment it even if
each is individually reasonable; don't freeze it against legitimate evolution.

### Executor consequence
Follow existing patterns and the ubiquitous language precisely; do not invent new
idioms or synonyms.

### Verification
Partial — linters/pattern checks; glossary consistency.

### Exceptions
Deliberate, recorded introduction of a new cross-cutting concept (an ADR).

---

## AP-021 — Specify significant behavior before implementing it

### Rule
Architecturally-significant behavior and its acceptance criteria are written down —
in a spec with objective, verifiable criteria — before implementation begins.

### Rationale
The whole point of the two-agent split is that the Architect removes ambiguity so
the Executor implements against a clear, testable target. Specs carry rationale, not
just directives, so reasoning survives context loss. `[05-P04, 06-P03, 02-P02]`

### Architect behavior
Produce feature specs with objective acceptance criteria and verification before
handing work to the Executor; write them in the ubiquitous language.

### Executor consequence
Implement against the spec's acceptance criteria; if the spec is ambiguous or wrong,
escalate rather than guessing.

### Verification
The spec's acceptance criteria and fitness functions.

### Exceptions
Exploratory spikes explicitly framed as throwaway learning.

---

## AP-022 — Document consequences and what future work must respect

### Rule
Every significant decision records its consequences: what it commits future
implementations to, what it forecloses, and how continued compliance is checked.

### Rationale
A decision without its consequences can't guide the people (or agents) who come
after. Consequences are what the Executor and future sessions must respect.
`[01 (ADRs), 04-P07, 05-P03]`

### Architect behavior
Fill the ADR "Consequences" and "Verification" sections concretely; point at the
fitness function that guards the decision.

### Executor consequence
Respect recorded consequences as constraints; a change that violates one is an
escalation, not a workaround.

### Verification
The named fitness function / acceptance criteria.

### Exceptions
Decisions too trivial to warrant an ADR (AP-012).

---

## AP-023 — Treat team and communication structure as an architectural input (Conway's Law)

### Rule
Design the intended architecture and the team/ownership/communication structure
together. Where they conflict, expect the communication structure to win — so align
them deliberately, or deliberately cut against them and manage the cost.

### Rationale
"Organizations produce designs that copy their communication structures." Boundaries
you must coordinate across become the real architectural seams. `[02-P05, 05-P05]`

### Architect behavior
Name the human/ownership boundary behind each major seam; prefer boundaries that
minimize a decision's affected parties (which also speeds decisions).

### Executor consequence
Change cross-team/cross-context contracts carefully — they are communication
boundaries, not just interfaces.

### Verification
No.

### Exceptions
Solo or single-team projects where communication structure is trivial.

---

## Unresolved / context-dependent tensions (recorded, not hidden)

These are genuine tensions the references pull in different directions; doctrine
resolves them *by context*, not by decree:

1. **Reuse (DRY) vs. decoupling.** Share only when cost(coordination) <
   cost(duplication), and keep the shared surface to contracts; break reuse the
   moment it becomes a bottleneck to change. `AP-008` + `03-P04` + `04-P06`.
2. **Upfront rigor vs. deferral.** Reversibility and subdomain type decide: core /
   irreversible / safety-critical ⇒ more upfront; supporting / reversible ⇒ defer to
   the last responsible moment. `AP-003` + `AP-014` + `AP-004`.
3. **"Anyone can decide" vs. a bounded Executor.** The advice process's openness is
   constrained here by the five-criteria test: the Executor may take *implementation*
   decisions freely but must escalate *architectural* ones. `AP-012` + `AP-013`.
4. **Distribution's benefits vs. its costs.** Never a default; earn it with a
   disintegrator and survive the integrators. `AP-007`.

## Dangerous universalizations to actively resist

- Microservices / distribution as a goal rather than a trade-off. `[AP-007]`
- DDD tactical patterns (aggregates, event sourcing, CQRS) applied to simple CRUD.
  `[AP-003, AP-004]`
- Fitness-function overload / ivory-tower governance. `[AP-017]`
- Metric fixation and gaming (Goodhart). `[AP-018]`
- "Systems thinking / it depends" as an excuse for analysis paralysis or vague
  specs. `[AP-002, AP-010]`
- Simulating a literal social "advice forum" or fabricating stakeholders. `[AP-013]`
