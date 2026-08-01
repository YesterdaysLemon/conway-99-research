#!/usr/bin/env python3
"""Recompute and compare the pre-source-sealed outputs with JSON normalization."""

from __future__ import annotations

import json

import independent_check as independent


def normalized(value: object) -> object:
    return json.loads(json.dumps(value, sort_keys=True))


payload = independent.build_results()
hostile = independent.hostile_tests(payload)
assert json.loads(independent.RESULT_PATH.read_text(encoding="utf-8")) == normalized(payload)
assert json.loads(independent.HOSTILE_PATH.read_text(encoding="utf-8")) == normalized(hostile)
print("independent sealed outputs PASS")
