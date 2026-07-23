# Attempt ledger

Record proof and search attempts here, including failures. Each entry should
state its scope, assumptions, result, evidence label, and the smallest known
obstruction. Do not overwrite failed attempts when a method evolves.

## Wave 15: global lift of the `n3=48` residual

- Scope: the independently audited Wave 14 active-point residual, conditional
  on a putative `srg(99,14,1,2)` with `n3=48`.
- Result: `VERIFIED` conditional equality exclusion, so `n3>=51` and
  `induced_C6_count>=209337`.
- Smallest obstruction: the nonempty active original vertices form an induced
  set of order at most 24 and minimum degree at least six, while the target
  spectrum requires every such set to have order at least 27.
- Independent evidence: `wave15-global-lift/` gives spectral and outside-degree
  moment certificates; `wave15-algebraic/` independently reconstructs the
  spectral route and retained triangle moments.
- Retained failures: active common-neighbor caps and the first two
  triangle-intersection moments do not obstruct the residual; an ambiguous
  algebraic JSON key and a CRLF/public-LF certificate mismatch were repaired
  transparently and re-audited.
- Boundary: this is a necessary count bound, not a proof or counterexample for
  Conway-99; target and novelty remain `UNKNOWN`.

## Wave 16: conditional `n3=51`

- Structural scope: all sixteen `sum q=34` profiles under the audited
  active-triangle framework.
- Structural result: `VERIFIED` conditional equality exclusion, hence
  `n3>=54` and `induced_C6_count>=209340`.
- Smallest obstruction: the four surviving profiles give at most 25 active
  original vertices, endpoint-local crossing arithmetic forces minimum
  induced degree six, and the target spectrum requires at least 27 vertices.
- Computational scope: a separate seven-branch active-local relaxation with
  exact CNF hashes and one raw positive candidate.
- Computational result: `PASS_FOR_CONDITIONAL_ACTIVE_LOCAL_ARCHIVE_ONLY`;
  one proofless UNSAT, five timeouts, and one historical budget stop are
  explicitly non-evidentiary.
- Retained failure: discovery baseline `09c20e6` pinned a transient Wave 15
  audit hash; repair `7530cae` pins the final public input and an independent
  re-audit preserves all historical hashes.
- Boundary: neither lane resolves Conway-99 or establishes novelty.
