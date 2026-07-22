# Discovery code

Search encodings, heuristic construction tools, and structural-analysis code
live here. They may suggest candidates or prove restricted exhaustive results,
but they are not the final trust boundary.

## Root scaffold

`root_model.py` deterministically constructs the 14 root-neighbor coordinates,
the 84 allowed pair labels, their incidence matrix data, and 13 generators for
the rooted scaffold relabeling group `C2 wreath S7`. It checks the fixed
identity `B B^T = 11 I + J - M` and the linear neighbor-incidence targets.

```powershell
python code/root_model.py
.venv\Scripts\python -m unittest discover -s code -p "test_*.py" -v
```

For direct common-neighbor linearization, the full model begins with 3,486
unknown residual edge variables and 285,852 conjunction auxiliaries. This count
is diagnostic, not a claim that the direct encoding is the best search method.

## Direct SAT prototype

`sat_model.py` translates the two exact block equations into CNF or a native
cardinality formula. Its default
`compact` variant uses one-way wedge implications and common-neighbor upper
bounds; a global wedge count proves these are exact. The larger `direct`
variant keeps full conjunction equivalences and exact common-neighbor sums as a
cross-check. The default CNF backend uses sequential counters; the native
backend retains exact `AtMost` constraints. Neither makes a completed-graph
automorphism assumption. The proof of compact exactness is recorded in
`attempts/2026-07-22-compact-sat-encoding.md`.

The independently reviewed `native` cardinality backend represents the same
compact constraints directly for MiniCard. It removes sequential-counter
auxiliaries but does not change the mathematics:

```powershell
.venv\Scripts\python code/sat_model.py --pair-count 2 `
  --cardinality native --solve
.venv\Scripts\python code/scout_branches.py --cardinality native `
  --fresh-solvers --conflict-budget 100000
```

`--fresh-solvers` launches one isolated Python process per branch and
materializes branch decisions as unit clauses. This avoids sharing embedded
solver state between branches; startup time is included in each wall time.

For the target this has 289,338 variables, 285,852 ordinary clauses, and
5,838 native `AtMost` constraints. MiniCard has no accepted proof-logging path
in this project, so embedded solves are discovery-only. The same native formula
can be exported canonically with `--opb` and sent to the pinned
Exact/VeriPB/CakePB path. Sequential-counter CNF plus LRAT remains an
alternative. See `attempts/2026-07-22-native-cardinality.md` and
`verification/2026-07-22-veripb-calibration.md`.

The small `pair_count=2` instance reconstructs an `srg(9,4,1,2)`. Embedded
solver output for `pair_count=3` is still labeled `UNSAT_UNVERIFIED`, but the
same negative-control formula now has independently checked LRAT and VeriPB
proofs. Run both controls before any target experiment:

```powershell
.venv\Scripts\python -m unittest discover -s code -p "test_*.py" -v
.venv\Scripts\python code/sat_model.py --pair-count 2 --solve `
  --candidate candidates/calibration-srg-9.srg.json
python verification/check_srg.py candidates/calibration-srg-9.srg.json `
  --vertices 9 --degree 4 --lambda 1 --mu 2
```

A solver's `UNSAT` status alone is not accepted. `--cnf` and `--opb` retain
exact instances for external pinned proof-producing solvers. The PySAT
in-process proof path is intentionally disabled because adversarial
verification found unstable or incomplete traces on the current Windows/Python
build. Any proof artifact must pass independent checking before promotion.

## Theorem-forced `N3` normalization

For the target only, `--n3` fixes one induced six-vertex `N3` obtained by
combining Makhnev's cited theorem with the project's `DERIVED` inference. Global
relabeling then reduces the normalization to the single residual edge unit
`x24=1`:

```powershell
.venv\Scripts\python code/sat_model.py --pair-count 7 --n3 `
  --cardinality native --opb logs/local/conway99-n3-native-lf.opb
```

The flag is rejected on calibration sizes. Both CLI and direct API also reject
combining it with the legacy `--branch` representatives: fixing the witness
changes the stabilizer, so those 11 representatives are no longer a proved
complete joint cover. See `agents/2026-07-22-wave4-n3-normalization.md` and
`verification/2026-07-22-n3-normalization-audit.md`.

The separately proved replacement is a 12-branch cover on the invariant
shared fiber `S_2`:

```powershell
.venv\Scripts\python code\matching_orbits.py --n3-joint
.venv\Scripts\python code\sat_model.py --pair-count 7 --n3 `
  --n3-branch 1 --cardinality native `
  --opb logs\local\conway99-n3-branch-01.opb
```

The normalized stabilizer has order 768. Its 945 compatible fiber matchings
split into 12 exact orbits. Each branch fixes all 66 shared-fiber edges, with
six positive and 60 negative units; `+24` is already supplied by `--n3`, so
the branch itself adds 65 clauses. The certificate and independent checker are
under `verification/n3-joint-cover/`.

## Eleven complete matching branches

`matching_orbits.py` exhausts all 10,395 perfect matchings in one 12-vertex
endpoint fiber and independently traverses the action generated by `C2 wreath
S6`, verifying exactly 11 orbits indexed by partitions of six. This produces a
safe complete split:

```powershell
python code/matching_orbits.py
.venv\Scripts\python code/sat_model.py --pair-count 7 --branch 3+2+1
```

One branch is conditional; all 11 together cover the full rooted search.
This statement concerns the legacy unnormalized search. Do not combine these
representatives with `--n3`; use `--n3-branch 1..12` for the separately
verified normalized split.

Use a conflict budget for scouting runs that must terminate reproducibly:

```powershell
.venv\Scripts\python code/sat_model.py --pair-count 7 --branch 6 --solve `
  --conflict-budget 1000
```

`UNKNOWN` at the budget is expected and has no mathematical evidentiary value.

For a bounded pass over all 11 branches, `scout_branches.py` reuses one
incremental solver and carries learned clauses between assumption branches:

```powershell
.venv\Scripts\python code/scout_branches.py --conflict-budget 100
```

This is explicitly a scouting workflow. An `UNSAT` branch must be regenerated
with its decisions as unit clauses and accompanied by a separately checked
proof before it counts as evidence.
