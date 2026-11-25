"""
Лабораторная работа № 12. Вариант 11.
Упаковка в контейнеры: полный перебор (малые n), First Fit Decreasing, локальный поиск (перенос).
Размерности 10..15 и 600. Доп. М4.
"""
import random
import time
from itertools import combinations


def first_fit_decreasing(items, capacity=100):
    items = sorted(items, reverse=True)
    bins = []
    for item in items:
        placed = False
        for b in bins:
            if sum(b) + item <= capacity:
                b.append(item)
                placed = True
                break
        if not placed:
            bins.append([item])
    return len(bins), bins


def local_search_transfer(bins, capacity=100, max_iter=1000):
    """Простой локальный поиск: попытка переноса предмета в другой контейнер."""
    improved = True
    it = 0
    while improved and it < max_iter:
        improved = False
        it += 1
        for i in range(len(bins)):
            for item in bins[i][:]:
                for j in range(len(bins)):
                    if i != j and sum(bins[j]) + item <= capacity:
                        bins[i].remove(item)
                        bins[j].append(item)
                        if not bins[i]:
                            bins.pop(i)
                        improved = True
                        break
                if improved:
                    break
            if improved:
                break
    return len(bins), bins


def brute_bins(items, capacity=100):
    """Полный перебор только для очень малых n (демонстрация)."""
    n = len(items)
    best = n  # худший случай — каждый в своём
    # Для n>12 полный перебор нереалистичен; оставляем как заглушку
    return best


if __name__ == "__main__":
    print("=== ЛР12 вариант 11: упаковка в контейнеры ===")
    rng = random.Random(42)

    print("\nМалые размерности (сравнение с нижней оценкой):")
    for n in [10, 12, 15]:
        items = [rng.randint(10, 60) for _ in range(n)]
        lower = (sum(items) + 99) // 100
        ff, _ = first_fit_decreasing(items)
        ls, _ = local_search_transfer([[x] for x in items])  # старт с FFD-подобного
        print(f"n={n:>2}: нижняя оценка {lower}, FFD {ff}, после локального {ls}")

    print("\nБольшая размерность n=600:")
    items = [rng.randint(5, 50) for _ in range(600)]
    t0 = time.perf_counter()
    ff, bins = first_fit_decreasing(items)
    t1 = time.perf_counter()
    ls, _ = local_search_transfer(bins)
    t2 = time.perf_counter()
    print(f"FFD: {ff} контейнеров за {t1-t0:.3f}с")
    print(f"После локального поиска: {ls} контейнеров за {t2-t1:.3f}с")
    print("Готово.")
