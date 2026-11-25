"""
Лабораторная работа № 7. Вариант 11.
Задача А: числа Фибоначчи (наивная, мемо, итер). n=10..31
Задача Б: размен суммы S=250, номиналы 1,4,6,9. Доп. Г4.
"""
import time

calls = 0


def fib_naive(n):
    global calls
    calls += 1
    if n < 2:
        return n
    return fib_naive(n-1) + fib_naive(n-2)


def fib_memo(n, cache=None):
    global calls
    calls += 1
    if cache is None:
        cache = {}
    if n < 2:
        return n
    if n in cache:
        return cache[n]
    cache[n] = fib_memo(n-1, cache) + fib_memo(n-2, cache)
    return cache[n]


def fib_iter(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def coin_change(amount, coins):
    """Минимальное число монет. Возвращает (число, список монет)."""
    dp = [float("inf")] * (amount + 1)
    parent = [-1] * (amount + 1)
    dp[0] = 0
    for s in range(1, amount + 1):
        for c in coins:
            if c <= s and dp[s - c] + 1 < dp[s]:
                dp[s] = dp[s - c] + 1
                parent[s] = c
    if dp[amount] == float("inf"):
        return -1, []
    # восстановление
    res = []
    s = amount
    while s > 0:
        c = parent[s]
        res.append(c)
        s -= c
    return dp[amount], res


if __name__ == "__main__":
    print("=== ЛР7 вариант 11: Фибоначчи ===")
    print(f"{'n':>4}{'наивная':>12}{'вызовов':>12}{'мемо':>10}{'вызовов':>10}{'итер':>10}")
    for n in [10, 15, 20, 25, 30, 31]:
        global calls
        calls = 0
        t0 = time.perf_counter()
        r1 = fib_naive(n)
        tn = time.perf_counter() - t0
        cn = calls

        calls = 0
        t0 = time.perf_counter()
        r2 = fib_memo(n)
        tm = time.perf_counter() - t0
        cm = calls

        t0 = time.perf_counter()
        r3 = fib_iter(n)
        ti = time.perf_counter() - t0
        assert r1 == r2 == r3
        print(f"{n:>4}{tn:>12.4f}{cn:>12}{tm:>10.6f}{cm:>10}{ti:>10.6f}")

    print("\n=== Размен S=250, номиналы [1,4,6,9] ===")
    coins = [1, 4, 6, 9]
    S = 250
    count, combo = coin_change(S, coins)
    print(f"Минимум монет: {count}")
    print(f"Пример комбинации (первые 20): {combo[:20]}... всего {len(combo)}")

    print("\n=== Доп. Г4: зависимость времени ДП от S ===")
    for S in [50, 100, 250, 500, 1000]:
        t0 = time.perf_counter()
        coin_change(S, coins)
        print(f"S={S:>5}: {time.perf_counter()-t0:.6f} с")
    print("Готово.")
