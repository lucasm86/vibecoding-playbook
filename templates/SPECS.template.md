# SYSTEM SPECS — <system name>

> **System-level architecture specification.** Owned by the Architect. Sits between
> `PROJECT.md` (product) and `specs/*.md` (features). Describes the *structure* the
> features live in. References ADRs; does not restate their reasoning.

## Purpose & Scope
What this system does as a whole, and the boundary of this spec. One paragraph on
the system's purpose and the behavior that **emerges** from its parts (AP-006).

## Architecture Characteristics (the "-ilities" that matter here)
The few characteristics this architecture is optimized for, each stated
**objectively/measurably** (AP-016), with the ones deliberately traded away noted
(AP-001).

| Characteristic | Target (measurable) | Priority | Traded against |
|----------------|--------------------|----------|----------------|
| … | … | … | … |

## Bounded Contexts / Modules
Each context: its responsibility, its subdomain type (AP-004), its ubiquitous
language boundary (AP-020), and its owner/team (AP-023).

| Context | Responsibility | Subdomain type | Owner |
|---------|---------------|----------------|-------|
| … | … | … | … |

## Architecture Quanta & Boundaries *(AP-007, AP-009)*
Which parts deploy independently, and where the coupling points are (shared DBs,
orchestrators). Note which boundaries are provisional and expected to split.

## Coupling Map *(AP-008)*
- **Static coupling** (must deploy together): …
- **Dynamic coupling** (runtime calls): …
- External dependencies and their anticorruption layers: …

## Integration Patterns *(AP-005)*
Per seam: the named context-mapping / integration pattern and its contract.

| Seam | Pattern (partnership / shared kernel / conformist / ACL / OHS / separate) | Contract |
|------|--------------------------------------------------------------------------|----------|
| … | … | … |

## Data Architecture *(AP-015 — data dimension)*
Ownership of data per context, operational vs. analytical data, consistency model
(strong vs. eventual), migration approach.

## Cross-Cutting Concerns
Security/trust boundaries, observability (logs/traces/metrics), error handling,
auth. Each with its measurable requirement.

## Governance — Fitness Functions *(AP-017)*
The automated checks that protect the characteristics above. Keep lean.

| Characteristic / rule | Fitness function | Category | Threshold |
|-----------------------|------------------|----------|-----------|
| … | … | atomic/holistic · triggered/continual/temporal · auto/manual | … |

## Technology Choices
The stack, with a one-line justification each and a pointer to the ADR. Every
external tool is an integration point behind a boundary (AP-005).

## Key Decisions (ADR index)
`ADR-xxx — summary` for each system-level decision.

## Open Architectural Questions
Unresolved system-level questions and what's needed to resolve them.
