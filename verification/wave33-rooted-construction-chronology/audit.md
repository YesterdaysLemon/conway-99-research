# Wave 33 rooted-construction historical chronology audit

## Verdict

`VERIFIED` only for reproducibility of the unchanged frozen construction
packages in their authenticated historical input state.

The original discovery and verifier bytes remain bound by:

```text
candidate freeze:      441465c157f28e658afde31e6ca0cff49ccb5841a001150bd3e3af616c5bf63a
candidate manifest:    0cd192c0182506b3c901806cc96abb9fe53f04dc906b0b5cd73bc9b602558ff4
precomparison freeze:  4ccbbad9c01eab764d9aa6fb207114e43f8c5a36bec3ec5bf0d161708ce0360d
verifier manifest:     20c27560bdf9720cd1cf043b11c218130cd2891a2d3c874f9dbc9bce2f27fbbf
```

No candidate, discovery, precomparison, comparison, or existing verifier
artifact was changed by this repair.

## Integration defect and correction

The discovery input ledger correctly froze the pre-integration
`STRUCTURE.md` bytes at

```text
45640fecaa5834b24063c682c7edd0898f2746253a7708a2c70c3610e4bcb99a.
```

The later central Wave 33 integration inserted its summary into that mutable
document, producing

```text
bfbdb3db713dd160c1941fd52033aac1d5fe182463b23f5bc47ac7d382393aef.
```

The unchanged discovery and comparison programs interpret their input
manifests as live-current paths. Directly running them at the integrated root
therefore fails closed. That failure is expected chronology behavior, not a
candidate defect and not evidence that the original mathematical replay
failed.

The correction does not replace `45640f...` with the later hash and does not
skip a freeze check. It stores all eight historical input byte strings in
`historical-inputs.json`, whose SHA-256 is

```text
d62fc4311577d56cbf34f8bd4e63aefb3b796457b3d020f4322324073d82f7dd.
```

The structured snapshot is deterministic `zlib+base85` JSON, not a binary
archive. Every decoded path, size, and SHA-256 must equal the two original
input ledgers exactly.

## Isolated replay

The chronology checker:

1. authenticates the four original package roots above;
2. validates all 17 candidate-freeze entries, 16 nested candidate-manifest
   entries, 14 verifier-manifest entries, and five precomparison entries;
3. rejects duplicate, absolute, parent-escaping, missing, nonregular, symlink,
   or hash-mismatched inputs;
4. materializes only the eight archived historical inputs plus the
   hash-accepted frozen candidate/verifier files in a new temporary root;
5. copies six solver-provenance files only after their recorded hashes pass;
6. sets `PYTHONDONTWRITEBYTECODE=1` and uses `python -B`;
7. writes regenerated output outside the synthetic checkout; and
8. proves both the synthetic tree and the four source freeze anchors are
   unchanged afterward.

The unchanged historical suites then pass:

```text
construction discovery: 14
construction verifier:  37
historical package total: 51
```

The exact checker regenerates `exact-results.json` byte-for-byte:

```text
ba6640eacd041bc8349024a1d3f13e3d74bd67cdad64d2d78c9a94927319c496.
```

The comparison CLI reproduces the independent search and emits deterministic
JSON with SHA-256

```text
7025cc30551e219c224fe068d641a202db9f1c7a39e480908933e9a93fe597c5.
```

Its regenerated hostile certificate is byte-identical at

```text
340e5df716ad63bceba25c745ab04c22ea1a3dca01e939072f09775a5fc5f634.
```

The accepted comparison result remains the deliberately compact curated
summary at

```text
c0476fb877e0e7d6a6fc63b1a4c72bda0d7804a18a4e4b2b6d5a1bcbc4b6b459.
```

It is not the raw CLI serialization. The unchanged 37-test verifier suite and
the chronology checker bind its claim label, status wall, assignment-row
digest, and hostile `BF` metrics to the full CLI recomputation.

## Hostile chronology tests

Fifteen current-tree tests pass. They cover deterministic archive rebuilding,
the exact eight-path map, historical-over-live `STRUCTURE.md` precedence,
archive-byte and decoded-payload mutation, missing and extra entries,
duplicate JSON keys, duplicate manifest paths, absolute and parent escapes,
symlink sources, candidate-byte mutation, root-manifest mutation, exact
historical replay, status promotion, and no-write/no-`__pycache__` discipline.

The single current-tree command is:

```powershell
python -B -m unittest discover `
  -s verification/wave33-rooted-construction-chronology `
  -p "test_*.py" -v
```

This reports 15 chronology tests. One of those tests performs the complete
unchanged `14+37` historical package replay. These are separate accounting
layers and must not be described as 66 independent theorem tests.

Regenerate the machine-readable result outside a clean checkout with:

```powershell
python -B verification/wave33-rooted-construction-chronology/chronology_replay.py `
  --output <scratch>/chronology-results.json
```

The expected result SHA-256 is
`06bc23423425feb49f37491fc7165aefaf62f50f54ef49992a0da373782bf19a`.

## Scope wall

This repair verifies chronology and reproducibility only. It does not improve
the hostile O-Q object, broaden the one-design MILP, turn the timeout into
evidence, supply an O-O layer, construct or exclude a graph extension, close
the rooted endpoint, exclude `n3=708`, resolve Conway-99, or establish
novelty. All of those statuses remain `UNKNOWN` or `NONE` exactly as before.
