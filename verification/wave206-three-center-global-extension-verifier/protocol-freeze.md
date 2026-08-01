# Wave 206 source-blind verifier protocol

```yaml
role: verifier
date_utc: 2026-07-29T21:41:43Z
git_commit: 85e705cc6c2a14d123120c93a847e30aaab1789e
claim_label: UNKNOWN
scope: >-
  Independently verify the formal fixed-middle projector tensor identities,
  the six-space compression Gram interpretation, the seven-star-column
  21-coordinate model, and the exact characteristic-three rank/radical
  caveats. No Wave 206 discovery package is in scope before this protocol
  and its implementation are hash-sealed.
inputs:
  AGENTS.md: read before the blind implementation
  attempts/wave206-three-center-global-extension/protocol.md: read before the blind implementation
  verification/2026-07-29-wave205-integration-audit.md: f50b5591cb0e1e3dfdd835a22fd9156dd3a2a039323388889a6fa5e756a0a297
  verification/2026-07-29-wave205-orchestrator.md: 9b9711ad4b9ac902161833b4a5825404e95ba6f443462ac3d79532df704b2deb
  verification/wave205-fourth-trace-globalization-verifier/package-manifest.sha256: b93f65f72db94539c7d42d7eca6debbaf3a5c4a401db3b812a80549bcb9b8325
  attempts/wave205-nonedge-fourth-trace-proof-a/package-manifest.sha256: 2c9976b6cb07a3036df07fd0e7ceb7ffce6a339651d604fcecdcf8c0c3da3d96
  attempts/wave205-global-fourth-moment-proof-b/package-manifest.sha256: a91a2a1cdbc129fa66e9d63b34031a774d5af78c458d18d9a1aadd7e4be217e7
  attempts/wave205-fourth-trace-globalization/protocol.md: a1d45fc0a82b9944a9e020ded3945e75944e0e00202eacbb20eb05598e30bf4d
method: >-
  Derive all identities from trace cyclicity, self-adjointness, idempotence,
  and the exact zero-frame sum. Implement finite-field matrix arithmetic
  independently in pure Python. Exercise the results on a deterministic
  99-projector algebraic control in a nonsquare nondegenerate 11-space, with
  a fixed seven-column singular star frame for the middle six-space.
command: >-
  python verification/wave206-three-center-global-extension-verifier/independent_verifier.py
  && python -m unittest
  verification/wave206-three-center-global-extension-verifier/test_independent_verifier.py
outputs:
  - verification/wave206-three-center-global-extension-verifier/independent_verifier.py
  - verification/wave206-three-center-global-extension-verifier/test_independent_verifier.py
  - verification/wave206-three-center-global-extension-verifier/blind_result.json
  - verification/wave206-three-center-global-extension-verifier/SOURCE_BLIND_FREEZE.sha256
limitations:
  - The deterministic control is not an SRG incidence configuration.
  - Its 99 projectors are formed by tripling 33 projector types, solely so their sum is zero in characteristic three.
  - Only the fixed middle projector is supplied with the seven-column star frame.
  - The computation verifies formal algebra and coordinate/radical claims, not any actual endpoint tau distribution.
  - No Gram-kernel word is promoted to a true operator or column relation.
  - Conway-99, rank 11, n3=4158, actual nonedge h, and all endpoint claims remain UNKNOWN.
```

## Frozen derivation targets

Work over `F_3`. Let `V` carry a nondegenerate symmetric bilinear form, and
let every `P_x` be a self-adjoint idempotent of rank six. Fix `y`, put
`W_y=im(P_y)`, and define

```text
A_x^(y) = (P_y P_x P_y)|W_y.
T_y[x,z] = tau_(xy;z) = tr(P_x P_y P_z P_y).
```

The source-blind checker must establish, by exact arithmetic and a recorded
algebraic derivation,

```text
T_y[x,z] = tr_Wy(A_x^(y) A_z^(y)),
T_y[x,z] = T_y[z,x],
T_y[x,x] = h_xy,
T_y[x,y] = g_xy,
sum_z T_y[x,z] = 0          when sum_z P_z=0.
```

Thus `T_y` is a Gram matrix for the trace pairing on the 21-dimensional
space of self-adjoint endomorphisms of a six-space. This gives only
`rank(T_y)<=21`.

For a seven-column star frame `Z=Z_y` freeze

```text
Z 1 = 0,
Z^* Z = E_7-I_7 = G,
P_y = -Z Z^*,
K_x = Z^* P_x Z.
```

Here `E_7` is the all-ones matrix. The checker must verify that `K_x` is
symmetric with `K_x 1=0`, that

```text
A_x^(y) = Z K_x Z^*,
tau_(xy;z) = tr(K_x K_z),
```

and that symmetric `7 by 7` matrices annihilating `1` are in bijection with
21 coordinates (the upper triangle of their leading `6 by 6` block).

## Characteristic-three scope wall

The ambient trace pairing on those 21 coordinates must be checked
nondegenerate. This does **not** make its restriction to every feature span
nondegenerate. Exact statements to test are:

```text
rank(T_y)
  = dim span{K_x}
    - dim(span{K_x} intersect span{K_x}^perp);

ker(feature map) is contained in ker(T_y), but equality needs a
nondegenerate restricted pairing.
```

In dimension six over `F_3`, the identity is nonzero but isotropic because
`tr(I_6)=6=0`. In seven-star coordinates it is represented by `G`, with
`tr(G^2)=0`. The full 21-space pairing remains nondegenerate, so isotropic
does not mean radical. By contrast, the trace-zero self-adjoint subspace has
dimension 20 and its restricted trace pairing has a one-dimensional radical
spanned by the identity; its pairing rank is 19. The checker must exhibit
all of these facts exactly.

These identities do not classify graph-labelled triples and do not change
the frozen endpoint status.
