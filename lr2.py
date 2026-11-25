"""
Лабораторная работа № 2. Вариант 11.
Эмпирический анализ квадратичных сортировок.
Данные типа D (много повторов, диапазон [0; 10]), n = 1000, 2000, 3000, 4000, k = 3.
Дополнительно: шейкерная сортировка (cocktail sort) vs классический пузырёк.
"""
import sys
from pathlib import Path

# Чтобы импортировать sorts_common из родительской директории
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sorts_common import generate_data, measure
import matplotlib.pyplot as plt


def bubble_sort(arr):
    """Сортировка пузырьком с флагом досрочного выхода."""
    a = arr.copy()
    n = len(a)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a


def insertion_sort(arr):
    """Сортировка вставками."""
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def cocktail_sort(arr):
    """Шейкерная сортировка (двунаправленный пузырёк) с флагом."""
    a = arr.copy()
    n = len(a)
    left, right = 0, n - 1
    while left < right:
        swapped = False
        # Проход слева направо
        for i in range(left, right):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                swapped = True
        if not swapped:
            break
        right -= 1
        swapped = False
        # Проход справа налево
        for i in range(right, left, -1):
            if a[i - 1] > a[i]:
                a[i - 1], a[i] = a[i], a[i - 1]
                swapped = True
        if not swapped:
            break
        left += 1
    return a


def run_main_experiment():
    """Основной эксперимент: пузырёк vs вставки на данных типа D."""
    sizes = [1000, 2000, 3000, 4000]
    repeats = 3
    algorithms = {
        "Пузырьком": bubble_sort,
        "Вставками": insertion_sort,
    }
    results = {name: [] for name in algorithms}

    print("=== Лабораторная работа № 2, вариант 11 ===")
    print("Тип данных: D (диапазон [0; 10], много повторов)")
    print(f"{'n':>6}" + "".join(f"{name:>14}" for name in algorithms))

    for n in sizes:
        data = generate_data(n, kind="D", lo=0, hi=10, seed=42)
        row = f"{n:>6}"
        for name, func in algorithms.items():
            t = measure(func, data, repeats)
            results[name].append(t)
            row += f"{t:>14.4f}"
        print(row)

    # График
    plt.figure(figsize=(8, 5))
    for name, times in results.items():
        plt.plot(sizes, times, marker="o", label=name)
    plt.xlabel("Размер массива n")
    plt.ylabel("Время, с")
    plt.title("ЛР2 вар.11: время сортировки (данные типа D)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("lr2_var11_main.png", dpi=150)
    print("\nГрафик сохранён: lr2_var11_main.png")

    # Проверка квадратичности
    print("\n=== Проверка T(2n)/T(n) ===")
    print(f"{'Переход':>12}{'Пузырёк':>12}{'Вставки':>12}{'Теория':>10}")
    for i in range(len(sizes) - 1):
        if sizes[i + 1] == 2 * sizes[i]:
            ratio_b = results["Пузырьком"][i + 1] / results["Пузырьком"][i]
            ratio_i = results["Вставками"][i + 1] / results["Вставками"][i]
            print(f"{sizes[i]}→{sizes[i+1]:>4}{ratio_b:>12.2f}{ratio_i:>12.2f}{4:>10}")

    return results


def run_additional_m5():
    """Доп. задание М5: шейкерная vs классический пузырёк."""
    print("\n=== Дополнительное задание М5: шейкерная сортировка ===")
    sizes = [1000, 2000, 3000, 4000]
    repeats = 3
    algorithms = {
        "Пузырьком": bubble_sort,
        "Шейкерная": cocktail_sort,
    }
    results = {name: [] for name in algorithms}

    print(f"{'n':>6}" + "".join(f"{name:>14}" for name in algorithms))
    for n in sizes:
        data = generate_data(n, kind="D", lo=0, hi=10, seed=42)
        row = f"{n:>6}"
        for name, func in algorithms.items():
            t = measure(func, data, repeats)
            results[name].append(t)
            row += f"{t:>14.4f}"
        print(row)

    plt.figure(figsize=(8, 5))
    for name, times in results.items():
        plt.plot(sizes, times, marker="o", label=name)
    plt.xlabel("Размер массива n")
    plt.ylabel("Время, с")
    plt.title("ЛР2 вар.11: пузырёк vs шейкерная (данные D)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("lr2_var11_cocktail.png", dpi=150)
    print("График сохранён: lr2_var11_cocktail.png")


if __name__ == "__main__":
    run_main_experiment()
    run_additional_m5()
    print("\nГотово. Запустите скрипт и используйте полученные таблицы и графики в отчёте.")
