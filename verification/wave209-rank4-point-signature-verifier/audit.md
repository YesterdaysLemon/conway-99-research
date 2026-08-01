# Independent audit: Wave 209 rank-four point-signature package

## Verdict

`PASS_NO_VETO` for the exact conditional reduction in the sealed package.
The verifier promotes the checked reduction to `VERIFIED`; the target,
rank-11 endpoint, and every surviving rank-four branch remain `UNKNOWN`.

The source manifest SHA-256 is
`2486affc14226e35542fac320216043c60bb881736af277bd19cabf8623d2a1b`.
All twelve entries in that manifest and all five separately frozen inputs
match their recorded bytes.

## Separation and reconstruction

No discovery module is imported.  Before auditing `exact_check.py`, the
verifier reconstructed the incidence identities directly from

```text
A^2=12I-A+2J,       BB^T=A+7I,       Aq=-4q,       q.q=56.
```

For `t=B^Tq` and `C=B^TB-3I`, these give

```text
t.t=q^T(A+7I)q=168,
Bt=(A+7I)q=3q,
Ct=0,
sum(t)=7 sum(q)=0.
```

The eight marked coordinates are `t_i=-3 alpha_i`, so their norm is 72
and their sum is zero.  The other 223 coordinates therefore have norm 96
and sum zero.

The three form matrices were not copied from discovery code.  They were
recovered by computing the three-dimensional space of symmetric forms over
`F_3` vanishing on the eight published M7g columns, enumerating all 27
forms, and selecting the three labels `(0,0,1)`, `(0,1,0)`, `(1,0,0)`.
Independent marked-subset enumeration recovered exactly 83 labelled
subsets for each form.

## Projector and parity checks

Let `F=B^T(A-3I)B`.  On triangle space its eigenvalues are `231`, `0`, and
`-21`, and the projector onto the zero eigenspace of `C` is

```text
P_0=(J-F)/21.
```

For every selected form, the independently reconstructed matrix
`21 P_0[S,S]` has exact eigenvalue multiplicities

```text
1^1, 3^4, 5^2, 9^1,
```

with `alpha` in the 9-eigenspace.  For marked values `b=-3 alpha`, direct
rational inversion gives `P_0[S,S]^{-1}b=-7 alpha` and hence

```text
b^T P_0[S,S]^{-1}b=168.
```

This equals the full norm of `t`; the interpolation lower bound is exactly
saturated, and the real zero-eigenvector extension is unique.

The point-space `-4` eigenspace has multiplicity 44, so its projector has
constant diagonal `44/99=4/9`.  Consequently
`q_x^2 <= (4/9)56=224/9<25`, and integral coordinates satisfy
`|q_x|<=4`.

The claimed parity obstruction is immediate and exact.  Every marked sum
`-3 alpha_i` is odd, so `q` cannot be even.  Reducing `Aq=-4q` modulo two
gives `A(q mod 2)=0`, while the marked equations give
`U^T(q mod 2)=1_8`.  Thus division by two and any norm-14 classification
of `q/2` are unavailable.

## Complete labelled branch cover

The verifier enumerated all `S_4 x S_4` sign-preserving label permutations.
For each ordered pair of the three forms, exactly eight permutations
preserve every polar entry.  Acting only by those explicitly checked data
renamings partitions the `3*83=249` nodes into 24 disjoint orbits:

```text
size 3:   1 orbit
size 6:   9 orbits
size 12: 12 orbits
size 24:  2 orbits
```

The union contains all 249 nodes exactly once.  This is an isomorphism of
the finite constraint systems, not an automorphism assumption about a
hypothetical target graph.

## Point-signature equations

For a point `x` and marked triangle `T_i`, define `s_i(x)` as `-1` on the
triangle, `+1` outside it when adjacent to its unique triangle point, and
zero otherwise.  The uniqueness follows from `lambda=1`.  Direct expansion
gives

```text
q_x=(1/3) sum_i alpha_i s_i(x).
```

