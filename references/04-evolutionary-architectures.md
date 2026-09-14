# Reference — Building Evolutionary Architectures (2nd Edition)

> Extraction document. Evidence, not doctrine.

## Bibliographic Reference

*Building Evolutionary Architectures: Automated Software Governance* (2nd ed.).
Neal Ford, Rebecca Parsons, Patrick Kua, Pramod Sadalage. O'Reilly Media, 2022
(ISBN 9781492097518).

## Core Thesis

The software ecosystem is a **dynamic equilibrium**: it constantly shifts, so no
five-year architecture plan survives. Rather than resist change, build
architecture that **supports guided, incremental change across multiple
dimensions**. "Guided" means you choose the architecture characteristics you care
about and protect them with **fitness functions** — objective, automatable checks
that catch degradation the way unit tests catch domain regressions. "Incremental"
means small changes, delivered continuously. "Multiple dimensions" means you
govern not just code but data, security, and operations. The goal is to prevent
**bit rot** by making architectural governance continuous, objective, and cheap —
a *checklist, not a stick*.

## Principles Worth Adopting

### REF-04-P01 — Architecture must support guided, incremental change

**Meaning**
Evolvability is itself a first-class goal. Prefer designs that permit small,
safe, continuous changes over designs that are "correct" but rigid. You cannot
predict the ecosystem; you can make the system cheap to change.

**Operational rule**
Favor modularity, decoupling, and continuous delivery so any change has a small
blast radius and fast feedback.

**Architect implication**
Treat "how easily can this evolve?" as an explicit characteristic when choosing
structure; avoid long-horizon big designs where knowledge is low.

**Executor implication**
Direct: work in small increments behind tests; each change should be independently
deployable/verifiable.

**Spec implication**
Specs favor incrementally shippable slices over big-bang features.

**ADR implication**
Decisions that reduce evolvability (a hard coupling, a vendor lock-in) must be
recorded with that cost.

**Verification implication**
Yes — cycle time and blast radius are measurable.

**Use when**
Any system expected to live and change.

**Do not apply blindly when**
True throwaway prototypes.

---

### REF-04-P02 — Protect architecture characteristics with fitness functions

**Meaning**
A fitness function is *any objective mechanism* (test, metric, monitor, manual
check) that assesses how well the architecture preserves a chosen characteristic.
It unifies previously separate concerns (code quality, DevOps metrics, security)
into one governance idea. Not all tests are fitness functions — only those
verifying architectural integrity.

**Operational rule**
For each architecture characteristic you commit to, define at least one fitness
function and run it in the pipeline.

**Architect implication**
Name the characteristics that matter, make each *objective/measurable*, and encode
it. "Evolvability" and "agility" are composites — decompose to measurable pieces.

**Executor implication**
Direct: a red fitness function blocks the change like a failing test; the Executor
fixes it, not bypasses it.

**Spec implication**
Non-functional acceptance criteria are expressed as fitness functions.

**ADR implication**
An ADR's governance/verification section names the fitness function that enforces
it.

**Verification implication**
This *is* the verification mechanism.

**Use when**
Any characteristic worth protecting over time.

**Do not apply blindly when**
Characteristics that don't actually matter for this system — don't manufacture
checks.

---

### REF-04-P03 — Know your fitness-function categories

**Meaning**
Fitness functions vary by **scope** (atomic = one aspect / holistic = interacting
aspects), **cadence** (triggered / continual / temporal), **result** (static
pass-fail / dynamic context-based), **invocation** (automated / manual), and
**proactivity** (intentional up-front / emergent). Holistic ones catch the nasty
cases where two individually-passing characteristics conflict (e.g., caching helps
scalability but breaks data-staleness security).

**Operational rule**
Choose the category deliberately: automate and trigger by default; use continual
(synthetic transactions, monitoring-driven development) for runtime characteristics;
use temporal (break-upon-upgrade, dependency reminders) for time-sensitive ones;
keep a few holistic checks for critical interactions.

**Architect implication**
Design a *portfolio* of fitness functions, not just unit-style checks.

**Executor implication**
Moderate — the Executor runs them and understands why a continual/holistic one
might fail even when unit tests pass.

**Spec implication**
Specs can indicate the category needed (e.g., "latency: continual/dynamic").

**ADR implication**
The category is part of documenting how a decision is governed.

**Verification implication**
Central.

**Use when**
Building the governance suite.

**Do not apply blindly when**
Small systems — a couple of atomic/triggered functions may be all that's warranted.

---

### REF-04-P04 — Govern multiple dimensions, not just code

