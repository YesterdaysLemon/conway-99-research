# Wave 206 fresh integration audit

## Verdict

`VERIFIED_WITH_SCOPE_AND_STRENGTHENING`.

The source-blind fixed-middle tensor derivation, the released hostile and
literature package, Proof A, Proof B, and the later tensor-weight addendum
all survive independent exact checks within their stated scopes.

The strongest newly verified conditional conclusion is:

```text
A_Delta
 = im(B^T) intersect ker(a |-> D diag(a) D)
is nonzero;

every nonzero a in A_Delta is nonconstant,
has wt(a)>=8,
has R_0=R_1=R_2 for its three coefficient classes,
and pulls back to a true projector relation lying in every
ker(Tau^(y)) and in ker(Gamma).
```

If `wt(a)=8`, its eight supported columns span dimension four and the
number of coefficient-two entries is even.

No endpoint exclusion follows.  The rank-11 endpoint, `n3=4158`,
`Q>=7060`, the actual nonedge fourth trace, external novelty, and Conway-99
all remain `UNKNOWN` or `NOT PROVED` as appropriate.

```yaml
role: verifier
date_utc: 2026-07-29T22:13:39Z
git_commit: 85e705cc6c2a14d123120c93a847e30aaab1789e
claim_label: VERIFIED
scope: >-
  Fresh source-blind and post-release verification of Wave 206 fixed-middle
  tensors, hostile controls, root-relative Proof A modules, crossing and
  Gamma identities, the true-kernel intersection code, and the tensor-weight
  addendum, all conditional on the prism-free n3=4158 centered rank-11
  endpoint where stated.
inputs:
  verification/wave206-three-center-global-extension-verifier/SOURCE_BLIND_FREEZE.sha256: f878441cf73e9087596f82b1600cbffb9f22659ee10f438825161ac28246adac
  attempts/wave206-three-center-hostile-controls/package-manifest.sha256: 775582984a530671acf0d0c08eef80ed8bb2242aad79901ba05c0132b06ae47a
  attempts/wave206-three-center-proof-a/package-manifest.sha256: 7a146cd8cae29246cff81b7614fa02f673927514f220218be2860b73554a39fb
  attempts/wave206-crossing-kernel-proof-b/package-manifest.sha256: 6c7718de1c5f2c7d4203d1727d6b74214e51fa069608f318c8583b07b0325f0a
  attempts/wave206-tensor-balance-weight-proof-b/package-manifest.sha256: a2d0b2e23b108e373616f5d5316612053768118435c11a0a2ed4f6520a9b8f25
  verification/wave174-no-weight3-dual/package-manifest.sha256: ac34c8a3b045bec70e3a2080cb4365c0ea43cc732b313ecb3cec355a28f23450
  agents/2026-07-29-wave191-global-star-module-proof-b.md: afe7d35627ec14a9599b427bcca0751e86a3f32b71fb7baf4d91e9e2e335f75f
method: >-
  Source-blind finite-field derivation sealed before discovery release;
  independent post-source matrix and combinatorial implementations; manifest
  verification; exact replay; primary-source scope checks; hostile mutations;
  coefficient-space Witt and projective-cap analysis; and a separately
  reconstructed weight-eight relaxed control.
command: >-
  python -B -m unittest
  verification/wave206-three-center-global-extension-verifier/test_independent_verifier.py
  verification/wave206-three-center-global-extension-verifier/test_post_source_hostile_audit.py
  verification/wave206-three-center-global-extension-verifier/test_post_source_proof_a_audit.py
  verification/wave206-three-center-global-extension-verifier/test_post_source_proof_b_audit.py
outputs:
  verification/wave206-three-center-global-extension-verifier/post_source_hostile_audit.py: 69a30b2d9931876e4e32057a640494b52d0c0934c16e78be7d426276affcfcd8
  verification/wave206-three-center-global-extension-verifier/post_source_hostile_result.json: 9dbb69a8ca45d50e102cb7ab248aaf137b313c2c5eac23de296c4d5bb3f1369b
  verification/wave206-three-center-global-extension-verifier/post_source_proof_a_audit.py: 3a55d3a1ecec12127cc899fd3fa21492680690d9483ac88770c79e9403f4c89f
  verification/wave206-three-center-global-extension-verifier/post_source_proof_a_result.json: ab69e2e2965b440047400ae6162ac7c1fb9c0a34970f6fc6ec6a54357e86a3ad
  verification/wave206-three-center-global-extension-verifier/post_source_proof_b_audit.py: 569a82a13e7a0633c36b027903f8543e0fee488a35f1bb48098cfbc899acb669
  verification/wave206-three-center-global-extension-verifier/post_source_proof_b_result.json: 67ff2d753564e17858a5463d7883ae405290310565147463c26fe8a37d17c4c2
limitations:
  - Every target theorem remains conditional on a putative prism-free rank-11 endpoint.
  - The relaxed controls are not endpoint constructions.
  - Trace-class difference nullities are Gram nullities unless a restricted radical is controlled.
  - Proof A does not impose the x-z pair module, shared 231-column completion, or t>=8 graph modules.
  - The weight-eight control has no target incidence or membership in im(B^T).
  - No rank-11 exclusion, strict n3 improvement, Q>=7060 proof, graph construction, or Conway-99 resolution follows.
```

