# Wave 206 three-center global-extension protocol

## Frozen branch

Assume only the still-open conditional branch

```text
G is srg(99,14,1,2)
n3=4158, equivalently the induced triangular-prism count P=0
rank_F3(D)=11
```

Let `B` be the `99 by 231` point--triangle incidence matrix, let `D` be the
verified centered Gram matrix of 231 projectively distinct singular columns
in the nonsquare nondegenerate 11-space over `F_3`, and let

```text
P_x=-sum_(T contains x) z_T tensor z_T
```

be the verified rank-six star projector.  Freeze

```text
g_xy=tr(P_x P_y)
h_xy=tr(P_x P_y P_x P_y)
C_xy=Z_x^* Z_y
t_xy=#{entries of the integer nonedge cross Gram C_xy equal to two}.
```

Wave 205 verifies the exact nonedge pair-local constraints

```text
t_xy>=6,
average_(y nonadjacent to x) t_xy=7,
g_xy=2t_xy in F_3,
h_xy=tr((C_xy C_yx)^2),
```

but full-rank local controls at `t_xy=7` realize every
`h_xy in {0,1,2}`.  Pair-local data are therefore insufficient.

## New three-center tensor

For pairwise labelled centers define

```text
tau_(xy;z)=tr(P_x P_y P_z P_y)
          =tr(C_xy C_yz C_zy C_yx).
```

The verified zero-frame identity `sum_z P_z=0` gives the exact contraction

```text
sum_z tau_(xy;z)=0,
tau_(xy;x)=h_xy,
tau_(xy;y)=g_xy,
sum_(z notin {x,y}) tau_(xy;z)=-h_xy-g_xy.       (*)
```

Equation `(*)` is the primary Wave 206 bridge from pair-local fourth traces
to simultaneous three-center compatibility.  It is a formal identity, not
an endpoint obstruction until the remaining terms are controlled from the
actual graph incidence.

Retain the Wave 205 global notation

```text
H=U K_D U^T,
Q=B^T B,
M_x=D S_x D,
w_TU=B(D_T o D_U),
(H 1)_x=tr((Q o M_x)M_x),
(K_D vec(Q))_(T,U)=w_TU^T w_TU.
```

## Required lanes

### Proof A: three-center graph geometry

Classify or sharply constrain `tau_(xy;z)` by the labelled graph type of
`x,y,z`, using the actual `lambda=1`, `mu=2`, linear triangle incidence,
prism-free crossing cap, and rank-11 centered Gram.  At minimum distinguish
the adjacency patterns on three centers and all forced common-neighbor
placements.  Seek an exact row or distribution consequence of `(*)` that
restricts the surviving `t=6,7` pair modules.

Do not infer a true column relation from a Gram-kernel word.

### Proof B: crossing kernel and localizers

Study `K_D` on `row(U)`, the Hadamard localizers `Q o M_x`, and the norms and
mutual inner products of `w_TU`.  Seek a rank, radical, trace, module,
characteristic-polynomial, or sum-of-localizers identity that uses the
actual shared 231-column incidence.  Any tensor-coordinate claim must retain
operator dimensions and characteristic-three signs.

### Construction/literature/hostile controls

Audit exact prior hypotheses relevant to triple projector moments,
three-point Grassmannian designs, Terwilliger modules, and linear triple
systems.  Independently construct or search exact controls satisfying
progressively stronger Wave 206 premises while varying `tau` or `H`.
Every missing target premise must be explicit.  A bounded nonhit is
non-evidentiary.

## Candidate inflection points

A Wave 206 inflection point is reached only if independent verification
establishes at least one of:

- a complete three-center `tau` classification for one or more graph types
  that eliminates a surviving nonedge pair module;
- a new full-matrix/localizer identity incompatible with every endpoint
  fourth-trace distribution;
- a strict improvement to `t_xy`, `Q`, `n3`, rank-11, or endpoint status;
- a construction-level compatibility blueprint substantially closer to the
  99-center endpoint than Wave 205; or
- a well-sealed obstruction proving that all exact three-center data checked
  here still leave the fourth-order route underdetermined, together with the
  newly named four-center/global invariant required next.

A solver timeout, restricted search nonhit, relaxed control by itself, or
unverified derivation is not an inflection point.

## Fixed status boundary

```text
Conway-99:                 UNKNOWN
rank-11 endpoint:          UNKNOWN
n3=4158 endpoint:          UNKNOWN
actual nonedge h:          UNKNOWN
rigorous n3 interval:      708<=n3<=4158
conditional Q bound:       Q>=7059
Q>=7060:                   NOT PROVED
automorphism assumption:   NONE
```

## Frozen inputs

```text
git commit
85e705cc6c2a14d123120c93a847e30aaab1789e

verification/2026-07-29-wave205-integration-audit.md
sha256 f50b5591cb0e1e3dfdd835a22fd9156dd3a2a039323388889a6fa5e756a0a297

verification/2026-07-29-wave205-orchestrator.md
sha256 9b9711ad4b9ac902161833b4a5825404e95ba6f443462ac3d79532df704b2deb

verification/wave205-fourth-trace-globalization-verifier/package-manifest.sha256
sha256 b93f65f72db94539c7d42d7eca6debbaf3a5c4a401db3b812a80549bcb9b8325

attempts/wave205-nonedge-fourth-trace-proof-a/package-manifest.sha256
sha256 2c9976b6cb07a3036df07fd0e7ceb7ffce6a339651d604fcecdcf8c0c3da3d96

attempts/wave205-global-fourth-moment-proof-b/package-manifest.sha256
sha256 a91a2a1cdbc129fa66e9d63b34031a774d5af78c458d18d9a1aadd7e4be217e7

attempts/wave205-fourth-trace-globalization/protocol.md
sha256 a1d45fc0a82b9944a9e020ded3945e75944e0e00202eacbb20eb05598e30bf4d
```

## Separation and evidence rules

- Discovery agents may label results only `DERIVED`, `CANDIDATE`,
  `REFUTED`, or `UNKNOWN`.
- Exact computational claims require deterministic source, tests,
  machine-readable results, input hashes, and a package manifest.
- A fresh verifier must freeze its protocol and independent implementation
  before opening Wave 206 discovery packages.
- Restricted searches must state all restrictions, especially any assumed
  automorphism or fixed local module.
- The verifier may veto or narrow a claim but may not silently repair it.
- Original target status changes only after a complete independently checked
  graph certificate or nonexistence proof.
