"""
Лабораторная работа № 8. Вариант 11.
Рюкзак 0/1: жадный по удельной ценности и по максимальной ценности vs ДП.
N=24, W=200. Доп. Ж4.
"""
import random
import statistics
import time


def knapsack_dp(weights, values, capacity):
    D = [0] * (capacity + 1)
    for wi, vi in zip(weights, values):
        for w in range(capacity, wi - 1, -1):
            if D[w - wi] + vi > D[w]:
                D[w] = D[w - wi] + vi
    return D[capacity]


def knapsack_greedy(weights, values, capacity, key):
    order = sorted(range(len(weights)), key=key, reverse=True)
    total, remain = 0, capacity
    for i in order:
        if weights[i] <= remain:
            remain -= weights[i]
            total += values[i]
    return total


def experiment(trials=300, n=24, capacity=200, seed=2024):
    rng = random.Random(seed)
    dev = {"Удельная": [], "Макс. ценность": []}
    hits = {k: 0 for k in dev}
    for _ in range(trials):
        weights = [rng.randint(5, 40) for _ in range(n)]
        values = [rng.randint(10, 100) for _ in range(n)]
        opt = knapsack_dp(weights, values, capacity)
        for name, key in [("Удельная", lambda i: values[i]/weights[i]),
                          ("Макс. ценность", lambda i: values[i])]:
            got = knapsack_greedy(weights, values, capacity, key)
            dev[name].append((opt - got) / opt * 100 if opt else 0)
            if got == opt:
                hits[name] += 1
    return dev, hits, trials


if __name__ == "__main__":
    print("=== ЛР8 вариант 11 ===")
    # Контрпример
    w, v, W = [6, 5, 5], [12, 9, 9], 10
    g = knapsack_greedy(w, v, W, lambda i: v[i]/w[i])
    opt = knapsack_dp(w, v, W)
    print(f"Контрпример: жадно {g}, оптимум {opt}, отклонение {(opt-g)/opt*100:.1f}%")

    dev, hits, trials = experiment()
    print(f"\nСерия {trials} наборов (N=24, W=200):")
    print(f"{'Критерий':<18}{'среднее %':>12}{'медиана %':>12}{'макс %':>10}{'совпадений %':>14}")
    for name, d in dev.items():
        print(f"{name:<18}{statistics.mean(d):>12.2f}{statistics.median(d):>12.2f}"
              f"{max(d):>10.2f}{hits[name]/trials*100:>13.1f}%")

    print("\n=== Доп. Ж4: отклонение от N ===")
    for n in [5, 10, 15, 24, 40]:
        d, _, _ = experiment(trials=100, n=n, capacity=200)
        print(f"N={n:>3}: среднее отклонение (удельная) {statistics.mean(d['Удельная']):.2f}%")
    print("Готово.")