## 1. Source-blind freeze

Before any Wave 206 discovery source was released, the verifier froze four
files under manifest

```text
f878441cf73e9087596f82b1600cbffb9f22659ee10f438825161ac28246adac.
```

Their hashes still match exactly after the post-source work.

The blind implementation independently established:

- fixed-middle symmetry, diagonal, marked-row, and contraction identities;
- the trace-Gram interpretation on the 21-dimensional self-adjoint
  six-space;
- the seven-star 21-coordinate reconstruction;
- nondegeneracy of the ambient 21-coordinate trace metric;
- the dimension-20 trace-zero hyperplane, restricted rank 19, and radical
  `span(I_6)`; and
- the required guard that isotropic does not mean ambient radical and that a
  restricted Gram kernel need not be a true operator kernel.

The blind suite passes `10/10`.

## 2. Hostile controls and literature

The hostile package manifest and every entry match.  Independent code,
without importing discovery Python, reproduces:

- two 99-label realizations with identical complete labelled `g` and `H`;
- different `tau` on exactly `209,952` ordered entries, supported on the six
  permutations of the three component types;
- a `99 x 231` degree-`7/3` incidence, rank-11 square-zero centered Gram,
  singular columns, star-projector coupling, and zero global frame;
- fixed-middle rank-21 controls in both independent projector windows; and
- rejection of reflection-root, simplex, and incidence-orbit mutations.

This verifies only the scoped negative result:

```text
the checked relaxed shared-incidence, rank-11, zero-frame,
star-projector, complete-g, and complete-H premises
do not determine tau.
```

It is not an endpoint counterexample.  The point graph is disconnected
with component sizes `27,36,36`, has `1,098` extra triangles, lacks uniform
`lambda=1` and `mu=2`, and uses only 19 projective directions with
multiplicities `9^5,12^12,21^2`.

The seven-entry literature ledger retains the needed frame/spanning,
positive-weight, design/annihilator, association-scheme, actual-graph, and
basepoint hypotheses.  Its bounded non-discovery claim remains `UNKNOWN`.

The independent hostile suite passes `8/8`; the submitted suite passes
`7/7`, and the sealed exact result replays.

## 3. Proof A

The independent audit reproduces:

```text
labelled degree-two edge modules: 67,950
unique compressions:              130

(rank,g,h) profile:
  (3,0,0): 15
  (4,0,0): 60
  (4,0,1): 45
  (6,0,0): 10
```

For marked low `t`, it reproduces:

