# tests/test_rgs_basic.py
from typing import List
from combinatoria.rgs import rgs_all, rgs_exactly, rgs_exactly_y, rgs_range, rgs_to_blocks

def is_valid_rgs(a: List[int]) -> bool:
    """RGS válido: a[i] <= 1 + max(a[:i]) y etiquetas compactas 0..m."""
    max_so_far = -1
    used = set()
    for i, v in enumerate(a):
        if i == 0:
            if v != 0: 
                return False
            max_so_far = 0
        else:
            if v > max_so_far + 1:
                return False
            max_so_far = max(max_so_far, v)
        used.add(v)
    # Compacto: si max label = m, entonces aparecen todos 0..m
    return used == set(range(max(a) + 1)) if a else True

def is_valid_partition(blocks: List[List[int]], n: int) -> bool:
    """Bloques no vacíos, disjuntos, cubren {1..n}."""
    flat = [x for b in blocks for x in b]
    return (
        all(len(b) >= 1 for b in blocks)
        and len(flat) == n
        and set(flat) == set(range(1, n + 1))
        and sum(len(b) for b in blocks) == len(set(flat))
    )

def test_rgs_all_basic_properties():
    n = 5
    rgss = list(rgs_all(n))  # RGS como listas de ints
    assert len(rgss) > 0
    # Cada RGS es válida y su conversión a bloques es partición válida
    for a in rgss:
        assert is_valid_rgs(a)
        blocks = rgs_to_blocks(a)
        assert is_valid_partition(blocks, n)

def test_exactly_k_variants_match():
    n, k = 5, 3
    xs = list(rgs_exactly(n, k))
    ys = list(rgs_exactly_y(n, k))
    # mismas cantidades y mismos conjuntos (en general, mismo orden también)
    assert len(xs) == len(ys)
    assert set(tuple(x) for x in xs) == set(tuple(y) for y in ys)

def test_range_covers_union_of_exactly():
    n, kmin, kmax = 6, 2, 4
    rng = list(rgs_range(n, kmin, kmax))
    union = []
    for k in range(kmin, kmax + 1):
        union.extend(list(rgs_exactly(n, k)))
    assert len(rng) == len(union)
    assert set(tuple(x) for x in rng) == set(tuple(x) for x in union)
