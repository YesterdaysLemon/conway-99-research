# Wave 207 statement and literature audit

```yaml
role: literature
date_utc: 2026-08-01T01:14:19Z
git_commit: c58fd917ea8f9622e1388f10b0e0e3c709ba4854
claim_label: CANDIDATE
scope: >-
  Current-through-2026-07-31 primary-source audit for the conditional
  prism-free n3=4158, rank_F3(D)=11 Conway-99 endpoint, emphasizing ternary
  codes, finite orthogonal geometry, quadratic Veronese configurations,
  Terwilliger/triple regularity, and Conway-99 work appearing after
  2026-04-24. Apply located theorems to the verified Wave 206 weight-eight
  boundary without changing the global UNKNOWN status.
inputs:
  attempts/wave206-three-center-global-extension/protocol.md: 66c20334e284a26cc771ee86d97e678cb67b6efb4648b2af2fffe480fb5a9103
  attempts/wave206-crossing-kernel-proof-b/derivation.md: 9bdc0a296f704a5bd73ffa3a726694b74454b011dac486da9afa599f868aab13
  attempts/wave206-tensor-balance-weight-proof-b/derivation.md: 7d13a1834819e952c4d4eff033fac033e23699ab643d9852318a67d19bcb6cf2
  verification/wave206-three-center-global-extension-verifier/audit.md: b1524bf3c923d5e52cb28c6899774130b3c1a9467cfb6d54a2de014d8b555a3e
  attempts/wave206-three-center-hostile-controls/literature-audit.md: 9a41f0b69cdf54d2a01f8f02fdbdf5ca6068248442126fc927399037e3518661
  attempts/wave205-global-fourth-moment-proof-b/derivation.md: 28ad3e3d2bd324e9b7cf5c2d2a7284aa938436f1477c1165ecc948b1edf222c4
  agents/2026-07-22-wave2-algebra-codes.md: 999cbb0366a984ab6ddf4a2ff084eb680beffaad47c0b8176752a5a6769cc0e9
method: >-
  Freeze the exact conditional claim; search primary and publisher sources;
  check every theorem's hypotheses against the target; apply the published
  classification of rank-seven quadratic-Veronese configurations over F3;
  derive the Terwilliger obstruction and clique-graph specializations by
  exact parameter arithmetic; and run small exhaustive F3 checks only on a
  published M7g representative. No automorphism was assumed.
command: >-
  rg -n "A_Delta|BD=0|rank.*D|rank.*Z|tensor|weight.?8|UNKNOWN"
  attempts verification agents ; python - (the two complete finite-field
  snippets and their outputs are reproduced in Sections 3 and 5 below) ;
  web queries and source cutoff are recorded in Section 9.
outputs: {}
limitations:
  - The report itself is the sole output, so its self-hash must be recorded externally after writing.
  - The new M7g application and exact representative checks are DERIVED/CANDIDATE until independently replayed.
  - A bounded literature non-hit is not evidence that no relevant theorem exists.
  - No actual weight-eight A_Delta word, graph, endpoint exclusion, or strict n3 improvement is produced.
  - The prism-free rank-11 branch and Conway-99 existence both remain UNKNOWN.
```

## 1. Frozen statement and safe verdict

Work over `F_3`.  On the frozen Wave 206 branch, assume a putative graph

```text
G is srg(99,14,1,2),
n3=4158 (equivalently, the induced triangular-prism count is zero),
rank(D)=11.
```

Let `B` be the `99 x 231` vertex--triangle incidence matrix, let `Z` have
the 231 centered triangle columns `z_T`, and let

```text
D=Z^*Z,
A_Delta=im(B^T) intersection ker(a |-> D diag(a) D).
```

The independently verified Wave 206 conclusion used here is

```text
A_Delta is nonzero;
every nonzero a in A_Delta has wt(a)>=8;
sum_T a_T (z_T tensor z_T)=0;
the three coefficient-class tensor sums are equal;
if wt(a)=8, the support is an eight-cap of vector rank four and the
number of coefficient-2 entries is even.
```

