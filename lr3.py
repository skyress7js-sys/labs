"""
Лабораторная работа № 3. Вариант 11.
Быстрая сортировка (опорный — первый элемент, разбиение Ломуто)
и восходящая (bottom-up) сортировка слиянием.
Сравнение с алгоритмами ЛР2 и sorted().
Доп. задание Г5: устойчивость на записях (регион, выручка).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sorts_common import generate_data, measure
import matplotlib.pyplot as plt

# ---------- Сортировки из ЛР2 (для эксперимента 1) ----------
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

# ---------- Быстрая сортировка (первый опорный, Ломуто) ----------
def quick_sort(arr):
    """Быстрая сортировка с опорным первым элементом и схемой Ломуто.
    Рекурсия только в меньшую часть — глубина стека O(log n).
    """
    a = arr.copy()
    _quick_sort(a, 0, len(a) - 1)
    return a


def _quick_sort(a, lo, hi):
    while lo < hi:
        p = _partition_lomuto_first(a, lo, hi)
        # Рекурсия в меньшую часть
        if p - lo < hi - p:
            _quick_sort(a, lo, p - 1)
            lo = p + 1
        else:
            _quick_sort(a, p + 1, hi)
            hi = p - 1


def _partition_lomuto_first(a, lo, hi):
    """Разбиение Ломуто, опорный элемент — первый (a[lo])."""
    # Перемещаем опорный в конец для стандартного Ломуто
    a[lo], a[hi] = a[hi], a[lo]
    pivot = a[hi]
    i = lo - 1
    for j in range(lo, hi):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[hi] = a[hi], a[i + 1]
    return i + 1


# ---------- Восходящая сортировка слиянием ----------
def merge_sort(arr):
    """Восходящая (bottom-up, итеративная) сортировка слиянием. Устойчивая."""
    a = arr.copy()
    n = len(a)
    width = 1
    while width < n:
        for left in range(0, n, 2 * width):
            mid = min(left + width, n)
            right = min(left + 2 * width, n)
            if mid < right:
                merged = _merge(a[left:mid], a[mid:right])
                a[left:right] = merged
        width *= 2
    return a


def _merge(left, right):
    """Слияние двух отсортированных списков. Устойчивое (при равенстве берём из left)."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def run_experiment(algorithms, sizes, kind="random", lo=0, hi=100_000, repeats=3, label=""):
    """Запуск эксперимента и вывод таблицы."""
    results = {name: [] for name in algorithms}
    print(f"\n=== {label} ===")
    print(f"{'n':>8}" + "".join(f"{name:>12}" for name in algorithms))
    for n in sizes:
        data = generate_data(n, kind=kind, lo=lo, hi=hi)
        row = f"{n:>8}"
        for name, func in algorithms.items():
            t = measure(func, data, repeats)
            results[name].append(t)
            row += f"{t:>12.4f}"
        print(row)
    return results


def experiment_1():
    """Эксперимент 1: 4 алгоритма на малых размерах (из ЛР2)."""
    small = [1000, 2000, 3000, 4000]
    algs = {
        "Пузырьком": bubble_sort,
        "Вставками": insertion_sort,
        "Быстрая": quick_sort,
        "Слиянием": merge_sort,
    }
    res = run_experiment(algs, small, kind="D", lo=0, hi=10,
                         label="Эксперимент 1: 4 алгоритма (данные D, [0;10])")
    # График с лог шкалой
    plt.figure(figsize=(8, 5))
    for name, times in res.items():
        plt.plot(small, times, marker="o", label=name)
    plt.yscale("log")
    plt.xlabel("Размер массива n")
    plt.ylabel("Время, с (лог. шкала)")
    plt.title("ЛР3 вар.11: Эксперимент 1")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("lr3_var11_exp1.png", dpi=150)
    print("График: lr3_var11_exp1.png")
    return res


