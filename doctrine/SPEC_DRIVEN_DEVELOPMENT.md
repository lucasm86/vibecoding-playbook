# Spec-Driven Development — Operational Doctrine

> The workflow this playbook exists to support, and the division of labour between
> the two agents. Normative. Core anchors: **AP-012, AP-013, AP-021, AP-011,
> AP-016**.

## The pipeline

```text
HUMAN IDEA / CONVERSATIONS / REQUIREMENTS
        │
        ▼
   PROJECT.md ................ product source of truth (what & why)
        │
        ▼   ┌──────────────── ARCHITECT (expensive reasoning) ────────────────┐
   SPECS.md ................... system-level architecture spec
        │
   specs/*.md ................. feature specs (objective acceptance criteria)
        │
     ADRs ..................... significant decisions, immutable, with consequences
        │
   ROADMAP.md ................ phases, referencing specs (not duplicating them)
        │   └────────────────────────────────────────────────────────────────┘
        ▼   ┌──────────────── EXECUTOR (constrained implementation) ──────────┐
   IMPLEMENT → TEST → FIX
        │
   VERIFY → COMMIT → PUSH → NEXT
        │   └────────────────────────────────────────────────────────────────┘
        ▼
   (implementation reveals a wrong decision) ── escalate ──▶ ARCHITECT
```

Everything the Architect decides is **written down** so the Executor never
re-derives it (AP-011). The Architect's success metric is **how much ambiguity it
removes from the Executor's work**.

## The artifacts (templates in [`../templates/`](../templates/))

| Artifact | Owner | Purpose |
|----------|-------|---------|
| `PROJECT.md` | Architect | Product source of truth: problem, users, scope, requirements, constraints, business rules, decisions, DoD. Subdomains classified here (AP-004). |
| `SPECS.md` | Architect | System-level architecture: contexts, boundaries, quanta, cross-cutting CFRs, integration patterns. |
| `specs/<feature>.md` | Architect | One feature: objective, requirements, I/O, state changes, dependencies, error/edge cases, security, **acceptance criteria + verification** (AP-021, AP-016). |
| `ADR-xxx` | Architect | One significant decision: context, decision, alternatives, trade-offs, consequences, verification (AP-011, AP-022). Immutable; supersede to change. |
| `CODESTYLE.md` | Architect | Engineering constraints and project-specific implementation rules the Executor must follow. |
| `ROADMAP.md` | Architect | Phases; **references** specs, does not duplicate them. |

## The two roles

### Architect (high-capability, expensive)

`UNDERSTAND → MODEL → REASON → DECIDE → SPECIFY → DECOMPOSE`

- Classifies the project and loads only the relevant doctrine + specialized
  knowledge.
- Produces PROJECT → SPECS → specs → ADRs → ROADMAP.
- Makes every architecturally-significant decision (five-criteria test, AP-012),
  seeking advice — primarily the human's intent — before deciding (AP-013).
- **May build Phase 0** (audit/specification) and **optionally a minimal Phase 1**
  architectural foundation / "coding DNA."
- **Must never implement Phase 2+.** Its job is to remove ambiguity, not to ship
  features.

### Executor (lower-cost, constrained)

`READ SPEC → INSPECT CODE → FOLLOW PATTERN → IMPLEMENT → TEST → FIX → VERIFY →
COMMIT → PUSH → NEXT`

- Consumes: PROJECT, SPECS, the current feature spec, relevant ADRs, CODESTYLE,
  ROADMAP, existing code, and tests. **Does not read the six source books.**
- Implements Phase 2+ against the spec's acceptance criteria; keeps fitness
  functions and tests green.
- **Must not**: redesign architecture, replace technologies, expand scope, invent
  features, introduce infrastructure, or reinterpret product requirements.
- **Escalates** (seeks advice, AP-013) whenever a decision meets the five-criteria
  test (structure, non-functional characteristics, dependencies, interfaces,
  construction techniques — AP-012), or when the spec is ambiguous, wrong, or
  contradicted by reality.

## The escalation boundary (the most important rule)

The two-agent economics only work if the boundary holds:

- **Executor decides freely:** naming, local structure within a module, which
  existing pattern to follow, how to satisfy a stated acceptance criterion.
- **Executor must escalate:** anything touching structure, a non-functional
  characteristic, a dependency, an interface/contract, or a construction technique;
  anything that would need a new ADR; any surprising system-wide effect (AP-006);
  any repeated cross-boundary change (boundary smell, AP-009).

When in doubt, escalate. A cheap wrong architectural decision is more expensive than
an escalation.

## Phases (see [`../templates/ROADMAP.template.md`](../templates/ROADMAP.template.md))

- **Phase 0 — Audit / Specification.** Understand the domain and (if brownfield) the
  existing system; classify subdomains; produce PROJECT/SPECS/specs/ADRs/ROADMAP.
  Architect.
- **Phase 1 — Architectural foundation / coding DNA.** Minimal skeleton that fixes
  the conceptual model, key patterns, and fitness-function harness. Architect
  (optional, minimal).
- **Phase 2+ — Implementation.** Feature by feature. Executor.

## Verification is objective

Every feature spec ends in **acceptance criteria that are objective and testable**
(AP-016), and where a characteristic must hold, a **fitness function** enforces it
(AP-017). "Done" means demonstrated behavior against those criteria (POSIWID,
AP-019), not "code written."

## Handling change

When implementation reveals that a decision was wrong, the Executor escalates; the
Architect writes a **new ADR that supersedes** the old one (AP-011). The Executor
never redesigns to route around a bad decision.
