# PROJECT — <product name>

> **Product source of truth.** Owned by the Architect. Everything downstream
> (SPECS, feature specs, ADRs, ROADMAP) derives from this file. Keep it current;
> when a decision changes, move it to *Superseded Decisions* rather than deleting.
> Write in the domain's **ubiquitous language** (AP-020).

## Overview
One paragraph: what this product is and the value it delivers.

## Problem
The problem being solved, and why it's worth solving now. What happens if it isn't.

## Users
Who uses it, their goals, and their context. Distinct user types/roles.

## Product Vision
The direction over the next horizon. What "great" looks like.

## Scope
- **In scope:** …
- **Out of scope (explicitly):** … *(guarding against scope creep — the Executor
  never expands this)*

## Current State
Greenfield, or a description of the existing system (brownfield): what exists, its
health, known pain points. For brownfield, note where the audit (Phase 0) lives.

## Subdomain Classification *(AP-004)*
| Capability | Type (core / supporting / generic) | Rationale | Sourcing (build / buy / adopt) |
|-----------|-----------------------------------|-----------|-------------------------------|
| … | … | … | … |

> Revisit when the business changes — subdomains change type.

## Functional Requirements
Numbered, testable statements of what the system must do. Group by capability.

## Technical Constraints
Platforms, languages, hosting, compliance, existing systems to integrate with,
performance/scale envelopes, budget/time limits.

## Business Rules
Domain rules and invariants that must always hold (independent of UI/tech).

## UX / UI
Key flows, design system or brand constraints, accessibility requirements. Link
mockups if any.

## Integrations
External systems/services, their contracts, and the integration pattern
(ACL / OHS / partnership …) per seam (AP-005).

## Cross-Functional Requirements (CFRs) *(AP-016)*
Objective, measurable, system-wide requirements with thresholds (e.g. "any user
action < 500 ms p99"). These become fitness functions.

## Risks
Known risks, likelihood/impact, and mitigation or monitoring plan.

## Decisions
Pointers to the ADRs that shape this product (id + one-line summary). The ADRs
themselves are the record.

## Superseded Decisions
Decisions no longer in force, with the ADR that superseded each. Kept for history.

## Open Questions
Unresolved questions blocking or shaping design, with who/what is needed to resolve.

## Definition of Done
What "done" means for this product/increment, framed as **observable outcomes**
(POSIWID, AP-019): the acceptance criteria, the passing fitness functions, the
verifications — not "code written."
