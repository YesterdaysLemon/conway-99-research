# Primary-source audit: Kaipa--Pradhan rank-seven configurations

## Source record

- Primary record: <https://arxiv.org/abs/2405.12011>
- Title: *Higher weight spectra of ternary codes associated to the quadratic
  Veronese 3-fold*
- Authors: Krishna Kaipa and Puspendu Pradhan
- ArXiv version inspected: `v1`, submitted 2024-05-20
- Transient PDF SHA256:
  `88c0ce7e6f83609b9556eeb961c40426f7d05c0d917ea82b9cc17ae3aba69f49`
  (`369499` bytes)
- Transient arXiv e-print SHA256:
  `e6858cce6a825dd100720c4e3d30d314bcf95a98474f73bf7e49e4c21fd15594`
  (`30548` bytes, gzip-compressed TeX)

The PDF and e-print bytes were used only for this source check and were
removed before packaging.  They are not vendored.  The line references below
refer to the gzip-expanded TeX snapshot with the recorded e-print hash.

## Located statements

- TeX lines `252--263` define the quadratic Veronese embedding and the rank
  of a point configuration as the rank of its Veronese image.
- TeX lines `266--281` define maximal rank-`r` configurations and state that
  every configuration has the unique maximal closure
  `bar(S)=V(I_2(S))` of the same rank.
- TeX lines `615--644` give the rank-seven classification (rendered Lemma
  6.1) into the seven projective classes `M7a,...,M7g`.
- TeX line `641` describes `M7g` as eight points paired on four lines through
  a common point outside the eight-set, with no three of the lines coplanar.
- The rank-seven enumeration later in Section 6 records that `M7g` has eight
  points and contributes one projective class at support size eight.

The cited equivalence is projective equivalence of configurations in
`PG(3,3)`.  It does not assert that a labelled representative has a unique
internal pairing.  The verifier's exhaustive check of all `105` perfect
matchings found four concurrent-secant decompositions of the same labelled
M7g eight-set.  Each has a unique external concurrency point and no three
secants coplanar.  Thus the correct uniqueness statement is **unique
projective M7g orbit/closure**, together with existence of such a pairing.

## Applicability to the conditional support

Let `S` be the eight projective centered columns supporting a hypothetical
weight-eight word in `A_Delta`.

1. The sealed Wave 206 result gives vector rank four.  The sealed Wave 174
   dual-distance result gives independence of every three supported columns,
   so `S` is an eight-cap in `PG(3,3)`.
2. The quadratic tensor relation makes the eight Veronese columns dependent,
   hence their Veronese rank is at most seven.
3. If that rank were at most six, the Veronese relation space would have
   dimension at least two.  A nontrivial linear combination of two relations
   can cancel any coordinate on which one is nonzero, producing a nonzero
   tensor relation of support at most seven.  The universal Wave 206
   Witt-plus-cap bound forbids such a relation.  The Veronese rank is therefore
   exactly seven.
4. The cited unique maximal closure applies.  The source descriptions bound
   cap size by at most `5,6,6,6,6,7` in `M7a,...,M7f`, respectively: a line
   contributes at most two cap points and a plane in `PG(2,3)` contributes at
   most four.  None can contain the eight-cap.  The only surviving closure is
   `M7g`, whose eight points are exactly `S`.

No graph automorphism, transitivity, or restricted orbit search is used in
this reduction.

## Verdict and boundary

The Kaipa--Pradhan citation and its application are `VERIFIED` for the
conditional weight-eight support.  The source classifies the local
projective support; it neither embeds the eight points into the actual
point--triangle incidence structure nor excludes that embedding.  It gives
no endpoint exclusion, graph construction, or Conway-99 resolution.
