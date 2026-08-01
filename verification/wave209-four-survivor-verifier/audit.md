# Wave 209 rank-three signed-trade verifier audit

```yaml
role: verifier
date_utc: 2026-08-01T03:40:53Z
git_commit: c58fd917ea8f9622e1388f10b0e0e3c709ba4854
claim_label: VERIFIED
scope: >-
  Source-blind reconstruction and post-source full-set audit of the sealed
  Wave 209 rank-three proof-A package, preserving its aggregate/local scope;
  plus a separately labelled DERIVED six-row selected-line narrowing.
```

## Verdict

`PASS_VERIFIED_SCOPED_WITH_DERIVED_352_TO_346_NARROWING_NO_RESOLUTION`.

The sealed discovery package passes within its stated scope.  Every requested
headline calculation was independently reconstructed, the complete finite
result sets agree after unsealing, the outer manifest and all ten entries
match, and no discovery theorem was refuted.

One integration qualification is mandatory.  The discovery's `352` rows are
exactly the rows of its explicitly aggregate degree/outside-moment catalog.
Six `x=4` rows contain an opposite-degree-four star on one sign.  Combining
the already verified selected-line equations with that catalog forces every
support point to have opposite degree at most three, so those six rows fail.
Thus `346` aggregate profiles pass this additional necessary cap.  This is a
new verifier derivation, not part of the sealed discovery result, and remains
`DERIVED` until another verifier promotes it.  It is not a graph census.

Global status remains:

```text
Conway-99:                    UNKNOWN
rank-11 endpoint:             UNKNOWN
n3=4158 endpoint:             UNKNOWN
rank-four survivors:          NOT EXCLUDED HERE
99-vertex graph/certificate:  NONE
nonexistence certificate:     NONE
```

## Claim matrix

| Claim | Independent result | Post-source comparison | Status |
|---|---:|---|---|
| `(R-3K)alpha` kills all four matched `q=0` crosses | 13,728 labelled marked/mask cases | Same coordinate conclusion | `VERIFIED` |
| Weight 14 forces `x=1` | independent wedge/triangle-parity route | Same endpoint as source marked-intersection route | `VERIFIED` |
| Unique rooted sign-side graph | 180 labelled graphs, one rooted type | Canonical edge set equal | `VERIFIED` |
| Outside signature | `(17,61,7)` | Equal | `VERIFIED` |
| Deficit bijections | `4480/5040` | Count and complete residual-profile distribution equal | `VERIFIED` |
| Weight-14 marked lines | `204/792` | Complete accepted labelled set equal | `VERIFIED` |
| Weight-20 `x=0` exclusion | all 66 labelled lower-bound certificates | Per-labelled bound equal to source DP | `VERIFIED` |
| Weight-20 `x=2` cases | six swapped-disjoint labelled pairs | Complete set equal | `VERIFIED` |
| Weight-20 `x=10` exclusion | outside pair lower bound `11 > 10` | Same empty aggregate shell | `VERIFIED` |
| Weight-20 aggregate table | `109+157+76+10=352` | Complete 352-row set equal | `VERIFIED`, aggregate only |
| Selected-line cap applied to aggregate table | six `x=4` rows removed; 346 remain | New post-source coupling | `DERIVED` |
| Line-vector identities and norm feasibility | symbolic identities plus exact line-type witnesses | Source witnesses replay independently | `VERIFIED`, necessary only |

## Source-blind reconstruction

Before opening the discovery package, the verifier froze
`protocol.md` and wrote a standard-library checker.  Discovery code is never
imported by `independent_rank3.py`.  The independent archive includes every
accepted weight-14 marked subset and every one of the 352 weight-20 aggregate
rows, not only the headline counts.

### Selected-line row identity

For a disjoint pair of selected triangles, `lambda=1` makes its cross graph a
matching, so a polar residue `0,1,2` permits exact cross size `0 or 3`, `1`, or
`2`, respectively.  An actual selected intersection has `(R,K)=(4,1)` and
therefore the same `R-3K=1` contribution as a disjoint product-one pair.

Writing `h_i` for whether the matched product-zero pair has cross size three,
the eight coordinates reconstruct as

```text
(R-3K)alpha = (-3h0,-3h1,-3h2,-3h3,3h0,3h1,3h2,3h3).
```

Hence every `h_i=0`.  This was checked for all 858 labelled weight-14/20
marked subsets times all 16 matched-cross masks, without an automorphism
quotient.

### Weight 14

If `x=e(P,N)`, same-sign wedge capacity leaves `x in {1,3}`.  In the `x=3`
equality row the cross graph is a three-edge matching and the same-sign degree
sequence is `(4,4,4,3,3,3,3)`.  Zero vertices supply no same-sign pair common
neighbors, and no opposite support vertex sees two same-sign vertices.  Every
same-sign internal edge would therefore lie in an internal triangle, forcing
all internal degrees even, a contradiction.  This independent route reaches
`x=1`; the sealed source instead exhausts all 792 marked subsets against its
exact `t<=1` intersection obstruction and also gets zero `x=3` cases.

With `x=1`, either sign has rooted degrees `(4,3,3,3,3,3,3)`.  A complete
labelled cap census has 180 graphs and one rooted isomorphism type:

```text
01 02 03 04 12 15 26 34 35 46 56.
```

Its seven unit deficit pairs are

```text
14 15 23 26 35 46 56.
```

The deficit graph is triangle-free, so an outside zero vertex has at most two
neighbors of either sign.  Exact first and two-star moments then give
`(z0,z1,z2)=(17,61,7)`.  The seven type-two vertices biject the two labelled
deficit-edge sets.  Directly checking all `7!=5040` bijections retains 4480;
the full residual-value profile distribution also equals the source output.

