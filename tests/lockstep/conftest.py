"""Lockstep's tests: the example projects and end-to-end scripts are inputs the tests copy, not tests."""

from lockstep_support import planned, proj  # noqa: F401  (shared fixtures)

collect_ignore = ["example", "example-simple", "e2e", "lockstep-plan-sample"]
