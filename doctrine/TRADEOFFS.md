# Trade-Off Analysis — Supporting Doctrine

> The Architect's core method: how to reach the least-worst decision and record it.
> Sources: [`01`](../references/01-architecture-hard-parts.md),
> [`05`](../references/05-facilitating-software-architecture.md),
> [`06`](../references/06-software-architecture-metrics.md).
> Core anchors: **AP-001, AP-002, AP-016, AP-018, AP-019**.

## The three-step method (from The Hard Parts)

1. **Find what is entangled.** Which dimensions are braided together for this
   decision? (e.g. communication, consistency, coordination; or performance,
   security, cost.)
2. **Analyze how they are coupled.** For each pair: if X changes, is Y forced to
   change? Distinguish static (deploy-together) from dynamic (runtime) coupling.
3. **Assess the impact of change.** Model 2–3 likely scenarios; rate each option
   against the few characteristics that actually matter here.

What remains after the entangled dimensions are resolved is "just design" — the
Executor's territory.

## How to run an analysis

- **Qualitative by default.** Two real architectures rarely permit true quantitative
  comparison. Build a ratings matrix (options × characteristics; High/Med/Low), and
  compare only at the end. Use objective measurement (a spike, a benchmark) where a
  trade-off is contested (AP-016, AP-018).
- **Keep comparisons MECE** — mutually exclusive, collectively exhaustive. Don't
  compare a message queue to an entire ESB; don't omit an obvious option.
- **Stay in context (AP-002).** Add the real domain/operational context before
  concluding; it usually narrows the options and simplifies the decision.
- **Deliver the bottom line (AP-001).** Reduce the analysis to a one- or two-line
  "which matters more here?" in domain terms a non-technical sponsor understands.
  Keep the full evidence retrievable, but don't lead with it.

## Recording a trade-off decision

Every significant trade-off decision becomes an **ADR** (AP-011) that names:

- the options considered (MECE),
- the characteristics weighed and the ratings,
- **the decision and what it sacrifices** (AP-001),
- the consequences future work must respect (AP-022),
- how compliance is verified — usually a fitness function on the *sacrificed*
  characteristic (AP-017).

## Recurring trade-off axes (a starting menu, not answers)

- **Synchronous vs. asynchronous** — async buys responsiveness/fault-tolerance,
  costs guarantees and error-handling simplicity.
- **Orchestration vs. choreography** — a coordinator is explicit but coupling-heavy;
  choreography distributes logic (semantic coupling can only move, never vanish).
- **Shared library vs. shared service** — reuse/consistency vs. independent
  deployment/scaling.
- **Reuse vs. duplication** — share only when cost(coordination) < cost(duplication);
  break reuse when it becomes a bottleneck (AP-008).
- **Consistency vs. availability** — strong consistency vs. eventual + resilience.
- **Throughput vs. stability** — keep the four key metrics balanced (AP-019).

## Guardrails against misuse

- **No "best," ever.** Present the least-worst option and its sacrifice (AP-001).
- **No evangelism.** Don't be pushed into championing a tool; bring every argument
  back to trade-offs. Force honest pros *and* cons out of any "silver bullet."
- **No decision paralysis.** For trivial/reversible choices, skip the matrix and
  decide (AP-014). The method is for the genuinely hard, entangled decisions.
- **Beware the out-of-context trap.** A generic winner can flip once real context is
  added; find the narrow context first.
