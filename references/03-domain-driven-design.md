# Reference — Learning Domain-Driven Design

> Extraction document. Evidence, not doctrine.

## Bibliographic Reference

*Learning Domain-Driven Design: Aligning Software Architecture and Business
Strategy.* Vlad (Vladik) Khononov. O'Reilly Media, 2021 (ISBN 9781098100131).

## Core Thesis

Software design should be **driven by the business domain**, not by technology
fashion. The most important act is **classifying subdomains** by their strategic
value — **core** (the company's competitive advantage; complex, volatile, must be
built in-house), **supporting** (necessary but simple CRUD/ETL; no advantage),
**generic** (complex but solved commodity; buy/adopt, don't build) — because that
classification *drives* every downstream decision: boundaries, business-logic
pattern, architecture, testing, integration, and sourcing. Design is organized
around **bounded contexts** (each with a consistent **ubiquitous language**),
integrated through explicit **context-mapping** patterns, and it must **evolve**
as subdomains change type. Above all: match the sophistication of the solution to
the complexity of the problem — use simple tools by default and reach for advanced
patterns only when a core subdomain actually demands them.

## Principles Worth Adopting

### REF-03-P01 — Classify subdomains before designing anything

**Meaning**
Core/supporting/generic is the strategic lens. Core = competitive advantage
(complex, in-house, invest); supporting = simple, no advantage (build cheaply or
outsource); generic = commodity (buy/adopt an existing solution). Effort must be
proportional to strategic value.

**Operational rule**
For every part of the system, label its subdomain type first; let that label
govern how much design sophistication it gets.

**Architect implication**
Start domain analysis with subdomain classification; concentrate the expensive
design work on core subdomains and deliberately under-invest in supporting/generic.

**Executor implication**
Important: the Executor must not gold-plate a supporting/generic area, nor treat a
core-subdomain spec as routine CRUD. The spec should state the subdomain type.

**Spec implication**
PROJECT/SPECS tag each subdomain with its type and the rationale.

**ADR implication**
"Build vs. buy vs. adopt" for a subdomain is an ADR driven by its type.

**Verification implication**
Indirect — mismatched complexity (a "core" subdomain that turns out to be trivial
CRUD) is a signal the classification is wrong.

**Use when**
The system spans multiple business capabilities.

**Do not apply blindly when**
A tiny single-purpose tool with one obvious concern.

---

### REF-03-P02 — Ubiquitous language and bounded contexts

**Meaning**
Within a **bounded context**, one consistent **ubiquitous language** is shared by
domain experts, code, and docs — the same term means exactly one thing. Different
contexts may use the same word for different concepts; the boundary is where the
language stays consistent.

**Operational rule**
Name things in code and specs using the domain's own vocabulary, consistently
within a context. A term that means two things signals a missing boundary.

**Architect implication**
Establish the language per context; make it the vocabulary of the specs.

**Executor implication**
Direct: use the established domain terms exactly; do not invent synonyms. This is
conceptual integrity at the naming level (ties to REF-02-P03).

**Spec implication**
Specs and acceptance criteria are written in the ubiquitous language.

**ADR implication**
Defining/redrawing a context boundary is an ADR.

**Verification implication**
Weak/manual — glossary consistency; occasionally lintable.

**Use when**
Always, within any modeled domain.

**Do not apply blindly when**
Purely technical/infrastructural code with no business language.

---

### REF-03-P03 — Size the bounded context to the model; start wide, split later

**Meaning**
Size is one of the *least* useful heuristics for boundaries. Make size a function
of the model, not the reverse. Because refactoring *logical* boundaries is far
cheaper than refactoring *physical* ones, start with **wider** boundaries
(especially around volatile core subdomains) and decompose as domain knowledge
grows. Equating "bounded context" with "smallest possible microservice" is a trap.

**Operational rule**
Don't split into the smallest services up front. Begin with broader boundaries;
narrow them once the model stabilizes and knowledge increases.

**Architect implication**
Resist premature microservice granularity; defer physical splits until the model
is understood. (Directly reinforces The Hard Parts' granularity balance.)

**Executor implication**
The Executor never splits a context on its own; boundary changes are architectural.

**Spec implication**
SPECS records current boundaries and which are provisional/expected to split.

**ADR implication**
Any boundary split/merge is an ADR.

**Verification implication**
Indirect — a change that repeatedly forces edits across contexts signals wrong
boundaries.

**Use when**
Early-stage or uncertain domains.

**Do not apply blindly when**
A well-understood, stable domain where the right small boundaries are already
known.

---

### REF-03-P04 — Integrate contexts with explicit context-mapping patterns

**Meaning**
Relationships between contexts are chosen deliberately, driven by team
collaboration: **cooperation** (partnership; shared kernel), **customer–supplier**
(conformist; anticorruption layer; open-host service / published language), or
**separate ways**. A core subdomain protects itself with an **anticorruption
layer** (ACL) inbound and a **published language / open-host service** (OHS)
outbound.

**Operational rule**
Never let contexts leak models into each other implicitly. Pick and name the
integration pattern; protect core models with an ACL; expose stable contracts via
OHS/published language.

**Architect implication**
Choose the integration pattern per seam, considering the team relationship and
cost of coordination vs. duplication (shared kernel only when duplication cost >
coordination cost).

**Executor implication**
Direct: when integrating, the Executor implements the *chosen* pattern (e.g.,
builds the ACL translation) and does not bypass it by importing the other
context's model directly.

**Spec implication**
Each cross-context integration spec names its mapping pattern and contract.

**ADR implication**
Every integration pattern choice is ADR-worthy (it encodes a coupling decision).

**Verification implication**
Partial — "context A must not import context B's internal model" can be a fitness
function.

**Use when**
Any multi-context / multi-team integration.

**Do not apply blindly when**
Single context — there's nothing to map.

---

### REF-03-P05 — Let subdomain type drive tactical patterns (the decision tree)

**Meaning**
A concrete, ordered heuristic:
- **Business logic pattern:** monetary/audit/deep-analytics → *event-sourced
  domain model*; else complex logic → *domain model*; else complex data → *active
  record*; else → *transaction script*.
- **Architecture pattern:** event-sourced → *CQRS*; domain model → *ports &
  adapters*; active record → *layered + service layer*; transaction script →
  *minimal layered*. (CQRS also whenever multiple persistent models are needed.)
- **Testing strategy:** domain model → *testing pyramid*; active record → *testing
  diamond (integration-heavy)*; transaction script → *reversed pyramid (E2E-heavy)*.

**Operational rule**
Use the decision tree as the default starting point; deviate only with a stated
reason. Prefer simple patterns; escalate to advanced ones only when the subdomain
demands it.

**Architect implication**
Drive tactical choices from subdomain type, not preference; record deviations.

**Executor implication**
Direct: the Executor implements the pattern the spec names and writes tests in the
prescribed emphasis; it does not substitute a different pattern.

**Spec implication**
Feature specs state the business-logic pattern, architecture pattern, and testing
emphasis (or inherit them from the context's SPECS).

**ADR implication**
Choosing/deviating from the tree for a context is an ADR.

**Verification implication**
Yes — the testing-strategy choice defines what "verified" means for that code.

**Use when**
Implementing any bounded context's internals.

**Do not apply blindly when**
The team has strong justified reasons for a uniform approach (e.g., event sourcing
everywhere) — heuristics are not hard rules.

---

### REF-03-P06 — Design must evolve as subdomains change type

**Meaning**
Subdomains migrate (core↔generic, supporting↔core, etc.) as the business and
market change. When type changes, boundaries, integration patterns, and sourcing
must change too. This is normal, not failure.

**Operational rule**
Periodically re-evaluate subdomain classification; when it shifts, revisit the
strategic decisions it drove (build/buy, ACL/OHS, in-house/outsource).

**Architect implication**
Own the evolution: watch the four change vectors (business domain, org structure,
domain knowledge, growth) and re-decide.

**Executor implication**
Minimal — but the Executor surfaces "this 'simple' area keeps growing complex
rules," a signal a supporting subdomain is becoming core.

**Spec implication**
Specs record assumptions that, if they change, invalidate the design.

**ADR implication**
Re-classification triggers superseding ADRs (ties to evolutionary architecture).

**Verification implication**
No.

**Use when**
Long-lived systems.

**Do not apply blindly when**
Short-lived throwaway software.

---

### REF-03-P07 — Match solution sophistication to problem complexity

**Meaning**
The whole book models restraint: advanced patterns (domain model, event sourcing,
CQRS) are *costs*, justified only by core-subdomain complexity. Applying elaborate
patterns everywhere is "wasteful and ineffective."

**Operational rule**
Default to the simplest pattern that fits; require a complexity justification to
escalate.

**Architect implication**
Actively push back on over-engineering; reserve sophistication for where advantage
lives.

**Executor implication**
Direct: don't introduce advanced patterns the spec didn't call for.

**Spec implication**
Specs justify any advanced pattern by the complexity it addresses.

**ADR implication**
Escalation to an advanced pattern is an ADR with a complexity rationale.

**Verification implication**
Indirect.

**Use when**
Every implementation choice.

**Do not apply blindly when**
Never harmful; this is a load-bearing default.

---

## Decision Heuristics

- **Classify first:** core (invest, build) / supporting (cheap, maybe outsource) /
  generic (buy/adopt).
- **Boundary size = f(model)**, not f(desired service size). Start wide, split on
  knowledge.
- **Business-logic decision tree:** audit/money/analytics → event sourcing; complex
  → domain model; complex data → active record; else → transaction script.
- **Architecture follows business-logic pattern** (see REF-03-P05).
- **Testing emphasis follows pattern:** pyramid / diamond / reversed pyramid.
- **Shared kernel only if** cost(duplication) > cost(coordination); keep it to
  contracts.
- **Protect core:** ACL inbound, OHS/published language outbound.
- Core subdomains: **in-house, near the domain experts**. Generic: **don't build**.

## Questions the Architect Should Ask

- Is this subdomain core, supporting, or generic — and what's the evidence?
- Where does the ubiquitous language stay consistent? (That's the boundary.)
- Am I sizing the context to the model, or to a microservice fashion?
- What's the team relationship across this seam, and which mapping pattern fits?
- Does the chosen business-logic pattern match the subdomain type — and if not, is
  my classification wrong?
- Am I applying an advanced pattern where a transaction script would do?
- Which assumptions, if the business changes, would flip this subdomain's type?

## Anti-Patterns

- **Equating bounded context with the smallest possible microservice.**
- **Building a generic subdomain** in-house instead of buying/adopting.
- **Gold-plating supporting subdomains** with domain models/event sourcing.
- **Implicit model leakage** between contexts (no ACL/OHS).
- **Anemic use of the same advanced pattern everywhere** regardless of complexity.
- **Premature physical decomposition** before the model is understood.

## Dangerous Misapplications

- **Cargo-culting DDD tactical patterns** (aggregates, event sourcing, CQRS) onto
  simple CRUD. The book explicitly warns these are for *core* complexity only. An
  AI that applies them universally has inverted the message.
- **Treating "core subdomain" as "the technically hardest part."** Core = *business
  competitive advantage*, which may be non-technical.
- **Freezing boundaries** because "DDD says bounded contexts" — the book insists
  boundaries evolve.
- **Microservice-per-entity** justified as "bounded contexts."
- **Over-reading the decision tree as law** — it is heuristics; deviation with a
  reason is allowed.

## Useful Techniques

- **Subdomain analysis** (core/supporting/generic) as the first design step.
- **EventStorming** — collaborative workshop to discover the domain and its events.
- **Context mapping** — explicit relationship/integration patterns between contexts.
- **Ubiquitous language / glossary** per context.
- **Domain-driven decision trees** for business-logic, architecture, and testing.
- **Aggregates / value objects** as consistency and unit-test boundaries (in domain
  models).

## Candidate Rules for Our Doctrine

1. Every part of a system is classified core/supporting/generic before design, and
   design investment is proportional to that classification.
2. Boundaries follow the domain model (ubiquitous language consistency), not a
   target service size; start wide and split as knowledge grows.
3. Cross-boundary integration uses an explicitly named context-mapping pattern;
   core models are protected by ACL/OHS.
4. Tactical patterns (business logic, architecture, tests) default from the
   subdomain type; advanced patterns require a complexity justification.
5. Subdomain classification is periodically revisited; type changes trigger
   superseding decisions.
6. The domain's ubiquitous language is the naming standard for specs and code.

## Concepts We Explicitly Reject or Limit

- We do **not** import the full tactical pattern catalog as mandatory. The
  *classification → proportional design* discipline is what we adopt; specific
  patterns are options selected per context.

## Relationship to Other References

- **The Hard Parts (01)** — bounded contexts are the natural seams for
  quantum/granularity decisions; both preach "start coarse, justify splits."
- **Systems Thinking (02)** — ubiquitous language and context boundaries are
  concrete tools for conceptual integrity and synthesis.
- **Evolutionary Architectures (04)** — REF-03-P06 (subdomains evolve) is the
  domain-level case of evolutionary/guided change.
- **Facilitating Software Architecture (05)** — context maps mirror team topology;
  integration patterns are chosen by team relationship.

## Source

*Learning Domain-Driven Design.* Vlad Khononov. O'Reilly, 2021. Referenced for
analysis only; no source text reproduced.
