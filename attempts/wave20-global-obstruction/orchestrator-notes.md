# Wave 20 orchestrator corrections and failed invocations

No item in this file is evidence for the mathematical claim.

## Frozen wording correction

The first paragraph of `failed-routes.md` says `n3>=699`. That sentence is a
stale description of the intermediate mod-two endpoint. The same frozen file's
later integral-lattice section, the discovery report, exact checker, result
JSON, run report, independent reconstruction, and final verifier audit all use
the strengthened endpoint

```text
n3 >= 705.
```

The frozen file is intentionally not rewritten. Its SHA-256 remains
`23355b845f17dac5b4ef260544d1664c8943999634ee8d02f63d5a6b0ef048b2`.

## Root replay failures

Before following the package's working-directory instructions, the
orchestrator attempted a module-style unittest invocation from the repository
root. Import resolution failed before any test ran. The exact original command
and raw terminal text were not retained, so they are not reconstructed here.

A separate exploratory invocation supplied a nonexistent `--check` option to
`exact_check.py`; `argparse` rejected it before computation. The command was
conceptually:

```text
python exact_check.py --check <result>
```

The documented invocations were then run from
`attempts/wave20-global-obstruction`:

```text
python -B -m unittest -v test_exact_check.py
python -B exact_check.py --output <fresh-result.json>
```

They passed 18/18 tests and regenerated SHA-256
`6aea5c4688880a33d358ccc8992ef3aa63d40be70b5c450a8a39bf83b4878dc2`.
The independent verifier separately records its own root-directory import
failure and corrected 16/16-test invocation. None of these harness failures
changed proof code or mathematical conclusions.
