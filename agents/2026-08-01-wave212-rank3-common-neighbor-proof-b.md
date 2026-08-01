# Wave 212 proof B: rank-three common-neighbor incidence

```yaml
role: proof_b
date_utc: 2026-08-01T05:02:46Z
git_commit: 698f4db2cecd67fb4b9cfa8ff2bf7b375d9d93f3
claim_label: DERIVED
scope: exact common-neighbor, triangle, four-cycle, and simultaneous coloured-one-factor consequences for rank-three orbits 0, 4, and 29
inputs:
  - attempts/wave210-rank3-marked-outside-coupling-proof-a/hostile-controls.json sha256 32788ca74d17730d7e3c8aec12b23af13c26fc772dd94b36ffbcbab6473c38dd
  - attempts/wave210-rank3-marked-outside-coupling-proof-a/package-manifest.sha256 sha256 d2c2bef169139d4e47d55d5084d5912caf5b8fa20bacda1ee5031e4e4e121722
method: local 7K2 edge-species split, four-cycle opposite-pair census, simultaneous labelled colour matchings, and exact hostile incidence controls
command: C:\Users\Yeste\OneDrive\Documents\math conjecture\.venv\Scripts\python.exe -B attempts\wave212-rank3-common-neighbor-proof-b\exact_check.py --verify
outputs:
  - attempts/wave212-rank3-common-neighbor-proof-b/exact-results.json sha256 370fff3eef0b4b9fc78f1e7d5d4968a2cd7582c88118675850d3bb417871f335
  - attempts/wave212-rank3-common-neighbor-proof-b/hostile-incidence-controls.json sha256 d583aad1c09d718ff8f8d8690a474e419e2aacf51ec050816903a24a261aa604
limitations: no orbit is excluded, the controls fail FD and most quadratic pairs, no full D is constructed, and global status is UNKNOWN
```

For an outside column `C_x`, put `t_x=|C_x|` and
`a_x=e(A_S[C_x])`.  The local `7K2` condition forces

```text
q=1 degree = t_x-2a_x,
all-outside triangle degree = 7-t_x+a_x.
```

Summing over each of the three representatives gives exactly 64 support-
coloured outside edges, 456 disjoint-support edges, and 152 all-outside
triangles.  The complete four-cycle census is

```text
0 support: 1211
1 support:  588
2 support:   40 alternating + 220 adjacent
3 support:   12
4 support:    8
total:     2079.
```

The fourteen support-colour matchings can be selected simultaneously in every
orbit: their candidate edge sets are disjoint by unique intersection colour,
and the committed labelled witnesses give all 64 edges.  Thus this natural
compatibility test produces no obstruction.

The package also seals one complete 152-block labelled triangle-incidence
control for each orbit.  Each yields 520 outside edges with every required
degree, all ten selected pair values, and no common neighbor on the 40 `q=2`
pairs or 64 coloured edges.  These are hostile relaxations, not completions:
they satisfy only `499/1190`, `534/1190`, and `532/1190` `FD` entries and only
`1256/3570`, `1259/3570`, and `1299/3570` quadratic pairs.  They also contain
132, 154, and 123 spurious outside triangles.

Finally, both sides of the global outside length-two-path budget equal 5888.
Consequently a degree-correct binary `D` satisfying every pairwise common-
neighbor *upper bound* automatically satisfies every quadratic equality.
This is the sealed forbidden-subconfiguration reduction; it is not yet solved.
Conway-99 remains `UNKNOWN`.
