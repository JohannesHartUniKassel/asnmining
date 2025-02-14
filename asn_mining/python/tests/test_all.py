import pytest
import asn_mining


def test_sum_as_string():
    assert asn_mining.sum_as_string(1, 1) == "2"
