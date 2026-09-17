import os
from pathlib import Path
import subprocess

import pytest

PINNED_REVISION = "90c38998e8141bd07e49a77a49ec417aa29beee0"


def test_pinned_data_contracts_revision_when_checkout_is_available():
    checkout = os.environ.get("AES_DATA_CONTRACTS_CHECKOUT")
    if not checkout:
        pytest.skip(
            "requires AES_DATA_CONTRACTS_CHECKOUT; this is intentionally not replaced by a synthetic fixture"
        )
    path = Path(checkout)
    observed = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=path, text=True, capture_output=True, check=True
    ).stdout.strip()
    assert observed == PINNED_REVISION
    assert (path / "README.md").is_file()
    assert (path / "src" / "data_contracts").is_dir()
    assert (path / "docs" / "ops" / "CAPABILITY_DECOMPOSITION.md").is_file()
