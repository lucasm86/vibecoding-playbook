# Reference — Software Architecture Metrics

> Extraction document. Evidence, not doctrine.

## Bibliographic Reference

*Software Architecture Metrics: Case Studies to Improve the Quality of Your
Architecture.* Christian Ciceri, Dave Farley, Neal Ford, Andrew Harmel-Law,
Michael Keeling, Carola Lilienthal, João Rosa, Alexander von Zitzewitz, Rene
Weiss, Eoin Woods. O'Reilly Media, 2022 (ISBN 9781098112202).

## Core Thesis

You cannot guide architecture by instinct or by following a rigid method; you
guide it by **measuring the qualities you care about, early and continuously, and
watching the trend**. A metric alone is just a number — it becomes *engineering*
only when placed in context, given an objective threshold, and automated into a
feedback loop. Crucially, measurement must be **purpose-driven**: start from the
goal (why you're measuring), derive the questions, then the metrics — never
collect numbers that are easy but meaningless. The book spans delivery metrics
(the DORA **four key metrics**, balancing throughput and stability),
maintainability metrics (coupling, cohesion, complexity, the Modularity Maturity
Index), and the meta-methods that keep metrics honest (Goal-Question-Metric,
fitness functions).

## Principles Worth Adopting

### REF-06-P01 — Measure early, continuously, and watch the trend

**Meaning**
Historically teams measured late (after operation). Modern practice extracts
measurements from the pipeline and running system continuously. A single snapshot
tells you where you are; the *trend over time* tells you where you're headed and
guides where to spend architectural effort. Measurement tells you when you've done
*enough* architecture work.

**Operational rule**
Wire measurement into the delivery pipeline from the start; track trends, not just
point values; let the data prioritize architectural attention.

**Architect implication**
Use measurement to decide what to work on and when to stop; don't over- or
under-invest by gut feel.

**Executor implication**
Moderate — the Executor keeps the measured qualities green and reports adverse
trends (rising complexity, coupling, cycle time) rather than silently absorbing
them.

**Spec implication**
Specs name the qualities to be measured and their thresholds.

**ADR implication**
A decision to add/relax a measured threshold is an ADR.

**Verification implication**
Central — this is measurement-as-verification.

**Use when**
Any system that will be maintained over time.

**Do not apply blindly when**
Throwaway prototypes; don't build a metrics platform for a weekend script.

---

### REF-06-P02 — A metric becomes engineering only with context, threshold, and automation

**Meaning**
"Math forms the measure, but evaluating that measure within a useful context
transforms metrics into engineering." A number gathered ad hoc is evidence after
the fact; a number with an objective threshold, run automatically and continuously,
is a proactive force. This is the bridge from *metrics* to *fitness functions*.

**Operational rule**
For every metric that matters, define an objective threshold and automate its
checking in the build; otherwise don't bother collecting it.

**Architect implication**
Turn the metrics that matter into fitness functions with thresholds; decompose
**composite characteristics** (reliability, agility) into measurable parts.

**Executor implication**
Direct: a threshold breach fails the build like a test; the Executor fixes it.

**Spec implication**
Non-functional acceptance criteria = metric + threshold.

**ADR implication**
The threshold and its automation are recorded with the decision they govern.

**Verification implication**
This is the verification mechanism (shared with books 01/04).

**Use when**
Any quality worth protecting.

**Do not apply blindly when**
Exploratory measurement where you're still discovering the right metric.

---

### REF-06-P03 — Start from the goal: Goal → Question → Metric (GQM)

**Meaning**
"To measure something well, you must understand *why* you're measuring it." GQM
builds a tree: **goal** (root) → **questions** that characterize progress →
**metrics** that answer them → **data** (leaves). This gives *traceability*: every
data point traces back to a purpose. It prevents vanity metrics and measuring
what's easy instead of what matters.

**Operational rule**
Never pick a metric first. State the goal and the questions, then choose the metric
that answers them. If a metric doesn't trace to a goal, drop it.

**Architect implication**
Use GQM to define measurement for "gnarly" qualities (technical debt, design
maturity, quality-attribute satisfaction).

**Executor implication**
Minimal — but the Executor should understand *why* a metric exists before optimizing
for it (guards against gaming).

**Spec implication**
Each measured acceptance criterion states the goal/question it serves.

**ADR implication**
Introducing a metric/threshold references the goal it serves.

**Verification implication**
Strong — GQM produces the right things to verify.

**Use when**
Defining metrics for hard-to-measure qualities.

**Do not apply blindly when**
Obvious, standard operational metrics (latency, error rate) where the goal is
self-evident.

---

### REF-06-P04 — Balance throughput and stability (the four key metrics)

**Meaning**
The DORA four key metrics: **deployment frequency** + **lead time for changes**
(throughput) and **change failure rate** + **time to restore service**
(stability). Their power is in the *combination* — improving throughput while
degrading stability is unbalanced and unsustainable. They must be measured over the
*same scope*. They also work as a conversation tool, not a control lever.

**Operational rule**
Track all four together at a consistent scope; improve throughput *and* stability,
never one at the expense of the other.

**Architect implication**
Use the four metrics to steer toward loosely-coupled, testable, deployable,
observable, maintainable architecture — and to know if changes helped.

**Executor implication**
Moderate — small, frequent, safe changes (throughput) with tests and easy rollback
(stability) is exactly the Executor's cadence.

**Spec implication**
Specs favor independently deployable, testable slices.

**ADR implication**
A decision that trades throughput for stability (or vice versa) is recorded as such.

**Verification implication**
Yes — these are directly measurable, ideally from the pipeline.

**Use when**
Assessing delivery health / evolvability.

**Do not apply blindly when**
Using them as individual targets to hoard — they're a balanced set and a
conversation starter, not per-team scoreboards (Goodhart risk).

---

### REF-06-P05 — Guard maintainability: coupling, cohesion, complexity, structural erosion

**Meaning**
Entropy (**structural erosion**) is the enemy; its end state is the **big ball of
mud** — highly coupled, where a change in one part breaks an unrelated part.
Measurable proxies for maintainability include **coupling**, **cohesion**,
**cyclomatic complexity**, cycles, and size. The **Modularity Maturity Index
(MMI)** aggregates these to quantify technical debt and guide refactor/replace/leave
decisions. A **metrics-based feedback loop** catches harmful trends early, while
they're cheap to fix.

**Operational rule**
Track coupling/cohesion/complexity trends continuously; treat rising coupling and
cycles as early warnings; fix erosion while it's small.

**Architect implication**
Use structural metrics to locate technical debt and prioritize refactoring;
maintain modularity as a first-class, measured concern.

**Executor implication**
Direct: don't introduce cycles or tight coupling; keep complexity within thresholds;
follow the module boundaries — these are often automatable fitness functions.

**Spec implication**
Maintainability thresholds are part of acceptance criteria (e.g., "no new package
cycles").

**ADR implication**
Accepting a maintainability cost (deliberate debt) is an ADR with a payoff plan.

**Verification implication**
Strong — static analysis (coupling, cycles, complexity) is automatable.

**Use when**
Any long-lived codebase.

**Do not apply blindly when**
Tiny codebases where the structure is trivially inspectable.

---

### REF-06-P06 — Match the measurement type to what/when you can see (the four quadrants)

**Meaning**
Measurements split along **artifact vs. operational** and **internal vs. external**.
*Artifact* measurements (design docs, code metrics) can be taken early — code
metrics are cheap and accurate but need the code written; design analysis is
predictive but judgment-based. *Operational* measurements (latency, throughput,
MTTR) capture real user experience but need a running system. Runtime observability
comes from **logs, traces, and metrics**.

**Operational rule**
Use predictive/artifact measurements early to guide design; use operational
measurements to validate reality; don't defer all measurement to production.

**Architect implication**
Pick the measurement approach that fits the lifecycle stage and the quality; know
each type's limits (models vs. reality, test vs. reality).

**Executor implication**
Moderate — build in logging/observability early (missing logging is a common
pitfall); avoid overwhelming logging.

**Spec implication**
Specs state which qualities are measured predictively vs. operationally.

**ADR implication**
Choosing an observability/measurement strategy is ADR-worthy.

**Verification implication**
Yes — defines *how* each characteristic is verified.

**Use when**
Planning how to measure a given quality.

**Do not apply blindly when**
Never harmful; just don't build heavy models where direct measurement is cheap.

---

## Decision Heuristics

- **Goal before metric** (GQM): if it doesn't trace to a goal, don't measure it.
- **Number + threshold + automation = engineering;** anything less is after-the-fact
  evidence.
- **Decompose composite characteristics** (reliability, agility) until measurable.
- **Trend > snapshot:** watch direction, catch erosion early.
- **Balance the four key metrics;** never trade stability for throughput.
- **Coupling/cycles/complexity** are the front-line maintainability signals.
- **Measure early (predictive) and late (operational);** know each type's limits.

## Questions the Architect Should Ask

- What goal does this metric serve, and what question does it answer? (GQM)
- Is this characteristic objectively measurable, or is it a composite to decompose?
- What threshold makes this metric actionable, and is it automated?
- Are we watching the trend, or just a one-off number?
- Are throughput and stability both healthy, or are we optimizing one at the other's
  expense?
- Is coupling/complexity trending up (erosion), and is it still cheap to fix?
- Can we measure this predictively now, or must we wait for operation?
- Could this metric be gamed — is anyone optimizing the number instead of the goal?

## Anti-Patterns

- **Vanity metrics** — measuring what's easy instead of what matters.
- **Metrics without thresholds/automation** — data that never drives action.
- **Metric as a target (Goodhart)** — gaming the number, losing the goal.
- **Big ball of mud / structural erosion** — unmanaged coupling growth.
- **Measuring only in production** — no early/predictive signal.
- **Missing or overwhelming logging.**
- **Unbalanced four-key-metrics optimization** — throughput up, stability down.

## Dangerous Misapplications

- **Metric fixation / Goodhart's law.** An AI that optimizes a metric (coverage %,
  complexity number, deployment count) can improve the number while harming the
  goal. Always keep the metric tied to its GQM purpose.
- **Vanity/easy metrics.** Measuring lines of code, commit counts, or raw test
  counts because they're easy. The book explicitly warns against this.
- **Threshold theater.** Setting thresholds so loose they never fail, or so tight
  they only generate noise — either way the metric stops being engineering.
- **Believing models/tests over reality.** The book repeatedly warns models and test
  environments diverge from production; calibrate against real measurement.
- **Treating maintainability metrics as absolute truth.** Coupling/complexity are
  *proxies and signals*, not verdicts; investigate before acting.
- **Over-instrumenting a trivial project.** Metrics infrastructure must be
  proportional to the system (echoes "how little design can you afford").

## Useful Techniques

- **Goal-Question-Metric (GQM)** trees for hard-to-measure qualities.
- **Four key metrics (DORA)** for delivery throughput + stability.
- **Fitness functions** with objective thresholds, automated in the pipeline (the
  metrics→engineering bridge; see the fitness-function testing pyramid).
- **Modularity Maturity Index (MMI)** for quantifying technical debt.
- **Structural analysis** — coupling, cohesion, cyclomatic complexity, cycles,
  size (tools like SonarQube / Sonargraph).
- **Metrics-based feedback loop** to catch erosion early.
- **Observability via logs, traces, metrics**; predictive models for early
  estimates.

## Candidate Rules for Our Doctrine

1. Every metric traces to a goal (GQM); no vanity metrics.
2. A characteristic worth protecting gets an objective threshold, automated in the
   pipeline — otherwise it's not a requirement.
3. Decompose composite characteristics until each part is measurable.
4. Track qualities as trends, catching structural erosion (coupling/complexity)
   early; the Executor keeps them green and reports adverse trends.
5. Balance throughput and stability (four key metrics); never trade one for the
   other silently.
6. Keep measurement proportional to the system; beware Goodhart — the number is a
   proxy for the goal, never the goal itself.

## Concepts We Explicitly Reject or Limit

- We do **not** mandate a specific metrics stack (SonarQube, Sonargraph, MMI
  tooling). The playbook adopts the *discipline* (goal-driven, thresholded,
  automated, trend-watched); concrete tools are chosen per project and scaled to
  its size.

## Relationship to Other References

- **Evolutionary (04)** & **The Hard Parts (01)** — this book supplies the concrete
  *measurements*; those books supply the *fitness function* wrapper and the
  objective-characteristic requirement. Shared authors (Ford, Farley,
  Harmel-Law).
- **Facilitating (05)** — testable CFRs need exactly these measurements; GQM
  complements collectively-sourced principles.
- **Systems Thinking (02)** — trend-watching and feedback loops; guard against
  optimizing a local metric that harms the whole (Goodhart ≈ local optimization).
- **DDD (03)** — coupling/complexity signals help locate where subdomain boundaries
  are wrong.

## Source

*Software Architecture Metrics.* Ciceri, Farley, Ford, Harmel-Law, Keeling,
Lilienthal, Rosa, von Zitzewitz, Weiss, Woods. O'Reilly, 2022. Referenced for
analysis only; no source text reproduced.
