"""
Лабораторная работа № 4. Вариант 11.
Последовательный, двоичный и интерполяционный поиск.
Данные: кластеризованное распределение (К), n=10^3,10^4,10^5, k=500, успешные запросы.
Доп. Б4: поиск границ диапазона (первое и последнее вхождение) за O(log n).
"""
import random
import time
import matplotlib.pyplot as plt


def linear_search(a, q):
    for i, value in enumerate(a):
        if value == q:
            return i, i + 1
    return -1, len(a)


def binary_search(a, q):
    lo, hi, cmps = 0, len(a) - 1, 0
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        cmps += 1
        if a[mid] == q:
            return mid, cmps
        if a[mid] < q:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1, cmps


def interpolation_search(a, q):
    lo, hi, cmps = 0, len(a) - 1, 0
    while lo <= hi and a[lo] <= q <= a[hi]:
        if a[lo] == a[hi]:
            cmps += 1
            return (lo, cmps) if a[lo] == q else (-1, cmps)
        mid = lo + (q - a[lo]) * (hi - lo) // (a[hi] - a[lo])
        cmps += 1
        if mid < lo or mid > hi:
            break
        if a[mid] == q:
            return mid, cmps
        if a[mid] < q:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1, cmps


def find_bounds(a, q):
    """Поиск первого и последнего вхождения ключа за O(log n)."""
    def lower_bound():
        lo, hi = 0, len(a)
        while lo < hi:
            mid = (lo + hi) // 2
            if a[mid] < q:
                lo = mid + 1
            else:
                hi = mid
        return lo

    def upper_bound():
        lo, hi = 0, len(a)
        while lo < hi:
            mid = (lo + hi) // 2
            if a[mid] <= q:
                lo = mid + 1
            else:
                hi = mid
        return lo

    left = lower_bound()
    right = upper_bound()
    if left < len(a) and a[left] == q:
        return left, right - 1, right - left
    return -1, -1, 0


def make_clustered(n, seed=42):
    """Кластеризованное распределение: 90% в [0;n], 10% в [10^6;10^7]."""
    rng = random.Random(seed)
    data = []
    for _ in range(n):
        if rng.random() < 0.9:
            data.append(rng.randint(0, n))
        else:
            data.append(rng.randint(10**6, 10**7))
    return sorted(data)


def benchmark(search_func, data, queries):
    start = time.perf_counter()
    total_cmps = 0
    for q in queries:
        _, cmps = search_func(data, q)
        total_cmps += cmps
    elapsed = time.perf_counter() - start
    return elapsed / len(queries), total_cmps / len(queries)


if __name__ == "__main__":
    SIZES = [10**3, 10**4, 10**5]
    K = 500
    rng = random.Random(1)
    algorithms = {
        "Последовательный": linear_search,
        "Двоичный": binary_search,
        "Интерполяционный": interpolation_search,
    }

    print("=== ЛР4 вариант 11 (кластеризованные данные, успешные запросы) ===")
    for n in SIZES:
        data = make_clustered(n)
        queries = [rng.choice(data) for _ in range(K)]
        print(f"\nn = {n}")
        for name, func in algorithms.items():
            t, c = benchmark(func, data, queries)
            print(f"  {name:<20} {t*1e6:10.2f} мкс/запрос   {c:10.1f} сравнений")

    # Доп. Б4
    print("\n=== Доп. Б4: границы диапазона ===")
    data = make_clustered(10_000, seed=7)
    # добавим повторы
    data = sorted(data + [data[100]] * 5 + [data[500]] * 3)
    for q in [data[100], data[500], 999999]:
        left, right, count = find_bounds(data, q)
        print(f"Ключ {q}: первое={left}, последнее={right}, вхождений={count}")

    print("\nГотово.")
