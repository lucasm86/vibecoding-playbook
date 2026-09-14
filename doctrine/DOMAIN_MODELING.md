# Domain Modeling — Supporting Doctrine

> Elaborates how to model the business domain and draw boundaries. Source:
> [`references/03-domain-driven-design.md`](../references/03-domain-driven-design.md).
> Core anchors: **AP-004, AP-005, AP-009, AP-020, AP-007**.

## The first move: classify subdomains (AP-004)

For every capability the system provides, label it:

| Type | What it is | Strategy | Design investment |
|------|-----------|----------|-------------------|
| **Core** | The competitive advantage; complex, volatile | Build in-house, near the experts; invest | Highest — advanced patterns allowed *here* |
| **Supporting** | Necessary but no advantage; mostly CRUD/ETL | Build cheaply; could outsource | Low — simplest pattern |
| **Generic** | A solved commodity | Buy / adopt; **do not build** | None — integrate |

Record the classification and its rationale in `PROJECT.md`. **Re-check it as the
business evolves** — subdomains change type (core→generic when a commodity appears;
supporting→core when it becomes a differentiator). A type change triggers a
superseding decision (AP-011).

> Core ≠ "the technically hardest part." Core = *business* competitive advantage,
> which may be non-technical.

## Boundaries and language

- **Ubiquitous language (AP-020).** Within a bounded context, one term means exactly
  one thing, shared by domain experts, specs, and code. A term that means two things
  signals a missing boundary. Use the domain's own vocabulary in code and tests.
- **Size the boundary to the model, not to a service size (AP-009).** Start wide —
  especially around volatile core subdomains — and split as knowledge grows.
  Refactoring logical boundaries is cheap; refactoring physical ones is not.
- **Do not equate a bounded context with the smallest possible microservice.** That
  is the trap this whole doctrine warns against (AP-007).

## Integration between contexts (AP-005, AP-008)

Choose and *name* the integration pattern per seam, driven by the team relationship:

- **Cooperation** — *partnership* (ad-hoc mutual adaptation) or *shared kernel*
  (a small shared contract; only when cost of duplication > cost of coordination).
- **Customer–supplier** — *conformist* (downstream accepts upstream's model),
  *anticorruption layer / ACL* (downstream translates to protect its model), or
  *open-host service / published language* (upstream offers a stable public
  contract).
- **Separate ways** — no integration.

**Protect core models: ACL inbound, OHS/published language outbound.** Never let one
context import another's internal model directly — that's an escalation (AP-012).

## Tactical patterns follow the subdomain type

Default decision tree (deviate only with a stated reason — these are heuristics, not
laws):

1. **Business logic:** money / audit / deep-analytics → *event sourcing*; else
   complex logic → *domain model*; else complex data → *active record*; else →
   *transaction script*.
2. **Architecture:** event-sourced → *CQRS*; domain model → *ports & adapters*;
   active record → *layered + service layer*; transaction script → *minimal layered*.
   (CQRS also whenever multiple persistent models are required.)
3. **Testing emphasis:** domain model → *pyramid*; active record → *diamond
   (integration-heavy)*; transaction script → *reversed pyramid (E2E-heavy)*.

If the "right" pattern for a supposed core subdomain turns out to be transaction
script, your classification is probably wrong — revisit it.

## Guardrails against misuse

- **Do not cargo-cult tactical DDD** (aggregates, event sourcing, CQRS) onto simple
  CRUD. Advanced patterns are for core complexity only (AP-003).
- **Do not freeze boundaries** — the domain evolves.
- **Discovery technique:** EventStorming is the recommended collaborative way to map
  the domain and its events before committing boundaries.
