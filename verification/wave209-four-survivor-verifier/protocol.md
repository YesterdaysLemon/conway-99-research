# Wave 209 source-blind verifier protocol: rank-three signed trade

## Role and contamination boundary

This is a verifier run under `AGENTS.md`.  Before this file was frozen, the
verifier read only the repository protocol, the public Wave 208 integration
audit/checkpoint, and the sealed Wave 209 package manifest whose SHA-256 was
communicated by the orchestrator.  No Wave 209 discovery prose, result JSON,
code, test, or agent report was opened.

The independent reconstruction must be written and exercised before the
sealed discovery package is opened.  Discovery code must never be imported,
copied, or called by the independent verifier.  Post-source comparison is a
separate phase and every correction or scope disagreement must be recorded.

## Frozen conditional hypothesis

Assume, only conditionally, a hypothetical prism-free rank-11 endpoint for an
`srg(99,14,1,2)`, its 231 triangle/line incidence columns, a balanced signed
selection `alpha` of eight lines in the surviving labelled rank-three M7g
form `(2,2,2)`, and

```text
c = U alpha,             A c = 3 c,
c_v in {0,+1,-1},        |supp(c)| in {14,20}.
```

Here `K=U^T U` and `R=U^T A U`.  The weight-14 branch has five actual
selected-line intersections (`m=5`), and the weight-20 branch has two
(`m=2`), as independently verified at Wave 208.  No target automorphism is
assumed and all selected-line labels remain distinct.

## Claims frozen for hostile verification

### R3K: selected-line forcing

Independently expand `(R-3K) alpha=0` from the SRG/line axioms and the labelled
rank-three `4K2` selected-line pattern.  Verify that every selected-line
cross-count variable in the matched `q=0` positions is forced to zero.  The
proof must check each coordinate (not only an alpha-weighted sum), retain all
labels, and survive global sign reversal and arbitrary relabelling of the
four matched pairs.

### W14: weight 14, m=5

With seven positive and seven negative support points and `x` the number of
opposite-sign support edges, verify all of the following exact claims:

1. `x=1` is forced.
2. Up to sign-preserving rooted isomorphism there is one support-side rooted
   graph, with the unique cross-edge endpoints distinguished; existence of
   this local graph is not a completion.
3. The 85 zero coordinates have balanced support-neighbour signature counts
   `(z_0,z_1,z_2)=(17,61,7)`, with no omitted higher signature.
4. The seven same-sign deficit pairs on each side admit `7!=5040` labelled
   bijections, exactly `4480` of which pass the stated local SRG/neighbourhood
   constraints.  The census must be over bijections, not an automorphism
   quotient.
5. A label-complete pass over all `C(12,5)=792` marked-intersection subsets
   retains exactly `204`.  Every accepted subset must be directly rechecked;
   rejected subsets need a reproducible reason code.

### W20: weight 20, m=2

With ten positive and ten negative support points and `x` the number of
opposite-sign support edges, verify all of the following:

1. The `x=0` and `x=10` cases are excluded by the frozen exact constraints.
2. The `x=2` branch has exactly six labelled swapped-disjoint marked cases,
   with the count convention stated explicitly and checked under sign swap.
3. A complete aggregate integer census retains exactly `352` rows.  Each row
   must satisfy every frozen degree, edge, common-neighbour, outside-signature,
   selected-line, and moment equation.  The search bounds must be derived,
   not guessed.

The 352 rows are necessary aggregate data only.  They are neither graphs nor
proof that an SRG completion exists.

### LM: full line-vector moments

Reconstruct the necessary moment equations for the 231-entry line-sum vector
`d=B^T c` from `BB^T=A+7I`, including the marked-line contribution.  Enumerate
all integral feasible histograms for both weights and directly verify their
moments.  A feasible histogram is not an incidence realization, and failure
of a restricted histogram search is not nonexistence unless completeness of
the stated integer system is proved.

### WALL: status and scope

The final audit must preserve all of these walls:

* every conclusion is conditional on the hypothetical endpoint and selected
  rank-three branch;
* no aggregate row, rooted support graph, deficit bijection, marked subset,
  or line histogram supplies the omitted 99-vertex adjacency/incidence data;
* local lambda/mu caps are not the full SRG equalities;
* no unproved automorphism quotient is allowed;
* no rank-four branch is excluded here;
* no graph, endpoint exclusion, nonexistence theorem, strict `n3` improvement,
  `Q>=7060`, novelty, or priority result follows;
* Conway-99, the rank-11 endpoint, and the `n3=4158` endpoint remain `UNKNOWN`.

## Independent hostile tests frozen in advance

1. Derive every finite domain from integrality, degree 14, lambda 1, mu 2,
   line size 3, and the signed eigenvector equations; use exact integers only.
2. Implement a label-complete reference enumerator with no discovery imports.
3. Recompute key totals by a structurally separate enumeration or closed-form
   counter: `5040`, `4480`, `792`, `204`, six, and `352`.
4. Recheck every accepted object/row from its primitive representation, with
   no reliance on the filter that accepted it.
5. Test global sign reversal, matched-pair permutations, within-pair swaps,
   and support-side relabellings.  State which transformations preserve labels
   and which are used only as test symmetries, never as a search quotient.
6. Inject near misses: duplicate/missing deficit pairs, forbidden overlap,
   one altered selected intersection, one violated `(R-3K)alpha` coordinate,
   and one altered aggregate/moment count.  Each must be rejected.
7. Search boundary values immediately outside every derived loop bound.
8. Check line histograms both by direct sums and by identities obtained from
   matrix products; reject fractional or out-of-range line values.
9. Construct or retain an explicit scope witness showing that the accepted
   aggregate/local data do not by themselves enforce all outside rows, or
   otherwise give a formal missing-data argument.
10. After unsealing, verify the communicated manifest hash first, then every
    manifest entry, run source tests separately, compare result sets (not just
    headline counts), and record any source undercoverage without silently
    repairing it.

## Promotion rule

The verifier may label a precisely reproduced conditional finite or symbolic
claim `VERIFIED`, but cannot promote its own new repair.  Any new narrowing is
`DERIVED` pending independent review.  The global target remains `UNKNOWN`
unless a complete 99-vertex certificate or a complete impossibility proof is
checked, neither of which is claimed by this protocol.
