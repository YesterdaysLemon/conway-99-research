# Wave 210 rank-three marked/outside coupling verifier

Verdict: **PASS / NO VETO** for the sealed finite coupling claim, retained at
`DERIVED`.  Conway-99 and the unknown outside block remain `UNKNOWN`.

The source-blind freeze is `protocol.md` plus `input-freeze.sha256`.
`independent_check.py` reconstructs the labelled census without importing the
discovery checker; its first complete outputs are pinned by
`pre-source-comparison-seal.sha256`.  `post_source_audit.py` then compares all
labelled sets and replays the sealed discovery artifacts.

Reproduce from the repository root:

```powershell
.venv\Scripts\python.exe -B verification\wave210-rank3-marked-outside-coupling-verifier\verify_sealed.py
.venv\Scripts\python.exe -B verification\wave210-rank3-marked-outside-coupling-verifier\post_source_audit.py --verify
.venv\Scripts\python.exe -B -m unittest discover -s verification\wave210-rank3-marked-outside-coupling-verifier -p test_verifier.py -v
```

The verified reduction is `204 -> 96` labelled marked graphs,
`20,928 -> 1,536` labelled packing cases, and
`93,757,440 -> 55,296` labelled case/deficit triples.  All 4,480 exact support
incidence configurations have rank 13 and admit the required local one-factors.
These are necessary local controls only; no `85 x 85` outside adjacency block
`D` is supplied or excluded.