The strongest safe result of this audit is a sharper conditional description:

> **CANDIDATE reduction.** If `a in A_Delta` has weight eight, its support is
> projectively equivalent to the `M7g` configuration classified by Kaipa and
> Pradhan.  Thus its eight points occur in four pairs on four lines concurrent
> at an external point, with no three of the four lines coplanar, and its
> coefficient composition is exactly four `1`'s and four `2`'s.  The additional
> incidence condition forces both `Da=0` and `Za=0`, leaving four relative
> projective-sign classes for a verifier to test against the 231-column frame.

This is a finite geometric narrowing, not an existence or nonexistence proof.
No primary source located through the stated cutoff claims a solution of the
Conway-99 problem.  The global status remains `UNKNOWN`.

| Item | Label | Consequence |
|---|---:|---|
| Kaipa--Pradhan rank-seven classification | `CITED` | Seven maximal quadratic closures in `PG(3,3)` |
| Weight-eight support must be `M7g` | `DERIVED`, pending replay | Unique surviving closure under the cap condition |
| Coefficient composition is `4+4` | `DERIVED`, pending replay | Strengthens Wave 206's even-parity conclusion |
| `a in im(B^T)` implies `Da=Za=0` | `DERIVED` | Adds a true linear relation to the Veronese relation |
| `Za=0` excludes `M7g` | `REFUTED` | Four relative sign classes survive |
| Target is triply regular | `REFUTED` | Its 84-vertex second subconstituent cannot be strongly regular |
| Ternary adjacency-code minimum distance is 24 | `UNKNOWN` | Weight-24 words exist; no matching lower-bound theorem was located |
| Conway-99 existence | `UNKNOWN` | No status promotion |

## 2. Primary geometric source: rank-seven quadratic Veronese configurations

