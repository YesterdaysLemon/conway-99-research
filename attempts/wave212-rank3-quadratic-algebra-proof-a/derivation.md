# Mod-2 Jordan structure and exact K-projector closure

Claim label: `DERIVED` pending independent verification.

## 1. Artin--Schreier structure over `F_2`

Put `N=F^T F mod 2`.  Exact bit elimination gives, in each of orbits
`0`, `4`, and `29`,

```text
rank(N), rank(N^2), rank(N^3), rank(N^4), rank(N^5)
  = 12,       8,         4,         2,         0.       (1)
```

For a nilpotent matrix, the number of Jordan blocks of size at least `k` is
`rank(N^(k-1))-rank(N^k)`.  Including `rank(N^0)=85`, (1) gives

```text
blocks of size at least 1,2,3,4,5:  73,4,4,2,2,
```

and therefore

```text
N  ~  J_5(0)^2 direct-sum J_3(0)^2 direct-sum J_1(0)^69. (2)
```

If the quadratic block holds, then over `F_2`

```text
D^2+D=N.                                                   (3)
```

Since `N^5=0`, the only primary roots of `D` are `0` and `1`.  On either
primary component write `D=lambda I+T`, with `T` nilpotent.  Then

```text
D^2+D = T+T^2 = T(I+T).
```

The factor `I+T` is invertible and commutes with `T`, so every power
`(T+T^2)^k` has the same rank as `T^k`.  Consequently any completion has
exactly the four nontrivial mod-2 Jordan blocks

```text
J_5, J_5, J_3, J_3,                                      (4)
```

allocated in an as-yet undetermined way between the `0`- and `1`-primary
spaces.  This is stronger than the Wave 211 idempotence statement on
`ker(F)`, but it is consistent.

The conditional rational characteristic polynomial reduces to

```text
chi_D(x) = x^45 (x+1)^40
         = x^85+x^77+x^53+x^45
         = x * (x^22 (x+1)^20)^2              in F_2[x]. (5)
```

For an odd-order symmetric zero-diagonal matrix over `F_2`, the
characteristic polynomial has the form `x` times a square.  Equation (5)
has exactly that form, so the alternating-characteristic-polynomial test
does not exclude any survivor.

## 2. Exact conditional projectors on `K`

Choose any independent row basis `B` of `rowspan(F,1^T)`.  Exact rational
elimination gives

```text
P_U = B^T (B B^T)^(-1) B,       P_K=I-P_U.                (6)
```

Every row of `BD` is forced by the linear block and degrees, hence so is

```text
D P_U = P_U D = B^T (B B^T)^(-1) B D.                    (7)
```

If the quadratic block holds, `D|K` has eigenvalues `3` and `-4`.  Its two
orthogonal projectors are therefore

```text
E_3^K  = (D+4I) P_K / 7,
E_-4^K = (3I-D) P_K / 7.                                  (8)
```

Because `D_ii=0`, (6)--(8) force every diagonal entry without knowing any
off-diagonal entry of `D`:

```text
(E_3^K)_ii  = (-(D P_U)_ii + 4(P_K)_ii)/7,
(E_-4^K)_ii = ( (D P_U)_ii + 3(P_K)_ii)/7.                (9)
```

The complete exact distributions are in `exact-results.json`.  In every
orbit all 170 local multiplicities are strictly between zero and one, and

```text
tr(P_K)=71,       tr(E_3^K)=40,       tr(E_-4^K)=31.       (10)
```

For an off-diagonal pair `{i,j}`, substituting `D_ij=0` and `D_ij=1` into
(8) gives two candidate entries for each projector.  Exact Cauchy--Schwarz
tests

```text
|(E_r^K)_ij|^2 <= (E_r^K)_ii (E_r^K)_jj,  r in {3,-4},   (11)
```

show that **both** binary choices pass both inequalities for **all 3,570
pairs**, in all three orbits.  Thus diagonal local multiplicities and every
`2 x 2` projector minor force no edge and no nonedge.

## 3. Exact boundary

Equations (1)--(11) close two plausible symbolic shortcuts more sharply than
rank, trace, or spectrum alone, but they do not solve the quadratic entrywise
problem.  Larger projector minors retain unresolved correlations among
several entries of `D`; treating their consistency as proved would simply
restate the missing quadratic block.

No `85 x 85` block `D`, 99-vertex graph, or nonexistence certificate is
supplied.  Orbits `0`, `4`, and `29`, the rank-three branch, and Conway-99 all
remain `UNKNOWN`.

