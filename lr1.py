"""
Лабораторная работа № 1. Вариант 11.
Итерационные методы: √a, ∛b, ln c.
Критерий остановки — по разности. x0 = 1.
Д3: сравнение ln с нормализацией и без.
"""
import math

EPS = 1e-4
N_MAX = 100


def sqrt_newton(a, eps=EPS, n_max=N_MAX, x0=1.0):
    """Квадратный корень методом Ньютона (формула Герона)."""
    if a < 0:
        raise ValueError("Подкоренное выражение должно быть неотрицательным")
    if a == 0:
        return 0.0, 0
    x = x0
    for n in range(1, n_max + 1):
        x_new = 0.5 * (x + a / x)
        if abs(x_new - x) < eps:
            return x_new, n
        x = x_new
    raise RuntimeError("Точность не достигнута за N_MAX итераций")


def cbrt_newton(b, eps=EPS, n_max=N_MAX, x0=1.0):
    """Кубический корень методом Ньютона (с учётом знака)."""
    if b == 0:
        return 0.0, 0
    sign = -1 if b < 0 else 1
    b_abs = abs(b)
    x = x0
    for n in range(1, n_max + 1):
        x_new = (2 * x + b_abs / (x * x)) / 3
        if abs(x_new - x) < eps:
            return sign * x_new, n
        x = x_new
    raise RuntimeError("Точность не достигнута за N_MAX итераций")


def ln_series(c, eps=EPS, n_max=100_000):
    """ln c через ряд 2*(y + y³/3 + y⁵/5 + ...), y=(c-1)/(c+1). Без нормализации."""
    if c <= 0:
        raise ValueError("Аргумент логарифма должен быть положительным")
    y = (c - 1) / (c + 1)
    y2 = y * y
    power = y
    total = 0.0
    for k in range(n_max):
        term = 2 * power / (2 * k + 1)
        if abs(term) < eps:
            return total, k
        total += term
        power *= y2
    raise RuntimeError("Точность не достигнута за n_max итераций")


def ln_series_normalized(c, eps=EPS, n_max=100_000):
    """ln c с нормализацией: c = m * 2^k, m ∈ [0.5, 1)."""
    if c <= 0:
        raise ValueError("Аргумент логарифма должен быть положительным")
    m, exp = math.frexp(c)          # m ∈ [0.5, 1), c = m * 2^exp
    ln_m, n_m = ln_series(m, eps, n_max)
    ln2, n2 = ln_series(2.0, eps, n_max)
    return ln_m + exp * ln2, n_m + n2, n_m, n2


if __name__ == "__main__":
    a, b, c = 29, 70, 50
    print(f"Вариант 11: a={a}, b={b}, c={c}, ε={EPS}, x0=1")
    print(f"{'Функция':<16}{'Аргумент':>10}{'Результат':>18}{'Эталон':>18}{'Погрешность':>14}{'Итераций':>10}")

    val_s, n_s = sqrt_newton(a)
    ref_s = math.sqrt(a)
    print(f"{'sqrt':<16}{a:>10}{val_s:>18.10f}{ref_s:>18.10f}{abs(val_s-ref_s):>14.2e}{n_s:>10}")

    val_c, n_c = cbrt_newton(b)
    ref_c = b ** (1/3)
    print(f"{'cbrt':<16}{b:>10}{val_c:>18.10f}{ref_c:>18.10f}{abs(val_c-ref_c):>14.2e}{n_c:>10}")

    val_l, n_l = ln_series(c)
    ref_l = math.log(c)
    print(f"{'ln (без норм.)':<16}{c:>10}{val_l:>18.10f}{ref_l:>18.10f}{abs(val_l-ref_l):>14.2e}{n_l:>10}")

    val_ln, n_tot, n_m, n2 = ln_series_normalized(c)
    print(f"{'ln (с норм.)':<16}{c:>10}{val_ln:>18.10f}{ref_l:>18.10f}{abs(val_ln-ref_l):>14.2e}{n_tot:>10} (m:{n_m}, ln2:{n2})")
