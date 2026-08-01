# Wave 209 proof A: rank-three signed trade

```yaml
role: proof_a
date_utc: 2026-08-01T03:02:36Z
git_commit: c58fd917ea8f9622e1388f10b0e0e3c709ba4854
claim_label: DERIVED
scope: both Ac=3c rank-three branches, support 14/m=5 and support 20/m=2
inputs:
  - attempts/wave209-four-survivor-globalization/protocol.md sha256 3a7208c3cc44bfb1884ad0031592fdca5999c7b52b41fd0cade84d31ddf1f196
  - attempts/wave208-marked-m7g-proof-b/package-manifest.sha256 sha256 f708a29bc2948e4bf732f6fbaa92125f132c28ac753a525f2af1b6fd479180bc
method: exact SRG moments, bounded labelled structural censuses, and line-incidence identities
command: .venv\Scripts\python.exe -B attempts\wave209-rank3-trade-proof-a\exact_check.py --verify
outputs:
  - attempts/wave209-rank3-trade-proof-a/exact-results.json sha256 294c873a751ec5750eb74089d65289cba55ceaf19008e263753b2616b36b7246
limitations: no 99-vertex completion or exclusion; global status UNKNOWN
```

## Result

For `c in {0,+1,-1}^99` with `Ac=3c`, writing `|P|=|N|=k` and
`x=e(P,N)` gives exact outside moments

```text
sum t z_t   =11k-2x,
sum t^2 z_t=2k^2-7x-sum j_v^2,
x<=k^2/9.
```

The selected row identity `(U^T A U-3U^T U)alpha=0` additionally forces all
four matched product-zero selected-line pairs to have cross count zero.

At support 14, exact moment and selected-intersection tests force `x=1`.
The induced graph on either sign is one rooted type, with edges

```text
01 02 03 04 12 15 26 34 35 46 56.
```

Its triangle-free common-neighbor deficit graph forces the unique outside
signature `(z_0,z_1,z_2)=(17,61,7)`.  The selected-line packing retains only
degree multisets `(3,1,1,0)` and `(2,2,1,0)` on each side, and exactly 204 of
the 792 labelled five-intersection subsets remain.  Cross-sign deficit
capacity retains 4,480 of 5,040 bijections for each fixed rooted labelling.

At support 20, the exact aggregate catalog has no `x=10` row.  A complete
selected-zero count relaxation removes `x=0`; `x=2` survives only for six
swapped disjoint intersection pairs, while `x=4,6,8` remain.  There are 352
aggregate rows.  The imported 22-vertex `x=6` control remains a hostile
positive control.

The full line vector `tau=B^T c` obeys `C tau=7tau`, `B tau=10c`, and
`||tau||^2=20k`.  Its remaining norms are feasible.  This is a strict
conditional reduction, not a global proof or counterexample.