Exactly 2,187 of the `3^8` signatures make the numerator divisible by
three.  Each coordinate has margins `(-1,0,+1)=(3,60,36)`.  The verifier
independently checked every joint table against both margins and the exact
inner product

```text
sum_x s_i(x)s_j(x)=18-7D_ij.
```

Including total count, all one- and two-coordinate cells, `sum(q)=0`, and
`q.q=56` gives 279 linear equations in nonnegative signature counts.

### Exact exclusions

For each of the 17 excluded orbit representatives, the archived sparse
integer vector was expanded against the independently ordered 279 equations.
Over all 2,187 columns it satisfies

```text
A^T y >= 0,       b^T y < 0.
```

Sixteen certificates have pointwise minimum zero; the remaining certificate
has a strictly positive integer minimum.  All right-hand sides are strictly
negative.  The verifier then transported the equation names, including the
orientation swap required when a pair is relabelled in reverse order, and
recomputed both inequalities for every labelled target.  This performs 198
explicit labelled exclusion checks, not merely 17 representative checks.

No solver status is used.  Negating a dual vector fails the required
orientation, and erasing it fails the strict right-hand-side inequality;
both hostile mutations are rejected.

### Exact surviving controls

The other seven orbits contain 51 labelled branches.  Every archived
nonnegative integer table was decoded into its 99 rows and checked against
all 279 equations.  Each table was then transported and rechecked on every
labelled target.  This contributes 51 explicit labelled control checks.
A one-count mutation is rejected by the total and moment equations.

These controls are exact anonymous joint-signature censuses.  They do not
name graph points, encode adjacency among rows, or prove an eigenvector or
graph exists.

## Triangle-side aggregate controls

The verifier independently rebuilt the 81-word rank-four evaluation code,
all allowed `(d,h,t)` residual types, and all 99 aggregate equations:

* 223 total residual triangles;
* the exact `0^32,1^162,2^36` polar row distribution after removing marked
  entries;
* every selected pair moment from `F^2=-21F+252J`;
* residual `t` sum zero and squared norm 96;
* all eight selected rows of `Ct=0`; and
* every one- and two-way selected intersection count.

All 24 archived integer controls satisfy these equations.  Relabelling and
full replay on every target gives 249 explicit aggregate-control checks.  A
one-count hostile mutation is rejected.  These are type counts, not 223
named residual blocks; in particular they do not enforce residual--residual
incidence or the other 223 rows of `Ct=0`.

The separately archived selected-union witnesses were also compared with an
independent componentwise integer minimization.  The minimum norm
distribution over labelled branches is

```text
20^3, 23^24, 24^24, 25^48, 26^72, 32^54, 34^24.
```

All 249 transported marked-line assignments were replayed.  Their norms are
at most 34, but none checks an outside adjacency equation.

## Source audit and hostile testing

The source default path uses only standard-library exact arithmetic and
archived integers.  SciPy/HiGHS appears only behind explicit generation
flags and is not imported or consulted by replay.  The source replay passed
and its nine tests passed.  The independent verifier has six tests covering
the frozen archive, full orbit partition, pair-table margins and inner
products, projector saturation, hostile mutations, and the status wall.

The following hostile changes are all rejected:

* erase an exclusion vector;
* reverse its inequality orientation;
* add one row to a surviving point census; and
* add one residual type to an aggregate census.

## Exact boundary

The 198 labelled exclusions are verified necessary-condition exclusions.
The remaining 51 branches have only census controls.  None of the artifacts
supplies:

1. 99 named points and their adjacency matrix;
2. all rows of `Aq=-4q`;
3. 231 named triangle blocks and a point-star decomposition;
4. the 223 omitted residual rows of `Ct=0`; or
5. all `lambda=1`, `mu=2`, regularity, and prism-free equations.

Therefore the package makes a substantial exact reduction but does not give
a global proof or counterexample.  Conway-99 remains `UNKNOWN`.
