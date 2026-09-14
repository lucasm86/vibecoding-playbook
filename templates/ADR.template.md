# ADR-XXX — <decision title (short noun phrase)>

> **Architecture Decision Record.** One significant decision. **Immutable** once
> Accepted — to change it, write a new ADR that supersedes this one (AP-011).
> Target ~1–2 pages. Written for the reader.
>
> Only architecturally-significant decisions get an ADR: those affecting
> **structure, non-functional characteristics, dependencies, interfaces, or
> construction techniques** (the five-criteria test, AP-012).

`Date:` YYYY-MM-DD  ·  `Deciders:` <who>  ·  `Related:` FS-xx, ADR-xx

## Status
Proposed | Accepted | Superseded (by ADR-YYY) | Rejected | Retired

## Context
What forces this decision? The problem, the constraints, the relevant CFRs/
principles, and the advice sought (AP-013) — whose input (human, code, doctrine)
shaped it. State the situation-specific context that makes the decision correct
(AP-002).

## Decision
The decision, in a few sentences (bold it). State it as a proposition — the choice
**and its justifying reasons** (AP-010).

## Alternatives Considered
Keep the comparison MECE (AP-001/trade-offs).

### Alternative A — <name>
- **Benefits:** …
- **Costs:** …
- **Reason rejected:** …

### Alternative B — <name>
- **Benefits:** …
- **Costs:** …
- **Reason rejected:** …

## Trade-offs
- **What we gain:** …
- **What we lose / sacrifice:** … *(naming the sacrifice is mandatory — AP-001)*
- **Reversibility:** one-way door | two-way door. If deferred, the trigger to
  re-decide (AP-014): …

## Consequences
What future implementations **must respect** as a result (AP-022): constraints
imposed, options foreclosed, follow-on work required. This is what the Executor is
bound by.

## Verification
How continued compliance is checked — the fitness function(s) or acceptance criteria
that guard this decision (AP-017). Name them.

## References
Related specs (FS-xx), doctrine principles (AP-xxx), superseded/superseding ADRs.
