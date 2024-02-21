import pytest

from crypteia import Multibasing, Multihashing, ToBytes, compose


def test_pipeline():
    get_hash = compose(ToBytes(), Multihashing("sha3-224"), Multibasing("base58btc"))
    data = "Hello, World!"
    digest = get_hash(data)
    assert len(digest) == 42
    assert digest.startswith("z")
    assert digest == "z5dbMfGzi9pjjDf5Uv7bVDqgPPMGAkrRDmEqSoVquB"
