# CODESTYLE — <project name>

> **Engineering constraints and project-specific implementation rules.** Owned by
> the Architect; binding on the Executor. This is where conceptual integrity
> (AP-020) becomes concrete at the code level. Keep it specific and enforceable —
> prefer rules that can be a linter/fitness function over prose preferences.

## Languages & Versions
Languages, runtime versions, and the dependency/version policy (temporal fitness
functions for drift — AP-018).

## Project Structure
Directory/module layout and what belongs where. The mapping from bounded contexts
(SPECS) to folders.

## Naming & Ubiquitous Language *(AP-020)*
- Use the domain's ubiquitous language exactly; no synonyms for domain terms.
- Naming conventions for files, types, functions, tests, branches.

## Patterns to Follow
The established idioms of this codebase (per subdomain type — see DOMAIN_MODELING):
error handling, logging, validation, dependency injection, persistence access,
API/contract shape. **The Executor follows these; it does not invent new idioms.**

## Patterns to Avoid
Known anti-patterns for this project (e.g. no cross-context model imports, no
component cycles, no shared mutable state between quanta — AP-007/AP-008).

## Testing
- Testing strategy per subdomain (pyramid / diamond / reversed pyramid).
- Coverage/quality expectations (as goals, not gamed targets — AP-018).
- What must have tests before merge.

## Observability *(AP-018)*
Logging/tracing/metrics conventions. Build logging in early; avoid overwhelming
logging.

## Error Handling
How errors are represented, propagated, logged, and surfaced. Idempotency/retry
rules.

## Security
Input handling, secrets management (never in Git — see GIT_GITHUB_POLICY), authz
patterns, PII rules.

## Formatting & Tooling
Formatter, linter, and their config; the commands that must pass locally
(`format`, `lint`, `test`, fitness functions) before commit.

## Fitness Functions the Executor Must Keep Green *(AP-017)*
List (or link) the automated checks that gate every change. A red one blocks the
commit; fix it or escalate — never bypass.

## Commit & PR Conventions
Conventional Commits; reference the driving spec/ADR; branch-per-feature (see
GIT_GITHUB_POLICY).
