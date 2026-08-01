# Weight-fourteen sign balance in the ternary adjacency kernel

All statements are conditional on a hypothetical `srg(99,14,1,2)`.  Let
`x in ker_F3(A)` have entries represented by `0,1,-1`.  Put

```text
P={v:x_v=1},  N={v:x_v=-1},  p=|P|,  n=|N|,
i_v=|N(v) intersect P|,  j_v=|N(v) intersect N|.
```

The imported Wave 207 theorem says that the point image of a hypothetical
weight-eight endpoint word is nonzero and has weight in `{14,17,20,23}`.
This package studies only the first of those four cases.

## 1. Exact signed-support equations

The check equation is

```text
i_v=j_v mod 3.                                      (1)
```

Let `1_P(v)` and `1_N(v)` denote membership indicators.  Regularity,
common-neighbor counting, and the support handshakes give

```text
sum i                              =14p,
sum j                              =14n,
sum [i(i-1)+1_P i]                =2p(p-1),
sum [j(j-1)+1_N j]                =2n(n-1),
sum [ij+1_P j]                    =2pn,
sum [1_P j-1_N i]                 =0.               (2)
```

For example, `sum C(i,2)=p(p-1)-e_P` and
`sum_P i=2e_P`, which proves the third equation.  The other pair equations
follow in the same way from `lambda=1`, `mu=2`.

At weight fourteen, `p-n=0 mod 3` leaves

```text
(p,n)=(1,13),(4,10),(7,7),(10,4),(13,1).           (3)
```

Negating `x` swaps `p,n`, so it is enough to exclude `(1,13)` and `(4,10)`.

## 2. The `(1,13)` Farkas certificate

For every admissible local type define

```text
Phi_13 = 1_N +4i-2j +j(j-1)+1_N j -2ij-2*1_N i.
```

This is the following integer combination of (2):

```text
1_N +4i-2j
+ [j(j-1)+1_N j]
-2[ij+1_P j]
+2[1_P j-1_N i].                                  (4)
```

It is pointwise nonnegative.  Because `p=1`, the possible values have
`i=0` on `P` and `i in {0,1}` elsewhere.  Using (1), (4) factors as

```text
P, i=0:  j(j-3),
O, i=0:  j(j-3),
O, i=1:  (j-1)(j-4),
N, i=0:  (j-1)^2,
N, i=1:  (j-1)(j-3).
```

The relevant residue classes are respectively `j=0 mod 3` or `j=1 mod 3`,
so every displayed value is nonnegative on its exact range.  But summing
(4) and using (2) gives

```text
13 +4(14)-2(14*13)+2(13*12)-4(13) = -35,          (5)
```

a contradiction.

## 3. The `(4,10)` Farkas certificate

Now define

```text
Phi_10 = 3i-2j+j(j-1)-ij+1_N(j-i).
```

Its unsimplified combination of (2) is

```text
3i-2j
+ [j(j-1)+1_N j]
- [ij+1_P j]
+ [1_P j-1_N i].                                  (6)
```

Since `i<=4`, equation (1) gives the pointwise factorizations

```text
v in P or O:  Phi_10=(j-3)(j-i),
v in N:       Phi_10=(j-2)(j-i).
```

For `j=0,1,2`, the congruence and `i<=4` make both products nonnegative;
for `j>=3`, one has `j>=i` (with the only `j=2` boundary already covered).
Thus `Phi_10>=0` everywhere.  Its global sum is nevertheless

```text
3(14*4)-2(14*10)+2(10*9)-2(4*10) = -12,           (7)
```

again a contradiction.

By sign reversal, `(13,1)` and `(10,4)` are also impossible.  Therefore

```text
Every weight-14 word in ker_F3(A), if one exists, has (p,n)=(7,7). (8)
```

This is a sign-composition theorem, not an exclusion of weight fourteen.

## 4. The integer lift and why its aggregate form stalls

Write `p-n=3t` and lift `Ax=0 mod 3` by setting `z=Ax/3 in Z^99`.
The integer SRG identity yields

```text
3Az=A^2x=12x-Ax+2Jx,
Az=4x-z+2t*1.                                     (9)
```

This pointwise equation may still carry unexploited information.  However,
summing it only over `P` or `N` adds nothing to (2).  After substituting the
pair moments, the two residuals are exactly

```text
2p(p-n)-6tp=0,
2n(p-n)-6tn=0.                                    (10)
```

The checker records this collapse explicitly.  A useful continuation must
retain correlations between neighboring `z` values, not merely category
sums.

## 5. Hostile balanced control and status wall

The included balanced aggregate control satisfies (1), all equations (2),
and the aggregate equations obtained from the local `7K_2` neighborhood
matching.  It is deliberately nongraphical: both sign classes declare degree
multiset `[0,0,0,0,0,6,6]`.  A degree-six vertex would meet every peer, which
contradicts the five degree-zero declarations.  Hence it is neither a graph
nor a codeword; it only demonstrates that these aggregate equations do not
exclude the balanced branch.

```text
weight 14, unbalanced compositions: REFUTED
weight 14, balanced 7+7 branch:      UNKNOWN
weight 14 excluded:                  NO
weights 17,20,23 excluded:           NO
d(ker_F3 A)>=24:                     UNKNOWN
endpoint / Conway-99:                UNKNOWN
```