The decisive source is Krishna Kaipa and Puspendu Pradhan,
[Higher weight spectra of ternary codes associated to the quadratic Veronese
3-fold](https://arxiv.org/abs/2405.12011), published in *Journal of Algebra
and Its Applications* 24 (13--14), 2541007 (2025),
[DOI 10.1142/S0219498825410075](https://doi.org/10.1142/S0219498825410075).
The paper studies the quadratic Veronese embedding

```text
iota: PG(3,3) -> PG(9,3).
```

Its terminology is exactly suited to the Wave 206 boundary:

- Definition 3.2 defines the rank of a point configuration as the rank of its
  quadratic-Veronese columns.
- Lemma 3.3 proves that every rank-`r` configuration `S` lies in a unique
  maximal rank-`r` configuration
  `Sbar=V(I_2(S))`.
- Lemma 6.1 classifies all maximal rank-seven configurations in `PG(3,3)`
  into seven classes `M7a,...,M7g`.
- Section 6.1 confirms that `M7g` has eight points and contributes
  `B_(8,7)(M7g)=1`.

The seven closures and the cap obstruction are as follows.  Here “cap maximum”
means the largest no-three-collinear subset that the displayed closure can
contain; the bounds are immediate from the source's geometric descriptions.

| Closure | Source description | Cap maximum relevant here |
|---|---|---:|
| `M7a` | a plane and one external point | `4+1=5` |
| `M7b` | three concurrent noncoplanar lines | at most `6` |
| `M7c` | three lines, one meeting two skew lines | at most `6` |
| `M7d` | two intersecting lines and two external points | at most `6` |
| `M7e` | four general-position points and a full line | at most `4+2=6` |
| `M7f` | a seven-point configuration | `7` points total |
| `M7g` | eight points paired on four externally concurrent lines, no three lines coplanar | `8` |

No assumption about a graph automorphism enters this classification or its
application.

## 3. Application to a Wave 206 weight-eight word

Let `S=supp(a)` for a hypothetical weight-eight `a in A_Delta`.  Wave 206
already proves that the original columns in `S` form an eight-cap spanning a
four-dimensional vector space.  Identify that span with `F_3^4` and hence its
projectivization with `PG(3,3)`.

The tensor equation says that the eight quadratic-Veronese columns are
dependent, so their Veronese rank is at most seven.  It is exactly seven:
if their rank were at most six, their relation space would have dimension at
least two.  Combining two independent relations to cancel any chosen
coordinate would give a nonzero quadratic-tensor relation supported on at
most seven of the cap points.  The universal Wave 206 Witt-plus-cap argument
excludes every such relation.  Therefore

```text
rank(iota(S))=7.
```

By Kaipa--Pradhan Lemma 3.3, `S` lies in a unique `C7` closure.  The cap
maximum column of the table eliminates `M7a` through `M7f`; consequently

```text
Sbar=S is an M7g configuration.
```

One representative used in the source is

```text
P1=e0,                    P2=e0+e3,
P3=e1,                    P4=e1+e3,
P5=e2,                    P6=e2+e3,
P7=e0+e1+e2+e3,           P8=e0+e1+e2-e3.
```

An exhaustive check of the `2^8` nonzero coefficient vectors gives only one
projective quadratic relation:

```text
(1,2,1,2,1,2,2,1)
```

and its scalar multiple.  Hence every target weight-eight word has exactly
four coefficients of each nonzero symbol.  This is invariant under projective
renormalization because every nonzero scalar in `F_3` squares to one.

The complete exact check used for this claim was:

```powershell
@'
from itertools import product
p=[(1,0,0,0),(1,0,0,1),(0,1,0,0),(0,1,0,1),
   (0,0,1,0),(0,0,1,1),(1,1,1,1),(1,1,1,2)]
mons=[(i,j) for i in range(4) for j in range(i,4)]
qcols=[[v[i]*v[j]%3 for i,j in mons] for v in p]
rels=[]
for a in product((1,2),repeat=8):
    if all(sum(a[t]*qcols[t][m] for t in range(8))%3==0
           for m in range(10)):
        rels.append(a)
print(rels)
'@ | python -
```

Output:

```text
[(1, 2, 1, 2, 1, 2, 2, 1),
 (2, 1, 2, 1, 2, 1, 1, 2)]
```

This calculation is small and exact, but it is a discovery-side check and must
not be labelled `VERIFIED` until independently reconstructed.

## 4. The incidence condition adds a true linear relation

The earlier tensor argument did not use the full condition `a in im(B^T)`.
Write

```text
a=B^T c.
```

The inherited star relation is `BD=0`, and `D` is symmetric.  Therefore

```text
Da=D B^T c=(BD)^T c=0.                         (1)
```

Also `D=Z^*Z`, `rank(D)=11`, and `rank(Z)=11`.  Since `ker(Z)` is contained
in `ker(D)` and the two kernels have the same dimension,

```text
ker(D)=ker(Z),
Za=0.                                           (2)
```

Thus a target weight-eight word is simultaneously

```text
sum_i a_i z_i=0,
sum_i a_i (z_i tensor z_i)=0.
```

This is a genuine strengthening over a generic rank-seven Veronese circuit.
It does **not**, however, exclude `M7g`.  For the representative in Section 3,
the displayed quadratic relation has ordinary vector sum

```text
sum_i a_i P_i=(0,0,0,1),
```

but a projective equivalence only fixes each `P_i` up to an independent sign
`epsilon_i in {1,2}`.  Those signs disappear from the quadratic tensors but
remain in the linear relation.  Exact enumeration finds eight sign patterns,
four modulo a common global sign, for which

```text
sum_i a_i epsilon_i P_i=0.
```

Representatives of the four relative classes are

```text
(1,1,1,1,2,2,1,1)
(1,1,2,2,1,1,1,1)
(1,1,2,2,2,2,2,2)
(1,2,1,2,1,2,1,2).
```

The exhaustive command is the Section 3 snippet with the following lines
appended:

```python
a=rels[0]
signs=[]
for e in product((1,2),repeat=8):
    if all(sum(a[t]*e[t]*p[t][j] for t in range(8))%3==0
           for j in range(4)):
        signs.append(e)
print(len(signs),signs)
```

The resulting target is now finite: an actual weight-eight word must realize
the `M7g` projective orbit, the unique `4+4` tensor circuit, and one of these
four relative-sign classes inside the shared 231-column incidence frame.

## 5. Orthogonal and polar-space compatibility audit

All centered columns are singular in a nonsquare nondegenerate 11-space.  On
the four-space spanned by an `M7g` support, the restricted ambient quadratic
form must therefore lie in the three-dimensional net `I_2(M7g)` of quadrics
through the eight points.

A direct enumeration of the 13 projective members of this net gives

| matrix rank | projective zero count | number in the net |
|---:|---:|---:|
| `2` | `22` | `6` |
| `3` | `13` | `4` |
| `4` | `16` | `3` |

The three rank-four members are hyperbolic quadrics `Q^+(3,3)`, since they
have `(3+1)^2=16` projective singular points.  Hence, if the ambient form is
nondegenerate on the support span, that span is plus type.  A nonzero
degenerate restriction can have rank two or three in this net, and an
identically zero restriction (a totally isotropic four-space) is also possible
a priori.  In every case, the local singularity premise is compatible with
`M7g` and supplies no contradiction.

For reproducibility, the following exact check row-reduces the `8 x 10`
quadratic evaluation matrix, enumerates the 13 one-dimensional subspaces of
its three-dimensional nullspace, converts each quadratic coefficient vector
to its symmetric `4 x 4` matrix, and counts zeros on the 40 projective points
of `PG(3,3)`:

```powershell
@'
from itertools import product
p=[(1,0,0,0),(1,0,0,1),(0,1,0,0),(0,1,0,1),
   (0,0,1,0),(0,0,1,1),(1,1,1,1),(1,1,1,2)]
mons=[(i,j) for i in range(4) for j in range(i,4)]
E=[[v[i]*v[j]%3 for i,j in mons] for v in p]

def rref(A):
    A=[row[:] for row in A]; piv=[]; rr=0
    for c in range(len(A[0])):
        q=next((i for i in range(rr,len(A)) if A[i][c]%3),None)
        if q is None: continue
        A[rr],A[q]=A[q],A[rr]
        inv=1 if A[rr][c]%3==1 else 2
        A[rr]=[(inv*x)%3 for x in A[rr]]
        for i in range(len(A)):
            if i!=rr and A[i][c]%3:
                z=A[i][c]%3
                A[i]=[(A[i][j]-z*A[rr][j])%3
                      for j in range(len(A[0]))]
        piv.append(c); rr+=1
        if rr==len(A): break
    return A,piv

def nullspace(A):
    R,piv=rref(A)
    free=[c for c in range(len(A[0])) if c not in piv]
    out=[]
    for f in free:
        x=[0]*len(A[0]); x[f]=1
        for i,c in enumerate(piv): x[c]=(-R[i][f])%3
        out.append(x)
    return out

basis=nullspace(E)
coeffs=[]
for t in product(range(3),repeat=len(basis)):
    if any(t) and next(x for x in t if x)==1:
        coeffs.append(t)
points=[]
for x in product(range(3),repeat=4):
    if any(x) and next(v for v in x if v)==1:
        points.append(x)
counts={}
for t in coeffs:
    c=[sum(t[k]*basis[k][m] for k in range(len(basis)))%3
       for m in range(10)]
    M=[[0]*4 for _ in range(4)]
    for z,(i,j) in zip(c,mons):
        if i==j: M[i][j]=z
        else: M[i][j]=M[j][i]=2*z%3
    rank=len(rref(M)[1])
    zeros=sum(sum(c[m]*x[i]*x[j]
                  for m,(i,j) in enumerate(mons))%3==0 for x in points)
    counts[(rank,zeros)]=counts.get((rank,zeros),0)+1
print('I2 dimension:',len(basis))
print('projective quadrics by (rank, projective zeros):',counts)
'@ | python -
```

Its exact output was:

```text
I2 dimension: 3
projective quadrics by (rank, projective zeros): {(4, 16): 3, (2, 22): 6, (3, 13): 4}
```

No theorem was located that embeds this local `M7g` net into, or excludes it
from, the full 231-point singular zero-frame.  That missing global incidence
compatibility remains the substantive boundary.

## 6. Ternary incidence and adjacency codes

### 6.1 Steiner-triple-system theorems do not apply

The triangle incidence is a regular partial linear triple system, not a
Steiner triple system or a `2-(99,3,1)` design:

```text
231 blocks, block size 3, point degree 7;
693 adjacent vertex pairs are covered once;
nonadjacent pairs are never covered.
```

An `STS(99)` would instead have `99*98/6=1617` blocks and cover every pair.
Accordingly, J. D. Key's
[Ternary codes of Steiner triple systems](https://doi.org/10.1002/jcd.3180020105)
and later block-code classifications such as Jungnickel--Tonchev,
[On Bonisoli's theorem and the block codes of Steiner triple
systems](https://doi.org/10.1007/s10623-017-0406-9), have a failed hypothesis.
Their Reed--Muller containment and rank conclusions cannot be transferred to
`B` merely because its columns have weight three.

The safe description is a `1-(99,3,7)` packing on the graph edges.

### 6.2 A new point-code bridge at weight eight

The `4+4` coefficient composition implies

```text
sum_T a_T=0 in F_3.
```

For `a=B^T c`, define the 99-coordinate point word

```text
b=B a=B B^T c=(A+I)c.
```

Here `BB^T=A+I` because each vertex is in seven triangles and each adjacent
pair is in its unique triangle.  Also `B 1=7*1=1` over `F_3`, so

```text
sum c=sum a=0.
```

The SRG identity gives `A(A+I)=-J` over `F_3`; hence

```text
Ab=-Jc=0,
b in ker_F3(A),
wt(b)<=24.                                      (3)
```

The support bound is the union bound for the vertices of eight triangles.
The word `b` could be zero; this caveat must be retained.

Equivalently, put `Q=A+I-J`.  Then `AQ=0`, while any `x in ker(A)` also has
`Jx=0` and hence `Qx=x`.  Thus

```text
ker_F3(A)=im(A+I-J),
```

the ternary `[99,54]` code from the verified modular rank `rank_F3(A)=45`.

There are parameter-forced weight-24 words in this code.  If `x~y`, let
`q_x` and `q_y` be the indicator rows of the two closed neighborhoods.  Then

```text
q_x-q_y in ker_F3(A).
```

The two closed neighborhoods have size 15 and intersect in exactly the edge
endpoints and their unique common neighbor, so

```text
wt(q_x-q_y)=2(15-3)=24.                         (4)
```

Consequently `d(ker_F3 A)<=24`.  A bounded search of adjacency-code, strongly
regular graph, neighborhood-design, and exact `[99,54]` literature did not
locate a theorem proving the reverse inequality or classifying equality for
these parameters.  Generic adjacency-code papers give graph-specific or
computational tables, not a parameter-only result for a graph whose existence
is unknown.  The following remains a precise high-value subproblem:

```text
Prove d(ker_F3 A)>=24 and classify all weight-24 words;
in particular, decide whether every such word is a scalar multiple of
q_x-q_y for an edge xy.
```

If established, (3) would force any nonzero `b` from a weight-eight
`A_Delta` word to have weight exactly 24, making its eight triangles
vertex-disjoint and placing `b` in the equality classification.  This is a
route proposal, not a proved consequence.

## 7. Terwilliger algebra and triple regularity: a decisive negative route

The relevant current primary source is Allen Herman, Roghayeh Maleki, and
Andriaherimanana Sarobidy Razafimahatratra,
[On the classification of triply-transitive strongly-regular
graphs](https://arxiv.org/pdf/2507.14320), later published in *Journal of
Algebraic Combinatorics* 63 (2) (2026),
[DOI 10.1007/s10801-026-01526-7](https://doi.org/10.1007/s10801-026-01526-7).
Its Theorem 2.6 states that a strongly regular graph is triply regular exactly
when `T_(0,omega)=T_omega` for some, equivalently every, base vertex.  Theorem
2.7, citing Munemasa Proposition 6, states that triple regularity is equivalent
to all subconstituents at every vertex being strongly regular.

Those hypotheses fail for the target by elementary parameter arithmetic.  At
a vertex `omega`, the first subconstituent is `7K_2`.  The second
subconstituent has 84 vertices and degree 12: every nonneighbor of `omega`
has exactly `mu=2` neighbors in the first subconstituent and therefore 12
neighbors among the other nonneighbors.

If this second subconstituent were `srg(84,12,lambda_2,mu_2)`, feasibility
would require

```text
(84-12-1) mu_2 = 12(12-lambda_2-1),
71 mu_2 = 12(11-lambda_2).
```

Since `0<=lambda_2<=11`, coprimality forces

```text
lambda_2=11,
mu_2=0.
```

It would then be a disjoint union of `K_13` components, impossible because
13 does not divide 84.  Therefore every putative target graph is **not**
triply regular, and

```text
T_(0,omega) is a proper subspace of T_omega for every omega.
```

This does not rule out the graph.  It rules out a tempting proof strategy:
the missing three- or four-center tensor cannot be declared parameter-forced
by invoking triple regularity.  Any Terwilliger continuation must retain the
extra second-subconstituent data explicitly.

## 8. Conway-99 work after the 2026-04-24 SAT cutoff

### 8.1 New archival source: the triangle clique graph

Connor Phillips submitted
[A Comprehensive Study of Clique Graphs and Clique Regular
Graphs](https://arxiv.org/abs/2605.22867) on 2026-05-19.  The thesis explicitly
states that the Conway prize remained unclaimed and develops the graph whose
vertices are the 231 triangles of a putative Conway graph.  Some earlier
chapters overlap Robert Petro and Connor Phillips,
[On clique graphs and clique regular graphs](https://doi.org/10.1016/j.disc.2025.114862),
*Discrete Mathematics* 349 (3), 114862 (March 2026), but the thesis's
triangle-centered `tau,rho` system is the material relevant to this cutoff.

Specializing Phillips's formulas to `srg(99,14,1,2)`, whose spectrum is
`14^1,3^54,(-4)^44`, gives a triangle clique graph `C_3(G)` with

```text
231 vertices,
degree 18,
maximum-clique assembly size 7,
spectrum 18^1, 7^54, 0^44, (-3)^132.
```

Fix a triangle-vertex `v`.  Phillips partitions its nonneighbors into `T_i`,
where a triangle in `T_i` has exactly `i` common clique-graph neighbors with
`v`, and writes `tau_i=|T_i|`.  The target specialization of equation (4.5)
is

```text
tau_0+tau_1+tau_2+tau_3=212,
tau_1+2 tau_2+3 tau_3=216,
tau_2+3 tau_3=36.
```

Thus, with `t=tau_3`,

```text
(tau_0,tau_1,tau_2,tau_3)
  =(32-t, 144+3t, 36-3t, t),
0<=t<=12.                                       (5)
```

Propositions 4.6--4.8 add edge variables `rho_ij` and prove

```text
rho_03=0,
(18-i)tau_i=rho_ii+sum_(j=0)^3 rho_ij,
(18+i(6-5-2))tau_i=i rho_ii+sum_(j=1)^3 j rho_ij.
```

The full system has rank 10 in 13 variables.  Phillips reports nonnegative
integer solutions for every feasible `srg(n,k,1,mu)` parameter tuple tested
up to degree 50 million, so this system alone excludes no candidate.  It is
nevertheless the closest new published graph-level language to the Wave 206
gap: its 231 vertices are the same triangles indexing `B`, `D`, and
`A_Delta`.

The proposed use is to mark the eight triangle-vertices of an `M7g` support
and refine (5) and the `rho` equations by their actual `B`-incidence.  The
four secant lines in `PG(3,3)` are projective-geometric lines, **not**
automatically clique-graph edges; the bridge has to be proved through `B`.

### 8.2 SAT revision and non-archival lead

Ali Keramatipour's
[Approaching the Conway-99 problem using SAT
solvers](https://arxiv.org/abs/2604.23037) was first submitted on 2026-04-24
and revised on 2026-04-28.  Its stated result remains a computational
nonresolution: the encodings did not solve the instance in reasonable time.
It is not a proof or counterexample.

A 2026-06-25 seminar announcement by Sergey Shpectorov and Tianxiao Zhao
describes a complete-enumeration approach for the different parameter set
`srg(85,14,3,2)` and only a
[possible similar approach to `srg(99,14,1,2)`](https://www.hebtu.edu.cn/a/2026/06/24/AD3624B468444197AA2464C61CBDEE63.html).
No paper, certificate, or Conway-99 theorem was attached, so this is recorded
only as a lead.

## 9. Bounded source ledger and evidence boundary

The live audit cutoff was 2026-07-31 in America/Los_Angeles
(2026-08-01 UTC).  Searches included exact-title and exact-parameter variants
of:

```text
"Conway-99" 2026
"srg(99,14,1,2)" 2026
"Conway's 99-graph" 2026
site:arxiv.org/abs/2605 OR 2606 OR 2607 "99-graph"
"adjacency code" strongly regular graph ternary "minimum distance"
"[99,54]" ternary code
quadratic Veronese PG(3,3) rank seven configuration
Terwilliger triple regular strongly regular subconstituents
```

Primary or publisher records actually used were:

1. Kaipa--Pradhan, arXiv:2405.12011 / DOI
   `10.1142/S0219498825410075` -- quadratic-Veronese definitions and complete
   `C7` classification.
2. Herman--Maleki--Razafimahatratra, arXiv:2507.14320 / DOI
   `10.1007/s10801-026-01526-7` -- Theorems 2.6 and 2.7 on triple regularity.
3. Phillips, arXiv:2605.22867 -- post-cutoff clique-graph spectrum and
   `tau,rho` system, plus an explicit contemporary open-status statement.
4. Petro--Phillips, DOI `10.1016/j.disc.2025.114862` -- journal provenance for
   the shared clique-graph material.
5. Keramatipour, arXiv:2604.23037v2 -- 2026-04-28 revision and SAT
   nonresolution.
6. Key, DOI `10.1002/jcd.3180020105`, and Jungnickel--Tonchev, DOI
   `10.1007/s10623-017-0406-9` -- ternary STS code results whose design
   hypothesis fails here.

The bounded search located no primary-source proof, counterexample, exact
`[99,54]` ternary minimum-distance theorem, or polar-space theorem that closes
the marked `M7g` incidence problem.  This sentence reports non-discovery only;
it is not a completeness certificate for the mathematical literature.

## 10. Recommended next symbolic target

The literature-supported next step is narrow enough for two independent proof
agents and a verifier:

```text
Assume a weight-eight a in A_Delta.
Normalize its support to the published M7g representative.
Retain the unique 4+4 tensor circuit and one of four Za=0 sign classes.
Pull the eight marked projective points back to eight triangle columns.
Impose a=B^T c and the induced 99-coordinate word b=B a in ker_F3(A).
Couple the marked triangle set to the C_3(G) tau,rho equations.
Either derive an incidence contradiction or emit a complete symbolic
compatibility certificate.
```

In parallel, the ternary-code lemma

```text
d(ker_F3 A)=24, with equality classified by adjacent closed-neighborhood
differences
```

is a clean standalone target.  Both routes use the actual shared incidence
that the Wave 206 relaxed controls deliberately omitted.  Triple regularity
should not be used, and absence of a compatible placement in any restricted
search must record every restriction rather than be promoted to
nonexistence.

## 11. Final status

```text
published C7 classification:             CITED
weight-eight support is M7g:             DERIVED / pending independent replay
weight-eight composition is 4+4:         DERIVED / pending independent replay
Da=Za=0 incidence strengthening:         DERIVED
Za=0 excludes M7g:                       REFUTED
local polar compatibility:               DERIVED / no contradiction
triple-regular closure route:             REFUTED
ternary [99,54] distance/equality route:  UNKNOWN
rank-11 endpoint:                         UNKNOWN
n3=4158 endpoint:                         UNKNOWN
Conway-99:                                UNKNOWN
```