```text
t=6: normalized 646, admissible 18, all (h,r)=(1,1)
t=7: normalized 7,886, admissible 765
     (h,r) counts 288,9,144,180,144 in the sealed five classes.
```

The root-neighbor module partitions the 84 nonneighbors into 21 four-point
fibres, with only the two opposite diagonals allowed inside a fibre; any
forbidden same-endpoint edge forces an induced triangular prism.

Every one-entry edge and nonedge marginal module admits all residues
`0,1,2`.  The 97-entry scalar ledgers satisfy their contractions, but they
do not share a common operator completion.

Accordingly, the following remain explicit vetoes:

```text
x-z pair module imposed:                         NO
shared 231-column realization:                  NO
full labelled three-center graph type -> tau:   UNKNOWN
simultaneous shared operator completion:        UNKNOWN
t>=8 graph modules:                             UNTESTED
endpoint exclusion:                             NO
```

The independent Proof A suite passes `8/8`; the submitted suite passes
`12/12`, and the sealed exact result replays.

## 4. Proof B: localizers, crossing feature, and Gamma

The off-diagonal star coordinates satisfy

```text
J_star=C^T C+2I_21,
rank(J_star)=21,
m_x^(y)[i,j]=M_x[T_i,T_j]= -<z_i,P_x z_j>,
g_xy=sum_e m_x^(y)[e],
tau_(xy;z)=m_x^(y)^T J_star m_z^(y),
h_xy=m_x^(y)^T J_star m_x^(y).
```

The sign in the `g` formula is correct because `m=-r` and
`tr(A)=2 sum r=-sum r` over `F_3`.

For

```text
M_x=D S_x D=-Z^*P_xZ,
W[(T,U),x]=M_x[T,U],
Q=B^TB,
```

the independently checked identities are

```text
rank(M_x)=6,
D M_x=M_x D=M_x M_y=0,
sum_x M_x=0,
rank(W)=dim span{P_x}<=65,
W1=0,
W^T W=0,
(WW^T)^2=0,

Gamma=W^T diag(vec Q) W
     =sum_y Tau^(y),
diag(Gamma)=H1,
Gamma1=0,
rank(Gamma)<=65.
```

A fresh 24-center, 168-column zero-frame control, built without discovery
constructors, has synthesis rank 11, `rank(W)=12`, and `rank(Gamma)=10`.
It checks 576 localizer sign instances and the full nonzero Gamma identity.
It remains a disjoint degree-one-star algebra control, not an endpoint.

The target `Q` mask follows from the actual incidence: its diagonal is
three, hence zero in `F_3`; distinct triangle pairs contribute one exactly
when they share a point.  Therefore summing the 99 star selectors gives
the same mask and proves `Gamma=sum_y Tau^(y)` without dropping or
double-counting diagonal terms.

## 5. The true-kernel intersection code

Let

```text
phi(c)=B^T c,
L=ker(phi),
P(c)=sum_x c_x P_x,
K_P=ker(P),
T(a)=sum_T a_T(z_T tensor z_T).
```

The star-projector relation gives

```text
P(c)=-T(phi(c)),
L subset K_P.
```

All `P_x` lie in the 65-dimensional trace-zero self-adjoint space, so

```text
dim K_P>=99-65=34.
```

Wave 191 gives `17<=dim L<=33`, equivalently `66<=rank(B)<=82`.
Hence `K_P/L` is nonzero.

For

```text
Theta(a)=D diag(a)D=Z^*T(a)Z,
```

the outer map is injective: full row rank of `Z` gives a right inverse `R`,
and

```text
R^*(Z^* A Z)R=A.
```

Thus `Theta(a)=0` if and only if `T(a)=0`, and `phi` induces

```text
K_P/L isomorphic to A_Delta,
dim A_Delta=rank(B)-dim span{P_x}>=1.
```

This is a genuine operator-kernel argument.  No trace-Gram null vector is
used in the transition.

The nonconstant proof is also exact.  If `B^T c=lambda 1` with
`lambda!=0`, block summation gives `sum c=0`; meanwhile

