"""
Лабораторная работа № 5. Вариант 11.
Хеш-таблица: метод деления, квадратичное пробирование и двойное хеширование.
n=40000, m=65521. Доп. В4: зависимость числа проб от α.
"""
import random
import time
import matplotlib.pyplot as plt

M = 65521  # простое


class OpenHashTable:
    EMPTY = object()
    DELETED = object()

    def __init__(self, m=M, probing="quadratic"):
        self.m = m
        self.keys = [self.EMPTY] * m
        self.values = [None] * m
        self.n = 0
        self.probes = 0
        self.probing = probing  # "quadratic" or "double"

    def _hash1(self, key):
        return key % self.m

    def _hash2(self, key):
        return 1 + (key % (self.m - 2))

    def _probe(self, key, i):
        h1 = self._hash1(key)
        if self.probing == "quadratic":
            return (h1 + i * i) % self.m
        else:  # double
            return (h1 + i * self._hash2(key)) % self.m

    def insert(self, key, value):
        for i in range(self.m):
            self.probes += 1
            pos = self._probe(key, i)
            k = self.keys[pos]
            if k is self.EMPTY or k is self.DELETED:
                self.keys[pos], self.values[pos] = key, value
                self.n += 1
                return
            if k == key:
                self.values[pos] = value
                return
        raise RuntimeError("Таблица переполнена")

    def search(self, key):
        for i in range(self.m):
            self.probes += 1
            pos = self._probe(key, i)
            k = self.keys[pos]
            if k is self.EMPTY:
                return None
            if k != self.DELETED and k == key:
                return self.values[pos]
        return None


def experiment_alpha():
    print("=== ЛР5 вариант 11: квадратичное vs двойное хеширование ===")
    N = 40_000
    rng = random.Random(42)
    keys = rng.sample(range(10_000_000), N)
    queries = [rng.choice(keys) for _ in range(5000)]

    for name, probing in [("Квадратичное", "quadratic"), ("Двойное", "double")]:
        table = OpenHashTable(M, probing)
        t0 = time.perf_counter()
        for k in keys:
            table.insert(k, k)
        ti = time.perf_counter() - t0
        table.probes = 0
        t0 = time.perf_counter()
        for q in queries:
            table.search(q)
        ts = time.perf_counter() - t0
        print(f"{name:<16} вставка {ti:.3f}с, поиск {ts:.3f}с, проб/запрос {table.probes/len(queries):.2f}")

    # Доп. В4
    print("\n=== Доп. В4: число проб от α ===")
    alphas = [0.1, 0.3, 0.5, 0.7, 0.9]
    print(f"{'α':>6}{'Квадр.':>12}{'Двойное':>12}{'1/(1-α)':>12}")
    for alpha in alphas:
        n = int(alpha * M)
        keys_sub = keys[:n]
        q_sub = [rng.choice(keys_sub) for _ in range(2000)]
        row = f"{alpha:>6.1f}"
        for probing in ["quadratic", "double"]:
            table = OpenHashTable(M, probing)
            for k in keys_sub:
                table.insert(k, k)
            table.probes = 0
            for q in q_sub:
                table.search(q)
            row += f"{table.probes/len(q_sub):>12.2f}"
        row += f"{1/(1-alpha):>12.2f}"
        print(row)


if __name__ == "__main__":
    experiment_alpha()
    print("\nГотово.")
