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
