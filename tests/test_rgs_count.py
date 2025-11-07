# tests/test_rgs_counts.py
from typing import Dict, List
from math import comb
from collections import Counter

from combinatoria.rgs import rgs_all, rgs_exactly

# Bell(n) por recurrencia clásica: B_{n+1} = sum_{k=0..n} C(n,k) B_k ; B_0=1
def bell(n: int) -> int:
    B = [0] * (n + 1)
    B[0] = 1
    for m in range(0, n):
        B[m + 1] = sum(comb(m, k) * B[k] for k in range(m + 1))
    return B[n]

# Stirling de 2a especie: S(n,k) = k S(n-1,k) + S(n-1,k-1); S(0,0)=1
def stirling2(n: int, k: int) -> int:
    if n == 0 and k == 0:
        return 1
    if n == 0 or k == 0 or k > n:
        return 0
    S = [[0] * (k + 1) for _ in range(n + 1)]
    S[0][0] = 1
    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            S[i][j] = j * S[i - 1][j] + S[i - 1][j - 1]
    return S[n][k]

def count_by_num_blocks(rgss: List[List[int]]) -> Dict[int, int]:
    # num_bloques = 1 + max(a), o 0 si a está vacío
    c = Counter()
    for a in rgss:
        k = 0 if len(a) == 0 else (1 + max(a))
        c[k] += 1
    return dict(c)

def test_bell_totals_small_n():
    # Valores de referencia: B0=1, B1=1, B2=2, B3=5, B4=15, B5=52, B6=203, B7=877
    for n, expected in [(0,1),(1,1),(2,2),(3,5),(4,15),(5,52),(6,203)]:
        got = len(list(rgs_all(n)))
        assert got == expected == bell(n)

def test_stirling_distribution_n5():
    n = 5
    rgss = list(rgs_all(n))
    byk = count_by_num_blocks(rgss)
    # Esperado: S(5,k) = 1, 15, 25, 10, 1  (k=1..5)
    expected = {k: stirling2(n, k) for k in range(1, n + 1)}
    assert sum(byk.values()) == bell(n) == 52
    assert byk == expected

def test_exactly_matches_stirling_for_range():
    n = 6
    for k in range(1, n + 1):
        got = len(list(rgs_exactly(n, k)))
        exp = stirling2(n, k)
        assert got == exp
