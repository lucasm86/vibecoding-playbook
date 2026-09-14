# FEATURE SPEC — <feature name>

> **One feature, specified before implementation** (AP-021). Owned by the Architect;
> executed by the Executor. This is the Executor's primary work order — it must be
> unambiguous and objectively verifiable. Written in the ubiquitous language.
>
> `ID:` FS-xxx  ·  `Context:` <bounded context>  ·  `Related ADRs:` ADR-xx, …
> `Roadmap phase:` Phase N

## Objective
One or two sentences: what this feature achieves and for whom. The outcome, not the
mechanism.

## Context
Where this fits in the system (which context/module), why it's needed now, and any
background the Executor needs. Link the relevant SPECS section.

## Requirements
Numbered, testable functional requirements for this feature.

1. …
2. …

## Inputs
Every input: source, type/shape, validation rules, required/optional.

## Outputs
Every output: destination, type/shape, success representation.

## State / Data Changes
What persistent state changes, in which store, owned by which context. Migrations
needed. Consistency expectations (AP-015 data dimension).

## Dependencies
Other features, services, contexts, or external systems this relies on, and the
integration boundary used (ACL/OHS…). Flag any **new** dependency — introducing one
is architecturally significant (AP-012) and needs Architect sign-off / an ADR.

## Constraints
Applicable CFRs and CODESTYLE rules; performance/security/compliance limits that
bound the implementation.

## Error Cases
Each failure mode: trigger → expected behavior/response → recovery. Be exhaustive.

| Error case | Trigger | Expected behavior |
|-----------|---------|-------------------|
| … | … | … |

## Edge Cases
Boundary and unusual conditions (empty, max, concurrent, partial failure, retries,
idempotency).

## Security Considerations
Trust boundaries crossed, authz/authn, PII/sensitive data handling, input
sanitization, audit needs.

## Acceptance Criteria *(objective & testable — AP-016)*
The definition of done for this feature, each independently verifiable. Prefer
Given/When/Then.

- [ ] …
- [ ] …

## Verification
How each acceptance criterion is checked: which tests (unit/integration/E2E — per
the testing strategy for this subdomain, see DOMAIN_MODELING) and which fitness
functions must pass. "Done" = these are green (POSIWID, AP-019).

## Out of Scope
What this feature explicitly does **not** do (guards the Executor against scope
creep).

## Notes for the Executor
Which existing pattern to follow, files/modules likely involved, and the reminder:
anything touching structure, a non-functional characteristic, a dependency, an
interface, or a construction technique ⇒ **escalate** (AP-012), don't decide alone.
