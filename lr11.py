"""
Лабораторная работа № 11. Вариант 11.
Наивный поиск и КМП. Образец «abbabba», случайный текст n=10^5,10^6.
Расстояние Левенштейна с оптимизацией памяти. Доп. Л4.
"""
import random
import time


def naive_search(text, pattern):
    n, m = len(text), len(pattern)
    positions, comps = [], 0
    for i in range(n - m + 1):
        j = 0
        while j < m:
            comps += 1
            if text[i + j] != pattern[j]:
                break
            j += 1
        if j == m:
            positions.append(i)
    return positions, comps


def prefix_function(p):
    pi = [0] * len(p)
    k = 0
    for i in range(1, len(p)):
        while k > 0 and p[i] != p[k]:
            k = pi[k - 1]
        if p[i] == p[k]:
            k += 1
        pi[i] = k
    return pi


def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
    pi = prefix_function(pattern)
    positions, comps = [], 0
    k = 0
    for i in range(n):
        while k > 0 and text[i] != pattern[k]:
            comps += 1
            k = pi[k - 1]
        comps += 1
        if text[i] == pattern[k]:
            k += 1
        if k == m:
            positions.append(i - m + 1)
            k = pi[k - 1]
    return positions, comps


def levenshtein_opt(a, b):
    """Расстояние Левенштейна с O(min(n,m)) памяти."""
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for ca in a:
        curr = [prev[0] + 1]
        for j, cb in enumerate(b, 1):
            curr.append(min(prev[j] + 1, curr[j-1] + 1, prev[j-1] + (ca != cb)))
        prev = curr
    return prev[-1]


if __name__ == "__main__":
    print("=== ЛР11 вариант 11 ===")
    PATTERN = "abbabba"
    rng = random.Random(42)
    print(f"π для '{PATTERN}': {prefix_function(PATTERN)}")

    for n in [10**5, 10**6]:
        text = "".join(rng.choice("abcd") for _ in range(n))
        t0 = time.perf_counter()
        _, c1 = naive_search(text, PATTERN)
        tn = time.perf_counter() - t0
        t0 = time.perf_counter()
        _, c2 = kmp_search(text, PATTERN)
        tk = time.perf_counter() - t0
        print(f"n={n:>7}: наивный {tn:.4f}с ({c1} сравн.), КМП {tk:.4f}с ({c2} сравн.)")

    print("\n=== Доп. Л4: оптимизированный Левенштейн ===")
    pairs = [("кот", "скот"), ("Ромашка", "Ромашки"), ("аналитика", "аналитик")]
    for a, b in pairs:
        print(f"d('{a}','{b}') = {levenshtein_opt(a, b)}")
    print("Готово.")
