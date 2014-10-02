import unittest
from pixie.vm.persistent_vector import PersistentVector, EMPTY


def test_vector_conj():

    acc = EMPTY
    for x in range(1000):
        acc = acc.conj(x)
        for y in range(x):
            assert acc.nth(y) == y