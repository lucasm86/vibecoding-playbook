# Specialized Knowledge

> **Opt-in, domain-specific architecture guides — loaded on demand, not by
> default.**

The core [`doctrine/`](../doctrine/) applies to every project. This directory is
for **deeper knowledge that only some projects need**. Loading all of it always
would violate the doctrine's own principles (AP-003 "how little… can you afford",
AP-019 "don't drown the signal in noise").

## How it works

1. The **Architect classifies the project first** (its domain, style, and the
   subdomains that matter — AP-004).
2. It then loads **only** the specialized guide(s) relevant to that classification.
3. The **Executor does not read these** — it works from PROJECT / SPECS / feature
   specs / ADRs / CODESTYLE / code (per SPEC_DRIVEN_DEVELOPMENT).

This mirrors the "technology radar" idea (reference 05): recorded, curated
knowledge you consult when the context calls for it — not a mandate.

## Candidate future guides

These are **not yet written**, and will be added only when a real project needs
them and there is evidence to ground them (the doctrine forbids speculative
documentation):

- API architecture (REST / gRPC / GraphQL contract design & versioning)
- Multi-tenant SaaS (isolation, tenancy models, noisy-neighbor)
- Event-driven systems (brokers, delivery guarantees, ordering, idempotency)
- Distributed systems (consistency, sagas, partial failure, resilience)
- Microservices (granularity, service mesh, operational concerns)
- Data platforms / data mesh (analytical vs. operational data, ownership)
- Python architecture (packaging, typing, project layout)
- Enterprise architecture (integration, governance at scale)

## Adding a specialized guide

A new guide should:

- be **grounded in evidence** (a source, a reference, real project experience) —
  no speculation;
- follow the **reference/doctrine discipline**: operational rules, decision
  heuristics, anti-patterns, dangerous misapplications, and **when *not* to apply**;
- state its **trigger** — the project classification that causes the Architect to
  load it;
- **defer to the core doctrine** (`AP-xxx`) and cite it, never contradict it
  silently. A genuine conflict is resolved by an ADR, not by a specialized file
  quietly overriding the core.

> Empty ceremonial guides are worse than none. Write one when the knowledge exists
> and a project needs it.