**Meaning**
Architecture has orthogonal dimensions — **technical** (frameworks, libraries,
languages), **data** (schemas, migrations), **security**, **operational** — each
of which evolves and can break the system. Evolvability requires watching all the
important ones.

**Operational rule**
For each project, list the dimensions that matter and ensure each has protection
(e.g., schema migration discipline, security scans, ops monitors).

**Architect implication**
Explicitly enumerate the dimensions in scope; don't tunnel-vision on technical
architecture.

**Executor implication**
Moderate — data migrations and security are part of "done," not afterthoughts.

**Spec implication**
Specs address data/security/operational impact per feature.

**ADR implication**
A decision touching a new dimension (introducing a datastore, a new trust
boundary) is an ADR.

**Verification implication**
Yes — each dimension gets its own fitness functions.

**Use when**
Any non-trivial system.

**Do not apply blindly when**
Single-dimension tools (a pure library).

---

### REF-04-P05 — How little design can you afford? Scale dictates architecture

**Meaning**
Agile doesn't mean no architecture; it means no *useless* architecture. A dog
house needs materials; a 50-story building needs design. The question is how
little *unnecessary* design you can get away with while keeping the ability to
iterate.

**Operational rule**
Size the architectural investment to the system's scale and risk; defer decisions
to the **last responsible moment** — the point past which deferring costs you
options.

**Architect implication**
Right-size upfront design; build in decision points (fitness-function thresholds)
where you re-decide later with more information.

**Executor implication**
Direct: don't add speculative structure the spec didn't ask for.

**Spec implication**
Specs mark which decisions are deliberately deferred.

**ADR implication**
"Deferred until X" is a legitimate ADR outcome with a trigger.

**Verification implication**
Indirect — a threshold fitness function can *be* the deferred decision point.

**Use when**
Every project sizing decision.

**Do not apply blindly when**
Irreversible/safety-critical decisions that genuinely need heavy upfront rigor.

---

### REF-04-P06 — Manage coupling deliberately; break it when it blocks evolution

**Meaning**
Inappropriate coupling is the enemy of evolvability. Reuse becomes an antipattern
when the shared component becomes a bottleneck; the fix can be to **break the
coupling** (fork/duplicate) even at the cost of some duplication. Treat all vendor
/ external tools as *integration points* behind anticorruption layers, never as
the center of the architecture.

**Operational rule**
When a coupling point demonstrably impedes evolution, break it (fork, duplicate,
abstract, or wrap). Insulate external tools behind ACLs.

**Architect implication**
Continually re-evaluate whether shared assets still add value or have become drag;
be willing to trade DRY for decoupling.

**Executor implication**
Moderate — the Executor does not centralize the architecture on a vendor tool or
create new tight couplings; it uses the ACL the spec defines.

**Spec implication**
Integration specs specify the ACL/boundary for external dependencies.

**ADR implication**
Introducing or breaking a major coupling point is an ADR.

**Verification implication**
Yes — dependency/communication-governance fitness functions.

**Use when**
Reuse decisions, vendor integrations, distributed systems.

**Do not apply blindly when**
Early on, when a small shared kernel is cheaper than duplication (cost of
coordination < cost of duplication — cf. DDD).

---

### REF-04-P07 — Fitness functions are a checklist, not a stick; document them

**Meaning**
The point is not to torture developers with ever-more-interlocking checks (ivory
tower). Like pilots' and surgeons' checklists, fitness functions stop capable
people from *accidentally skipping* important-but-not-urgent steps under pressure.
Principles stated only in wikis get skipped; encoded ones don't.

**Operational rule**
Encode governance rules that would otherwise erode under schedule pressure; keep
the suite lean and collaboratively owned; document each in the relevant ADR.

**Architect implication**
Collaborate with implementers on fitness functions; justify each by real risk.

**Executor implication**
Direct: fitness functions are the executable checklist the Executor must pass;
breakage is fixed with the Architect if intent is unclear.

**Spec implication**
Specs reference the checklist items relevant to the feature.

**ADR implication**
ADRs include a "how this is governed" note pointing at the fitness function.

**Verification implication**
Central.

**Use when**
Always, but sparingly.

**Do not apply blindly when**
Never build checks that add burden without corresponding value.

---

## Decision Heuristics

- **Evolvability first:** prefer the design that's cheapest to change safely.
- **Objective or it isn't a characteristic:** decompose composites (agility,
  evolvability) into measurable parts.
- **Automate + trigger by default;** reserve continual/holistic/manual for where
  they're needed.
