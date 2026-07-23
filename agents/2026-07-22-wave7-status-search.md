# Wave 7 precise-status and novelty search

```yaml
role: literature
date_utc: 2026-07-23T00:53:29Z
git_commit: 0728b260e1282afdbaeaa9215659a4175cab25de
claim_label: UNKNOWN
scope: precise conditional bounds n3>=30 and induced_C6_count>=209316 for a putative srg(99,14,1,2)
inputs:
  agents/2026-07-22-wave7-triangle-side-incidence.md: 2225d7f26f8719d24bceca0c4ef6d8b829332a80793762769d282f176e75b651
  reimbayev_2024_pdf:
    url: https://ejaam.org/articles/2024/10.62780-ejaam-2024-001.pdf
    sha256: 484ff4bbcf13ea26d478baa4c24b97f6996ac3fc35ef8459c15fb61b61b98521
  reimbayev_2025_v2_pdf:
    url: https://arxiv.org/pdf/2508.03377v2
    sha256: c25d3c989343a7af843ddfaa07187558ecc115c19b100f96d599b296ef203fe9
  cesarz_woldar_2025_pdf:
    url: https://alco.centre-mersenne.org/item/10.5802/alco.418.pdf
    sha256: d88f3832337b949edbd21cadf0836bd0df77bf84bf5c225a1b834d9883ca65a8
method: targeted web and full-text search of primary sources under exact values, formulas, graph parameters, and alternate terminology
command: interactive web search and full-text PDF inspection using the exact queries recorded below
outputs:
  checked_source_prior_art_hit: NONE_FOUND
  novelty_established: false
search_date: 2026-07-22
verdict: NO_PRIOR_ART_HIT_IN_CHECKED_PRIMARY_SOURCES_NOVELTY_NOT_ESTABLISHED
limitations: absence from a targeted search is not proof of novelty or exhaustive bibliographic coverage
```

## Queries

The independent status auditor searched variants including

```text
"n3 >= 30" "strongly regular"
"n_3 \ge 30" "strongly regular"
"209316" "srg(99"
"209,316" "srg(99"
"209,286" hexagons strongly regular
"srg(99,14,1,2)" hexagons
"Conway 99-graph" hexagons
"Conway 99" "N3" graph
site:arxiv.org "srg(99,14,1,2)" "n3"
"The Subgraphs of Order Six" Reimbayev
```

The full texts of both Reimbayev papers were also searched for `n3`, lower-
bound variants, the exact values `209316` and `209,316`, and the target
parameters.

## Primary-source findings

Reimbayev's 2024 paper,
[*The Lower Bound for Number of Hexagons in Strongly Regular Graphs with
Parameters lambda=1 and mu=2*](https://doi.org/10.62780/ejaam/2024-001),
derives

```text
p6 = (1/12) n k (k-2) (2k^2-21k+53) + n3.
```

For `(n,k)=(99,14)`, this is `p6=209,286+n3`. Its published lower bound uses
only `n3>=0`, and it does not state `n3>=30`.

The current 2025 order-six preprint,
[*The Subgraphs of Order Six of the Family of Strongly Regular Graphs with
Parameters lambda=1 and mu=2*](https://arxiv.org/abs/2508.03377v2), explicitly
treats `n3` as a free variable and expresses the other six-vertex counts in
terms of `n,k,n3`. Its conclusion does not determine `n3`; the exact Wave 7
bound and induced-cycle value do not appear.

Cesarz and Woldar's 2025 published paper,
[*On the automorphism group of a putative Conway 99-graph*](https://doi.org/10.5802/alco.418),
addresses automorphism restrictions rather than this induced-subgraph count.

## Conservative verdict

No checked primary source was found stating the conditional bound

```text
n3 >= 30
```

or its equivalent `p6>=209,316`. This targeted search does not establish
novelty, and the project makes no novelty claim. It also does not alter the
literature or project status of Conway-99 itself, which remains `UNKNOWN` here.