The independent rooted block-packing pass checks all `C(12,5)=792` labelled
marked subsets and retains 204.  Its accepted-set SHA-256 is
`d16cbf04d03f4637be24f80bcdeb31a122cc13b9a890439fca4a17c9c022f967`,
identical post-source.  No retained marked subset is asserted realizable.

### Weight 20

Parity, the support bound, and exact moments give the initial domain
`x in {0,2,4,6,8,10}`.  The independent selected-union coefficient
certificates reproduce the source dynamic program on every one of the 66
labelled two-intersection subsets:

```text
shared endpoint:       24 subsets with raw lower bound 5;
swapped disjoint:       6 subsets with raw lower bound 2;
other disjoint:        24 with lower bound 3, 12 with lower bound 4.
```

Thus `x=0` is impossible and `x=2` leaves precisely the six labelled pairs
`{(i,j),(j,i)}`.  At `x=10`, 90 positive incidences on 79 outside vertices
force at least 11 outside same-sign pairs, while the exact wedge equation
allows at most 10, so `x=10` is impossible.

The clean-room degree-histogram, Gale--Ryser, and outside-moment enumeration
then gives

```text
x=2: 109
x=4: 157
x=6:  76
x=8:  10
total: 352.
```

The complete independent and source sets agree, not only the distribution.
The representation-independent set SHA-256 is
`c66c3757432fdda2180d4a45f66125314b8ebf2272a2f6d5b35bec3200f2ecc4`.

#### Six-row scope narrowing

Every nonzero coordinate is a singleton point on one selected line.  A
positive point on line `P_i` cannot meet a negative support point on matched
line `N_i`, because that selected-pair cross count is zero.  For each of the
other three negative selected lines, an intersecting pair has no remaining
support-support cross edge and a disjoint product-one pair has total cross
count one.  Therefore its opposite support degree is at most three.

Exactly six aggregate rows violate this cap.  They are the three possible
outside histograms paired with

```text
one sign:   [9,0,0,0,1,0]   (one degree-four support point)
other sign: [6,4,0,0,0,0]   (four degree-one support points),
```

and their sign reversals.  All occur at `x=4`.  Their exact list is stored in
`post-source-audit.json`.  Removing them leaves 346 aggregate profiles not
excluded by this one added cap; further selected-line/outside coupling can
remove more, and none of the 346 is a graph.

## Line-vector audit

For `tau=B^T c` and `C=B^T B-3I`, the verifier independently derives

```text
B tau=10c,  C tau=7tau,  sum(tau)=0,  ||tau||^2=20k.
```

If selected line `i` has intersection degree `d_i`, then
`tau_i=alpha_i(3-d_i)` and the selected norm is
`72-12m+sum d_i^2`.  This reproduces the source splits `30/32/34` versus
`110/108/106` at weight 14, and `52+148` or `54+146` at weight 20.  Both
source line-type witnesses pass independent point-, edge-, and line-moment
checks.  These are necessary integer tables; neither package supplies a
231-line intersection realization or an actual integral `7`-eigenvector on
the line graph.

## Manifest and test replay

The communicated discovery-manifest SHA-256 was reproduced exactly:

```text
521c7ba3e0b34a563f30cc6251c053fe250beb000ff0a808d57fc0a6dcec5ff1
```

All ten entries matched before any source file was opened.  After source
inspection:

```text
discovery exact archive replay:  PASS
discovery unit tests:            11/11 PASS
independent hostile tests:        9/9 PASS
post-source delta tests:          6/6 PASS
Python compilation:               PASS
full k=7 aggregate set:            5/5 equal
full k=10 aggregate set:         425/425 equal
weight-14 marked set:            204/204 equal
weight-20 retained aggregate:    352/352 equal
all labelled m=2 lower bounds:    66/66 equal
```

The source tests check the important headlines, but they do not compare the
complete aggregate/marked sets, inject nonzero matched crosses
coordinatewise, or couple the aggregate rows to the degree-three
selected-line cap.  The verifier suite adds those attacks.

## Input-delta and source-contact record

The blind freeze read the public Wave 208 integration audit at SHA-256
`61b3279f9c48cf3b72755ce047cdb8b30a3125596452c7fa5ff72bd8ed3548e8`.
A concurrent correction changed it to
`eb46057b18ce4d0c0f4c1bd2b4377509c0392194c5cbaa04cd765151bcc3c754`
after the verifier protocol was written.  The original freeze is preserved,
and the corrected bytes are separately pinned in `post-freeze-inputs.sha256`;
`upstream-delta.md` records the substantive documentation change.

One post-freeze terminology search accidentally returned one line from the
sealed agent report saying that an imported `x=6` local control remained.
No discovery formula, table, code, or result set was exposed, and the same
control was already in the public Wave 208 replay surface.  The event is
retained in `source-contact-log.md`; it does not alter the independent result
sets, but the audit does not hide it.

## Frozen boundary

The rooted graph, deficit pairings, marked subsets, aggregate rows, and line
tables omit outside adjacency, outside-outside common-neighbor equations, and
most of the 231-line intersection structure.  A one-row hostile extension
can preserve every internal signed equation while giving a new zero vertex
nonzero dot product with `c`.  Therefore no local or aggregate result implies
the omitted outside equations.

No target automorphism was assumed.  No restricted non-hit was promoted.  No
rank-four branch was touched.  The rank-three branch and every global endpoint
remain `UNKNOWN`.
