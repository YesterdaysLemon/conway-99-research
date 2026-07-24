# Wave 33 rooted-construction chronology objections

## Replace the frozen STRUCTURE hash with the integrated hash

`REJECTED`. The earlier `45640f...` bytes are part of the historical input
record. Replacing them with `bfbdb3...` would silently rewrite chronology.
The replay instead materializes the exact earlier bytes from an independently
hashed structured snapshot.

## Ignore the stale input-manifest entry

`REJECTED`. The repair authenticates the original ledger byte-for-byte and
requires its complete eight-path/hash map. Missing, extra, reordered,
duplicate, malformed, escaping, or content-mutated entries fail closed.

## The direct integrated-root failure refutes the candidate replay

`REJECTED`. The unchanged programs intentionally compare their historical
ledger with live paths, so later central-document edits make a direct replay
fail. In an authenticated historical root, the unchanged 14 discovery and 37
verifier tests pass and the exact output remains byte-identical.

## The synthetic root might import current central documents

`REJECTED`. Every historical central input is decoded from the
`d62fc4...` snapshot. The materialized `STRUCTURE.md` is asserted to have
`45640f...`, not the integrated `bfbdb3...` hash. No central document is
copied from the live root during materialization.

## A candidate or verifier mutation could be hidden by the snapshot

`REJECTED`. The snapshot contains only the eight historical inputs. Candidate
and verifier bytes must independently pass the original candidate freeze,
nested candidate manifest, precomparison freeze, and verifier manifest before
copying. A one-byte candidate mutation is an explicit rejecting test.

## The accepted comparison summary is the raw comparison CLI output

`REFUTED`. The raw deterministic CLI JSON has SHA-256 `7025cc...`; the compact
accepted summary has SHA-256 `c0476f...`. The unchanged verifier tests and the
chronology replay bind the summary's status wall, claim label, assignment-row
digest, and hostile `BF` fields to the full recomputation. No false byte-
identity claim is made between those two different serializations.

## A passing historical replay promotes the mathematical status

`REJECTED`. Replay proves reproducibility, not construction or exclusion.
Graph extension, full rooted endpoint, `n3=708`, Conway-99, and novelty remain
`UNKNOWN`; the complete-domain UNSAT certificate remains `NONE`.
