# Vibecoding Playbook

> A methodological knowledge base for AI-assisted, **Spec-Driven Development**.
> This repository is **not a software product**. It is an engineering *playbook* —
> a doctrine that guides two collaborating AI roles through the work of turning
> human intent into working, verifiable software.

---

## Why this exists

Large models are expensive to run at their full reasoning capacity, and cheap
models are dangerous when asked to make architectural decisions. The economical
and safe pattern is to **separate reasoning from implementation**:

- A high-capability **Architect** makes the expensive decisions *once*, records
  them so they survive context loss, and removes ambiguity.
- A lower-cost **Executor** makes many small, *constrained* implementation
  decisions inside the boundaries the Architect set.

This playbook is the shared memory that makes that division of labour reliable.
It is distilled from six practitioner books on architecture, systems thinking,
domain modeling, evolutionary design, facilitation, and metrics — translated
into operational rules an AI agent can actually follow.

## The two roles

| | **Architect** (expensive) | **Executor** (cheap) |
|---|---|---|
| Verb | understand → model → reason → decide → specify → decompose | read spec → follow pattern → implement → test → fix → verify → commit |
| Owns | architecture, trade-offs, specs, ADRs, roadmap | code, tests, small local decisions |
| May build | Phase 0, optionally minimal Phase 1 "coding DNA" | Phase 2+ implementation |
| Must never | drift into being the implementation agent | redesign architecture, expand scope, swap technologies |
| Reads | core doctrine + relevant specialized doctrine + source references | PROJECT, SPECS, current feature spec, relevant ADRs, CODESTYLE, ROADMAP, code, tests |

See [`agents/ARCHITECT.md`](agents/ARCHITECT.md) and
[`agents/EXECUTOR.md`](agents/EXECUTOR.md).

## The workflow

```text
HUMAN IDEA / CONVERSATIONS / REQUIREMENTS
                │
                ▼
           PROJECT.md ................ product source of truth
                │
     ┌──────────┴───────────┐
     │   POWERFUL ARCHITECT  │
     └──────────┬───────────┘
                ▼
        SYSTEM ARCHITECTURE
                │
             SPECS.md ............... system-level spec
                │
            specs/*.md ............. feature specs
                │
              ADRs ................. significant decisions, with consequences
                │
            ROADMAP.md ............ phases, referencing specs
                │
     ┌──────────┴───────────┐
     │   LOWER-COST EXECUTOR │
     └──────────┬───────────┘
                ▼
      IMPLEMENT → TEST → FIX
                │
        VERIFY → COMMIT → PUSH
```

The Architect performs expensive reasoning; the Executor performs repetitive
implementation. Everything the Architect decides is written down so the Executor
never has to re-derive it.

## Repository structure

```text
vibecoding-playbook/
├── README.md                     ← you are here
├── .gitignore                    ← keeps source books out of Git
│
├── doctrine/                     ← NORMATIVE. What we have decided to believe.
│   ├── ARCHITECTURE_PRINCIPLES.md   ← the core: AP-001 … (cross-book synthesis)
│   ├── SYSTEMS_THINKING.md
│   ├── DOMAIN_MODELING.md
│   ├── TRADEOFFS.md
│   ├── EVOLUTIONARY_ARCHITECTURE.md
│   ├── ARCHITECTURE_METRICS.md
│   ├── SPEC_DRIVEN_DEVELOPMENT.md   ← our operational workflow
│   └── GIT_GITHUB_POLICY.md
│
├── references/                   ← EVIDENCE. Per-book extraction, kept separate.
│   ├── 01-architecture-hard-parts.md
│   ├── 02-systems-thinking.md
│   ├── 03-domain-driven-design.md
│   ├── 04-evolutionary-architectures.md
│   ├── 05-facilitating-software-architecture.md
│   └── 06-software-architecture-metrics.md
│
├── specialized/                  ← Opt-in, domain-specific knowledge (loaded on demand)
│   └── README.md
│
├── templates/                    ← The artifacts the workflow produces
│   ├── PROJECT.template.md
│   ├── SPECS.template.md
│   ├── FEATURE_SPEC.template.md
│   ├── ADR.template.md
│   ├── CODESTYLE.template.md
│   └── ROADMAP.template.md
│
└── agents/                       ← Role definitions, derived from the doctrine
    ├── ARCHITECT.md
    └── EXECUTOR.md
```

### References vs. Doctrine — the important distinction

- **`references/`** is *evidence*. Each file extracts operational principles from
  one book, on that book's own terms, and is committed separately to preserve
  provenance. References may disagree with each other.
- **`doctrine/`** is *synthesis*. It is what this project has decided to adopt
  after reading all six references together and resolving their tensions with
  explicit context and trade-offs. Doctrine is normative; references are inputs.

Evidence is kept separate from conclusions on purpose: it lets a future reader
(human or AI) audit *why* a rule exists and revise it when the evidence changes.

## Doctrine hierarchy (what to load, when)

1. **Always** — `doctrine/ARCHITECTURE_PRINCIPLES.md` (the AP-xxx core).
2. **When relevant to the task** — the supporting doctrine files
   (systems thinking, domain modeling, trade-offs, evolutionary, metrics) and
   `SPEC_DRIVEN_DEVELOPMENT.md`.
3. **Only when the project's domain calls for it** — anything under
   `specialized/`. The Architect classifies the project first, then loads.
4. **`references/`** — consulted by the Architect for depth; the Executor should
   not normally need them.

## Templates & ADRs

- Templates in `templates/` are the concrete documents the workflow produces.
  Copy them into a real project, strip the `.template` suffix, and fill them in.
- **ADRs** (Architecture Decision Records) capture *significant* decisions —
  their context, the alternatives rejected, the trade-offs accepted, and the
  consequences future implementations must respect. Not every code choice needs
  an ADR; a decision that is expensive to reverse or that constrains later work
  does. See [`templates/ADR.template.md`](templates/ADR.template.md).

## Repository policy

- **Private by default. Always.** This playbook is never made public, forked
  publicly, or mirrored publicly. See
  [`doctrine/GIT_GITHUB_POLICY.md`](doctrine/GIT_GITHUB_POLICY.md).
- **Source books never enter Git.** They are copyrighted source material. This
  repo contains only original analysis, concise paraphrase, and derived rules.
- **Conventional Commits**, meaningful checkpoints, no destructive Git operations
  without justification.

## How to use this in a real project

1. Point the **Architect** at the target codebase (or a blank slate) and at this
   playbook. It classifies the project and loads the relevant doctrine.
2. The Architect produces `PROJECT.md`, then `SPECS.md`, feature specs, ADRs, and
   a `ROADMAP.md`, using the templates here.
3. The Architect may build **Phase 0** (audit/specification) and, optionally, a
   **minimal Phase 1** architectural foundation ("coding DNA"). It stops there.
4. The **Executor** picks up the roadmap and implements Phase 2+ one feature spec
   at a time: read → implement → test → fix → verify → commit → push → next.
5. When implementation reveals that a decision was wrong, the *Executor escalates*
   to the Architect rather than redesigning on its own. New decisions become new
   ADRs.

---

*This playbook follows its own doctrine: simple, explicit, traceable, evolvable,
verifiable.*
