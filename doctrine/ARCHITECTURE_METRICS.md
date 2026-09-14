# Architecture Metrics — Supporting Doctrine

> How to make characteristics objective and keep measurement honest. Source:
> [`06`](../references/06-software-architecture-metrics.md).
> Core anchors: **AP-016, AP-017, AP-018, AP-019**.

## The rule that turns metrics into engineering

> A metric alone is a number. **Metric + context + objective threshold +
> automation + continuous execution = engineering** (AP-016, AP-017).

Anything less is evidence after the fact, not a proactive force.

## Start from the goal (Goal-Question-Metric)

Never pick a metric first (AP-018). Build the tree top-down:

```
GOAL      (why we measure — e.g. "keep the ordering context maintainable")
  └ QUESTION  (e.g. "is coupling between modules growing?")
      └ METRIC   (e.g. afferent/efferent coupling, cycle count)
          └ DATA (the raw measurements)
```

Every data point must trace back to a goal. If a metric doesn't, drop it — it's a
vanity metric.

## Decompose composite characteristics

Vague characteristics (reliability, agility, evolvability) are *composites*. If you
can't measure something directly, decompose it until each part is measurable
(AP-016). Example: *reliability* → availability + data integrity + MTTR.

## What to measure, and when (the four quadrants)

|  | **Internal** (dev/ops see it) | **External** (users/stakeholders see it) |
|--|-------------------------------|------------------------------------------|
| **Artifact** (early, pre-run) | coupling, cohesion, cyclomatic complexity, cycles, MMI | design-doc compliance, standards/GDPR alignment |
| **Operational** (needs running system) | memory, index growth, resource use | latency, throughput, MTTR, failures/month |

Use predictive/artifact measures early to guide design; use operational measures to
validate reality. Don't defer all measurement to production. Runtime observability =
**logs, traces, metrics**; build logging in early (missing logging is a common
pitfall; so is overwhelming logging).

## Maintainability front line (AP-008, AP-018)

The earliest, cheapest signals of decay:

- **Coupling** and **dependency cycles** — the road to the big ball of mud.
- **Cyclomatic complexity** and size.
- **Modularity Maturity Index (MMI)** to quantify technical debt and prioritize
  refactor / replace / leave.

Track them as **trends** in a feedback loop; catch structural erosion while it's
cheap to fix. Treat these as *proxies and signals*, not verdicts — investigate before
acting.

## Delivery metrics — the four key metrics

**Deployment frequency + lead time** (throughput) and **change failure rate + time to
restore** (stability). Track together, same scope, balanced (AP-019). They are a
conversation tool, not per-team scoreboards.

## Guardrails against misuse

- **Goodhart's law (AP-018).** A metric made into a target gets gamed. Keep every
  metric tied to its GQM purpose; optimize the *goal*, not the number.
- **No vanity metrics.** Lines of code, commit counts, raw test counts — measuring
  what's easy instead of what matters.
- **No threshold theater.** Thresholds so loose they never fire, or so tight they
  only make noise, both stop being engineering.
- **Don't trust models/tests over reality.** Test environments and models diverge
  from production; calibrate against real measurement.
- **Keep it proportional (AP-003).** Metrics infrastructure scales to the system;
  don't build a measurement platform for a trivial project.