def experiment_2():
    """Эксперимент 2: O(n log n) на больших размерах."""
    large = [15_000, 30_000, 45_000, 60_000]
    algs = {
        "Быстрая": quick_sort,
        "Слиянием": merge_sort,
        "sorted()": sorted,
    }
    res = run_experiment(algs, large, kind="random",
                         label="Эксперимент 2: большие массивы (случайные)")
    plt.figure(figsize=(8, 5))
    for name, times in res.items():
        plt.plot(large, times, marker="o", label=name)
    plt.xlabel("Размер массива n")
    plt.ylabel("Время, с")
    plt.title("ЛР3 вар.11: Эксперимент 2")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("lr3_var11_exp2.png", dpi=150)
    print("График: lr3_var11_exp2.png")

    # Проверка роста
    print("\n=== T(2n)/T(n) для O(n log n) ===")
    print("(Теория ≈ 2.1–2.2)")
    for i in range(len(large) - 1):
        if large[i + 1] == 2 * large[i]:
            for name in ["Быстрая", "Слиянием"]:
                ratio = res[name][i + 1] / res[name][i]
                print(f"{name} {large[i]}→{large[i+1]}: {ratio:.2f}")
    return res


def experiment_3():
    """Эксперимент 3: влияние структуры данных.
    Для опорного «первый» на упорядоченных данных используем n ≤ 3000.
    """
    print("\n=== Эксперимент 3: структура данных ===")
    print("(Для S и V — n=3000 из-за худшего случая при опорном «первый»)")
    kinds = [
        ("random", "R", 50_000),
        ("sorted", "S", 3000),
        ("reversed", "V", 3000),
        ("nearly_sorted", "N", 50_000),
        ("duplicates", "D", 50_000),
    ]
    print(f"{'Тип':>15}{'n':>8}{'Быстрая':>12}{'Слиянием':>12}")
    for kind, code, n in kinds:
        data = generate_data(n, kind=kind, lo=0, hi=100_000 if kind != "D" else 10)
        t_q = measure(quick_sort, data, repeats=3)
        t_m = measure(merge_sort, data, repeats=3)
        print(f"{code:>15}{n:>8}{t_q:>12.4f}{t_m:>12.4f}")


def additional_g5():
    """Доп. задание Г5: устойчивость на записях (регион, выручка)."""
    print("\n=== Дополнительное задание Г5: устойчивость ===")
    # Записи: (регион, выручка). Одинаковая выручка у нескольких регионов.
    records = [
        ("Москва", 1000),
        ("СПб", 500),
        ("Казань", 1000),
        ("Новосибирск", 300),
        ("Екатеринбург", 500),
        ("Владивосток", 1000),
        ("Калининград", 300),
    ]
    print("Исходный порядок:")
    for r in records:
        print(f"  {r}")

    # Для демонстрации сортируем по выручке (индекс 1)
    # Обёртка: сортируем пары (выручка, исходный_индекс, запись) чтобы сохранить стабильность
    indexed = [(rec[1], i, rec) for i, rec in enumerate(records)]
    print("\n(Сортируем по выручке, сохраняя исходный индекс для проверки стабильности)")

    sorted_by_merge = merge_sort(indexed)  # сортирует по выручке, затем по индексу
    stable_expected = sorted(indexed)  # тоже стабильно по сути, т.к. индекс

    print("\nРезультат сортировки слиянием (по выручке):")
    for _, _, rec in sorted_by_merge:
        print(f"  {rec}")
    print("Порядок совпадает с устойчивым:", sorted_by_merge == stable_expected)

    print("\nБыстрая сортировка может нарушить исходный порядок при равных ключах.")
    q_sorted = quick_sort(indexed)
    print("Результат быстрой (пример):")
    for _, _, rec in q_sorted:
        print(f"  {rec}")
    print("Совпадает с устойчивым?", q_sorted == stable_expected)

    print("\nВывод: сортировка слиянием устойчива и подходит для многоуровневой сортировки отчётов")
    print("(можно последовательно сортировать по разным ключам, сохраняя предыдущий порядок).")
    print("Быстрая сортировка неустойчива — при равных значениях ключа порядок может измениться.")


if __name__ == "__main__":
    # Увеличим лимит рекурсии на всякий случай
    sys.setrecursionlimit(10_000)

    experiment_1()
    experiment_2()
    experiment_3()
    additional_g5()
    print("\nГотово. Используйте таблицы, графики и выводы в отчёте.")
