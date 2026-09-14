# ROADMAP — <project name>

> **Phased plan of work.** Owned by the Architect. **References specs; does not
> duplicate them.** Organized so the Architect's expensive work happens once
> (Phases 0–1) and the Executor's constrained work fills Phase 2+.

## How to read this
Each item points to the spec/ADR that defines it. Phases are ordered by dependency
and risk; prefer small, independently deliverable increments (AP-015). Mark
provisional/deferred decisions and their triggers (AP-014).

---

## Phase 0 — Audit / Specification  *(Architect)*
Understand the domain and (if brownfield) the existing system; classify subdomains;
produce the source-of-truth artifacts.

- [ ] `PROJECT.md` complete
- [ ] Subdomain classification (AP-004)
- [ ] `SPECS.md` (contexts, boundaries, characteristics, CFRs)
- [ ] Key ADRs for the foundational decisions
- [ ] Feature specs for Phase 1–2 items
- [ ] This ROADMAP

**Exit criteria:** the Executor could start with no architectural ambiguity.

---

## Phase 1 — Architectural Foundation / Coding DNA  *(Architect, optional & minimal)*
The smallest skeleton that fixes the conceptual model and the patterns everything
else will follow. **Not features.**

- [ ] Project scaffold + `CODESTYLE.md`
- [ ] Fitness-function harness / CI wired (AP-017)
- [ ] Core domain model & ubiquitous language in code (AP-020)
- [ ] Reference implementation of the key pattern(s) the Executor will repeat
- [ ] Integration/ACL skeletons for external dependencies

**Exit criteria:** a coherent, verified foundation; the Architect stops here.

---

## Phase 2+ — Implementation  *(Executor)*
Feature by feature, each against its spec. The Executor: read spec → follow pattern →
implement → test → fix → verify → commit → push → next. Escalates architectural
matters (AP-012).

### Phase 2 — <milestone name>
| # | Feature | Spec | Depends on | ADRs | Status |
|---|---------|------|-----------|------|--------|
| 2.1 | … | FS-xxx | — | ADR-xx | ☐ |
| 2.2 | … | FS-xxx | 2.1 | — | ☐ |

### Phase 3 — <milestone name>
| # | Feature | Spec | Depends on | ADRs | Status |
|---|---------|------|-----------|------|--------|
| 3.1 | … | FS-xxx | 2.x | … | ☐ |

*(Add phases/milestones as needed.)*

---

## Deferred Decisions *(AP-014)*
| Decision | Deferred until (trigger) | Owner |
|----------|--------------------------|-------|
| … | … | Architect |

## Risks to the Plan
Sequencing risks, dependency risks, and their mitigations (link `PROJECT.md` risks).