- **Last responsible moment:** defer decisions and install a threshold fitness
  function as the future decision point.
- **Cycle time is a fitness function** — rising cycle time is architectural decay.
- **Break coupling that blocks evolution;** trade DRY for decoupling when reuse
  becomes a bottleneck.
- **All external tools are integration points behind an ACL.**

## Questions the Architect Should Ask

- Which architecture characteristics must survive change here, and how do I measure
  each objectively?
- What's the smallest increment that delivers and can be verified?
- Which dimensions (technical/data/security/operational) can break this system?
- What's the last responsible moment for this decision, and what triggers the
  re-decision?
- Is this reuse still adding value, or has it become a bottleneck?
- Am I making a vendor the king of my architecture?
- Is this fitness function earning its overhead, or am I building an ivory tower?

## Anti-Patterns

- **Last 10% Trap / Low-Code-No-Code** — the tool does 90%, and the final 10%
  (the part that matters) is impossible.
- **Vendor King** — architecture built around a vendor product that dictates all
  future decisions.
- **Inappropriate Governance** — homogenizing on one stack/DB, forcing every
  project to bear the most-complex case's cost.
- **Resume-Driven Development** — choosing tech for the résumé, not the problem.
- **Leaky Abstractions** (pitfall) — all nontrivial abstractions leak.
- **Lack of Speed to Release** — slow cycle time throttles evolution.
- **Ivory-tower fitness functions** — governance detached from real value.

## Dangerous Misapplications

- **"Evolutionary" ≠ unplanned.** The book stresses *guided* change; an AI must not
  read this as "just refactor endlessly / no design." Guidance (fitness functions)
  is mandatory.
- **Fitness-function overload** — encoding every preference as a gate, choking
  delivery. Keep it lean.
- **Confusing all tests with fitness functions** — only architecture-verifying
  checks qualify.
- **Chasing microservices for "evolvability"** — the book shows microservices need
  ecosystem support and add coupling risks; distribution is a trade-off, not a
  goal.
- **Deferring decisions forever** under the banner of "last responsible moment" —
  it's the *last responsible* moment, and it has a trigger.

## Useful Techniques

- **Fitness functions** across the category matrix (atomic/holistic,
  triggered/continual/temporal, static/dynamic, automated/manual).
- **Deployment pipelines** as the place fitness functions run.
- **Synthetic transactions / monitoring-driven development** for continual runtime
  checks.
- **Break-upon-upgrade & temporal reminders** (Dependabot/Snyk) for dependency
  drift.
- **Cycle-time fitness function** as a process health metric.
- **Anticorruption layers** to insulate vendor/integration coupling.
- **Fitness-function-driven architecture** — define the checks first, like TDD.
- **ADRs with a governance section** documenting each fitness function.

## Candidate Rules for Our Doctrine

1. Evolvability is an explicit design goal: prefer small-blast-radius, reversible,
   incrementally deliverable changes.
2. Every committed architecture characteristic has an objective fitness function
   run in the pipeline; the Executor treats a red one like a failing test.
3. Governance spans dimensions (technical, data, security, operational), not just
   code.
4. Right-size upfront design to scale/risk; defer decisions to the last responsible
   moment with an explicit trigger.
5. Manage coupling actively; break reuse that becomes a bottleneck; wrap external
   tools in ACLs.
6. Keep the fitness-function suite lean and collaboratively owned — checklist, not
   stick — and document each in an ADR.

## Concepts We Explicitly Reject or Limit

- We keep fitness functions **lean by default**; the playbook's own repo uses only
  the governance it needs (it's Markdown, not a distributed system).
- Specific topology/data-migration mechanics are adopted *as needed per project*,
  not as universal mandates.

## Relationship to Other References

- **The Hard Parts (01)** — same authors; fitness functions and objective
  characteristics are shared machinery; this book is the governance engine behind
  Hard Parts' trade-offs.
- **Metrics (06)** — supplies the concrete measurements fitness functions assert
  on (coupling, cycle time, complexity).
- **Systems Thinking (02)** — incremental change + feedback loops + acting under
  uncertainty are the same disposition.
- **DDD (03)** — subdomain evolution (REF-03-P06) is the domain-level case of
  guided change; ACLs appear in both.
- **Facilitating (05)** — decentralized governance via ADRs + fitness functions is
  how the advice process scales.

## Source

*Building Evolutionary Architectures*, 2nd ed. Ford, Parsons, Kua, Sadalage.
O'Reilly, 2022. Referenced for analysis only; no source text reproduced.
