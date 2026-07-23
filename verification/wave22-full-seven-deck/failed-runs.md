# Retained verifier failures

## Preinspection hash-display command

The first read-only PowerShell command intended to print candidate hashes
computed the hashes but failed while formatting each path:

```text
The regular expression pattern \ is not valid.
FullyQualifiedErrorId : InvalidRegularExpression
```

Cause: a literal backslash was passed to PowerShell's regex-based `-replace`.
No candidate file was modified, and no candidate content was printed.  Before
any candidate content was inspected, the command was rerun using
`String.Replace` for path separators and the successful output was committed
to `preinspection-freeze.tsv`.

## Generated-cache cleanup

Two attempts to remove the verifier's generated `__pycache__` with
PowerShell `Remove-Item` were rejected by the execution policy before running.
After resolving and checking the exact directory was the direct child of this
verification package, the two `.pyc` files and now-empty directory were removed
with explicit .NET file and nonrecursive directory deletion calls.  No research
artifact was removed.

## Mathematical and certificate discrepancies

None found.  All candidate claims within the stated aggregate-count scope
reproduced independently.
