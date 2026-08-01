# Wave 206 tensor-balance weight addendum protocol

## Frozen claim under audit

Assume the conditional rank-11 endpoint inputs already sealed in Wave 206:

```text
the 231 centered columns z_T are projectively distinct over F_3;
their true column code has dual distance at least four;
A_Delta contains a nonzero word a with
sum_T a_T(z_T tensor z_T)=0.
```

Audit only the proposed strengthening

```text
every nonzero a in A_Delta has wt(a)>=8.
```

For a support of size `k`, all displayed coefficients are nonzero.  The
required proof route is:

1. remove the invertible ambient bilinear form from the rank-one-operator
   equation and write `V Lambda V^T=0`;
2. prove that the row space of `V` is totally isotropic for the
   nondegenerate diagonal coefficient form `Lambda`;
3. apply the Witt-index bound `rank(V)<=floor(k/2)`;
4. transfer dual distance at least four to the assertion that no three
   support points are collinear; and
5. use exact cap maxima in projective dimensions at most two over `F_3` to
   exclude every `k<=7`.

Attack characteristic-three signs, possible degeneracy of the ambient
support span, coefficient-form discriminants, and the cap transfer.  A
weight-eight control should be sought to test whether these ingredients
alone can prove anything stronger.

## Frozen inputs

```text
attempts/wave206-crossing-kernel-proof-b/package-manifest.sha256
sha256 6c7718de1c5f2c7d4203d1727d6b74214e51fa069608f318c8583b07b0325f0a

verification/wave174-no-weight3-dual/package-manifest.sha256
sha256 ac34c8a3b045bec70e3a2080cb4365c0ea43cc732b313ecb3cec355a28f23450

verification/wave174-no-weight3-dual/verification-report.md
sha256 59bc0e470a7d007aa2ddaec262a2f3046c8df7da56192bdab90327962feb9b0a
```

## Status wall

The addendum may strengthen only the support bound for the already derived
conditional tensor-balance word.  It may not promote the Wave 206 discovery
package to independently verified status and may not alter any endpoint,
`n3`, `Q`, graph-construction, or Conway-99 status.
