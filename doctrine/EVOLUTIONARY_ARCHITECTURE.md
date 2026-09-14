# Evolutionary Architecture — Supporting Doctrine

> How the system stays changeable and governed over time. Sources:
> [`04`](../references/04-evolutionary-architectures.md),
> [`02`](../references/02-systems-thinking.md),
> [`06`](../references/06-software-architecture-metrics.md).
> Core anchors: **AP-015, AP-014, AP-016, AP-017, AP-008**.

## The definition we adopt

Architecture should support **guided, incremental change across multiple
dimensions** (AP-015).

- **Guided** — change is protected by fitness functions, not left to drift.
- **Incremental** — small changes, delivered continuously, small blast radius.
- **Multiple dimensions** — govern technical, **data**, **security**, and
  **operational** concerns, not just code (AP-015).

Evolvability is a design goal, not an afterthought. "Evolutionary" never means
"unplanned" — the guidance is mandatory.

## Fitness functions (AP-016, AP-017)

For each characteristic worth protecting, define an objective, automated check that
runs in the pipeline and fails the build on violation. Choose its category
deliberately:

- **Scope:** *atomic* (one aspect, e.g. no component cycles) vs. *holistic* (an
  interaction, e.g. caching-for-scalability vs. data-staleness-for-security).
- **Cadence:** *triggered* (on build) / *continual* (synthetic transactions,
  monitoring-driven) / *temporal* (break-upon-upgrade, dependency-drift reminders).
- **Result:** *static* (pass/fail) vs. *dynamic* (threshold varies with context,
  e.g. responsiveness vs. concurrent users).
- **Invocation:** *automated* (default) vs. *manual* (legal/exploratory).

**Checklist, not a stick.** Keep the suite lean, collaboratively owned, and justified
by real risk. Document each fitness function in the ADR whose decision it governs
(AP-022). Do not build an ivory-tower web of interlocking gates.

> This playbook is Markdown, not a distributed system: it needs almost no fitness
> functions. Scale the governance to the artifact (AP-003).

## Managing change over time

- **Last responsible moment (AP-014).** Defer hard-to-reverse decisions until
  deferring would cost options; attach an explicit trigger (often a threshold
  fitness function) for re-deciding.
- **Cycle time is a fitness function.** Rising cycle time is architectural decay;
  set a threshold that alarms.
- **Manage coupling actively (AP-008).** Break reuse that becomes a bottleneck (fork,
  duplicate, abstract, wrap); wrap every external tool in an anticorruption layer so
  no vendor becomes the king of the architecture.
- **Watch trends (AP-018).** Coupling, cycles, and complexity trending up are early
  warnings — fix erosion while it's cheap.

## The four key metrics (delivery health, AP-015, AP-019)

Track **deployment frequency** + **lead time** (throughput) and **change failure
rate** + **time to restore** (stability) *together*, at a consistent scope. Improving
throughput while degrading stability is unbalanced and unsustainable.

## Antipatterns to resist

- **Vendor King** — architecture built around a vendor product that dictates all
  future decisions. Treat every tool as an integration point behind an ACL.
- **Last 10% Trap** — the low-code/vendor tool does 90%; the crucial final 10% is
  impossible.
- **Inappropriate governance** — homogenizing on one stack/DB, forcing every project
  to bear the most-complex case's cost.
- **Resume-driven development** — choosing tech for the résumé, not the problem.
- **Fitness-function overload** — governance detached from value.
- **Deferring forever** — it's the *last responsible* moment, and it has a trigger.
