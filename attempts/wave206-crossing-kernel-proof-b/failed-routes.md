# Failed routes and retained boundaries

## 1. Ambient nondegeneracy does not identify Gram and operator kernels

The trace form on the 21-dimensional self-adjoint operator space of one
six-dimensional star is nondegenerate.  It is invalid to conclude that its
restriction to the span of the compression operators is nondegenerate.

In characteristic three,

```text
I_6 is nonzero but tr(I_6^2)=0.
```

The trace-zero hyperplane has dimension 20, rank 19, and radical `<I_6>`.
The checker includes the hostile span `{I_6}`, whose feature rank is one
and Gram rank is zero.  Accordingly, a null word of `Tau^(y)` is not
promoted to a true compression relation without a radical check.

## 2. Twenty-one coordinate functionals do not imply twenty-one samples span

The 21 unordered pairs of distinct triangles in a seven-triangle star give
a complete coordinate system for self-adjoint operators on the star
six-space.  This is a statement about coordinate functionals.

It does not say that 21 chosen center compressions `P_yP_xP_y` form a
basis.  That requires a graph-dependent 21-by-21 coordinate determinant or
equivalent span theorem.  No such determinant is assumed.

## 3. Fixed-middle rank does not bound the global fourth moment

Every `Tau^(y)` has rank at most 21.  A deterministic exact control has all
99 slice ranks equal to 21 while `rank(H)=96`.  Therefore the rank cap
cannot be transferred to `H` without the missing shared-incidence
compatibility.

The control is not a target realization: it lacks the shared 231 columns,
degree-three incidence, SRG, prism-free geometry, and endpoint code.

## 4. Square-zero crossing data do not make the localizers vanish

The exact identities

```text
W^T W=0,
(W W^T)^2=0,
sum_x M_x=0,
sum_x(Q o M_x)=0
```

permit nonzero matrices in characteristic three.  They do not imply
`Q o M_x=0`, `Gamma=0`, or `H1=0`.  The exact controls retain nonzero
crossing and Gamma matrices.

## 5. Trace-class nullities are not true relations

Within a fixed `g_xy` residue, compression differences lie in the
trace-zero operator hyperplane.  Their difference Gram has rank at most
19; a largest nonneighbor residue class therefore has Gram nullity at
least eight.

This does not produce eight operator relations.  The one-dimensional
radical `<I_6>` can contribute Gram-kernel words, and the restricted span
may have a larger radical.

## 6. The new tensor relation is not an original-code relation

The forced word

```text
a in im(B^T),
sum_T a_T(z_T tensor z_T)=0
```

is a relation among quadratic Veronese columns.  It need not satisfy
`sum_T a_T z_T=0`.  The verified dual distance of the original centered
`[231,11]_3` code therefore cannot be cited directly for `a`.

The independently checked safe bound is only `wt(a)>=4`.  No complete
composition, upper weight bound, or class-size distribution is derived.

## 7. The constant zero frame is not the new relation

The global coefficient word `1_231` lies in the quadratic tensor kernel,
but it does not lie in `im(B^T)`.  The exact `G^2=G-J` argument proves

```text
im(B^T) intersect <1_231>={0}.
```

Thus the guaranteed nonzero word in the intersection code is nonconstant.
No claim is made that the intersection code is one-dimensional.

## 8. Graph-side fiber patterns need coordinate values

A parallel graph lane may restrict each four-vertex fiber to a matching
pattern.  This package does not consume an unsealed parallel result.
Even after such a pattern is verified, it must be translated into actual
values of the 21 localizer coordinates before equations for `g`, `h`, or
`tau` follow.

## 9. Remaining exact target

The individual fixed-middle Gram slices do not compare coordinates in two
different star spaces.  The next missing invariant is the kernel of the
simultaneous compression map or the mixed four-center tensor

```text
tr((P_yP_xP_y)(P_vP_zP_v)), y!=v.
```

The rank-11 endpoint, `n3=4158`, actual nonedge fourth traces, `Q>=7060`,
and Conway-99 all remain `UNKNOWN`.
