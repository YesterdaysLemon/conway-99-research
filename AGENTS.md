# Multi-agent research protocol

## Roles

- **Orchestrator:** freezes the statement, assigns disjoint work, integrates
  evidence, and prevents status inflation.
- **Statement/literature agent:** checks definitions, chronology, prior art,
  source quality, and whether the exact target is still open.
- **Proof agents A and B:** pursue structurally different derivations and record
  failed lemmas as carefully as successful ones.
- **Construction agent:** searches for exact objects and emits complete,
  machine-readable candidate certificates.
- **Verifier:** receives claims without relying on discovery internals, attacks
  assumptions and edge cases, and reproduces computations independently.

## Separation rules

1. Agents do not promote their own discoveries to `VERIFIED`.
2. A restricted search must state every restriction, especially any assumed
   automorphism.
3. Absence of a found object is not evidence of nonexistence unless a complete
   search and its certificate are checked.
4. Failed attempts are retained with enough detail to avoid repetition.
5. Human prose, model confidence, and solver exit codes are not certificates.
6. The verifier may veto publication status but cannot silently repair a claim;
   corrections must be recorded.

## Run report schema

Every substantive run report should include:

```yaml
role: proof_a | proof_b | construction | verifier | literature
date_utc: YYYY-MM-DDTHH:MM:SSZ
git_commit: full_hash
claim_label: CITED | DERIVED | VERIFIED | CANDIDATE | REFUTED | UNKNOWN
scope: exact statement or restricted subproblem
inputs: paths and sha256 hashes
method: concise description
command: exact reproducible command, if computational
outputs: paths and sha256 hashes
limitations: explicit caveats
```
