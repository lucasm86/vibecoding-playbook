# Git / GitHub Policy — Operational Doctrine

> Version-control and repository rules for this playbook and for any project it
> guides. Normative.

## 1. Private by default — always

- Repositories are **private** unless a human explicitly and specifically decides
  otherwise for a given repo.
- **Never** create a public repository, **never** change visibility to public, and
  **never** create a public fork or mirror.
- If a hosting action cannot be performed privately, stop and ask a human.

## 2. Source material never enters Git

- Copyrighted source material (the six books, any PDFs/EPUBs, licensed datasets)
  is **never committed**. `.gitignore` blocks `*.pdf *.epub *.mobi *.azw *.azw3
  *.djvu` and working dirs (`books/ sources/ source-books/ extracted/ _work/`).
- The repo contains only original analysis, concise paraphrase, and derived rules —
  no chapter reproductions, no long quotations.
- Before **every** commit, verify no source binary is staged (`git status`).

## 3. Secrets never enter Git

- No credentials, API keys, tokens, private keys, connection strings, or personal
  data in commits or history.
- Keep secrets in environment variables or an ignored `.env`; commit a
  `.env.example` with blanks instead.
- If a secret is committed, treat it as compromised: rotate it, then scrub history.

## 4. Conventional Commits

Format: `type(optional-scope): imperative summary`. Types: `feat`, `fix`, `docs`,
`chore`, `refactor`, `test`, `build`, `ci`, `perf`, `style`, `revert`.

- One coherent change per commit; the message says *what* and *why*, not a diff dump.
- Reference the driving spec/ADR where useful (e.g. `feat(orders): add checkout saga
  (ADR-014)`).

## 5. Meaningful checkpoints, not noise

- Commit at meaningful boundaries (a completed spec, a passing feature, a doctrine
  section) — not after every trivial edit, and not one giant commit for everything.
- Preserve **provenance**: independent pieces of work get independent commits so
  history stays legible (this playbook committed each book extraction separately).

## 6. Push policy

- Push each meaningful checkpoint to the private remote.
- **Never fabricate a successful push.** If auth or the network fails, say so, keep
  the work committed locally, and document exactly what remains to sync.
- If GitHub auth is unavailable, continue locally with full history and record the
  blocker.

## 7. Branch safety

- Work on `main` for solo/small doctrine work is acceptable; for feature work in a
  guided project, branch per feature/spec and open a PR.
- Do not commit directly to a protected branch when a review process exists.

## 8. No destructive Git without justification

- Avoid `push --force`, hard resets on shared branches, history rewrites, and branch
  deletion unless a human has asked and the reason is recorded.
- Prefer `revert` (a new commit) over rewriting published history.
- Never bypass hooks (`--no-verify`) or signing unless explicitly requested.

## 9. Attribution

- Follow the session's configured commit/PR attribution lines. Do not invent
  attribution the harness didn't specify.

## 10. Pre-commit checklist (run every time)

1. `git status` — confirm intended files only; **no source books, no secrets**.
2. `git diff` (staged) — confirm the change matches the intended checkpoint.
3. Markdown/structure sane.
4. Commit with a Conventional Commit message.
5. Push to the private remote; verify success honestly.
