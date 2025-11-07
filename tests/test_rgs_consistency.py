# tests/test_rgs_consistency.py
from combinatoria.rgs import rgs_all, rgs_exactly, rgs_range

def test_all_equals_union_of_exactly():
    n = 6
    all_v = list(rgs_all(n))
    union = []
    for k in range(1, n + 1):
        union.extend(list(rgs_exactly(n, k)))
    # Igualdad de conjuntos (RGS como tuplas)
    set_all = set(tuple(a) for a in all_v)
    set_union = set(tuple(a) for a in union)
    assert set_all == set_union

def test_range_vs_all_for_full_bounds():
    n = 5
    r = list(rgs_range(n, 1, n))
    v = list(rgs_all(n))
    assert set(tuple(a) for a in r) == set(tuple(a) for a in v)