```text
Gc=lambda 1,
G1=0,
G^2=G-J
```

simultaneously force `G^2c=0` and `G^2c=lambda 1`, a contradiction.
Therefore

```text
im(B^T) intersect span(1)={0}.
```

Writing `R_j` for the rank-one tensor sum over coefficient class `j`,
the tensor relation and global zero frame give

```text
R_1+2R_2=0,
R_0+R_1+R_2=0,
```

so `R_0=R_1=R_2`.  This is equality of operator sums, not equality of class
sizes.

Finally, if `c in K_P`, then

```text
(Tau^(y)c)_x
 =tr(P_x P_y (sum_z c_z P_z) P_y)
 =0.
```

Hence `K_P` lies in every true fixed-middle kernel and, because
`Gamma=sum_y Tau^(y)`, in `ker(Gamma)`.

## 6. Strengthened support bound and sharp local boundary

This verifier derived the strengthening before the addendum source was
released.  The later sealed addendum matches the independent derivation and
control.

For a nonzero tensor relation of support size `k`, let `V` contain the
supported columns and `Lambda=diag(a_i)`.  The operator equation is

```text
V Lambda V^T F=0.
```

The ambient form `F` is invertible, so `V Lambda V^T=0`.  Every supported
coefficient is one or two, hence `Lambda` is nondegenerate.  The row space
of `V` is totally isotropic in this coefficient space:

```text
rank(V)<=floor(k/2).
```

The independently verified Wave 174 theorem `d(W^perp)>=4` means that no
three original centered columns are dependent.  Exact exhaustion gives
projective cap maxima

```text
vector rank:  1  2  3
cap maximum:  1  2  4
```

with 234 maximum four-point caps in `PG(2,3)`.  For every `k<=7`, the Witt
rank bound places the support in rank at most three and the corresponding
cap maximum is smaller than `k`.  Therefore

```text
wt(a)>=8.
```

At equality, the cap condition forces `rank(V)>=4`, while the Witt bound
forces `rank(V)<=4`.  Thus `rank(V)=4`, `Lambda` is split, and its number of
coefficient-two entries is even.

The independently replayed eight-column control has:

```text
support size 8,
rank(V)=4,
every three columns independent,
V Lambda V^T=0,
all columns singular,
a nondegenerate nonsquare ambient 11-form,
and zero rank-one operator sum.
```

It has no 231-column frame, point-triangle incidence, graph, or demonstrated
membership in `im(B^T)`.  It proves only that these local ingredients cannot
raise the bound to nine; it does not produce a target weight-eight word.

The addendum manifest and all 11 entries match.  Its exact result replays,
its submitted suite passes `11/11`, and the independent Proof B suite
passes `11/11`.  The original crossing-kernel package remains unchanged.

## 7. Final status wall

```text
source-blind fixed-middle algebra:                         VERIFIED
relaxed complete-(g,H)-does-not-determine-tau result:      VERIFIED_SCOPED
Proof A edge/fibre/low-t/root-relative module censuses:    VERIFIED_SCOPED
21-coordinate localizer and W/Gamma identities:           VERIFIED
A_Delta nonzero/nonconstant and class-balanced:            VERIFIED
A_Delta common true-kernel consequence:                    VERIFIED
every nonzero A_Delta word has weight at least 8:          VERIFIED
weight-eight parity and relaxed local boundary control:    VERIFIED_SCOPED

Proof A full labelled graph-type determination of tau:     UNKNOWN
trace-class Gram nullities are true operator relations:    NO
actual target weight-eight word constructed:               NO
weight at least 9:                                         NOT PROVED
rank-11 endpoint excluded:                                 NO
n3 improved below 4158:                                    NO
Q>=7060:                                                   NOT PROVED
actual nonedge h:                                           UNKNOWN
external novelty:                                          UNKNOWN
Conway-99:                                                  UNKNOWN
```
