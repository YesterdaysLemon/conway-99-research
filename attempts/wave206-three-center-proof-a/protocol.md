# Wave 206 proof A protocol

Permitted discovery labels are `DERIVED`, `CANDIDATE`, `REFUTED`, and
`UNKNOWN`.

## Frozen target

Work only in the branch

```text
G is srg(99,14,1,2),
P=0,
rank_F3(D)=11.
```

For a fixed center `y`, put

```text
A_x^(y)=P_y P_x P_y restricted to E_y,
tau_y[x,z]=tr(A_x^(y) A_z^(y)).
```

For a frozen nonedge `x,y`, classify the consequences of:

- the labelled adjacency pattern on `x,y,z`;
- the placement of the common neighbor or common-neighbor pair in the seven
  triangles through `y`;
- the exact adjacent outer-cycle modules;
- the verified `t=6,7` nonedge modules; and
- `sum_z A_z^(y)=0`.

## Integrity rules

- A Gram-kernel word is not a true column relation unless nondegeneracy or
  a separate vector argument proves it.
- The 21 four-vertex nonneighbor fibers are labelled; no automorphism or
  transitivity is assumed.
- A list of independently feasible marginal modules is not a shared
  231-column realization.
- A formal zero-sum operator control is not a graph compression unless every
  compression premise is checked.
- Bounded `t=6,7` classification leaves all `t>=8` cases open.

## Reproduction

```powershell
.\.venv\Scripts\python.exe -B attempts\wave206-three-center-proof-a\exact_check.py --verify attempts\wave206-three-center-proof-a\exact-results.json
.\.venv\Scripts\python.exe -B -m unittest -v attempts\wave206-three-center-proof-a\test_exact_check.py
```
