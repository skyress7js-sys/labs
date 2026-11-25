"""
Лабораторная работа № 9. Вариант 11.
Списки смежности, BFS. Проверка двудольности на разреженных неориентированных графах.
n=1000,2000,4000. Доп. И4.
"""
import random
import time
from collections import deque


class ListGraph:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n)]

    def add_edge(self, u, v):
        self.adj[u].append(v)
        self.adj[v].append(u)

    def neighbors(self, v):
        return self.adj[v]


def is_bipartite(graph):
    """Проверка двудольности раскраской в два цвета при BFS."""
    color = [-1] * graph.n
    for start in range(graph.n):
        if color[start] != -1:
            continue
        color[start] = 0
        queue = deque([start])
        while queue:
            v = queue.popleft()
            for u in graph.neighbors(v):
                if color[u] == -1:
                    color[u] = 1 - color[v]
                    queue.append(u)
                elif color[u] == color[v]:
                    return False, color
    return True, color


def generate_sparse(n, m_factor=3, seed=42):
    rng = random.Random(seed)
    g = ListGraph(n)
    edges = set()
    while len(edges) < n * m_factor:
        u, v = rng.randrange(n), rng.randrange(n)
        if u != v and (min(u,v), max(u,v)) not in edges:
            edges.add((min(u,v), max(u,v)))
            g.add_edge(u, v)
    return g


if __name__ == "__main__":
    print("=== ЛР9 вариант 11: проверка двудольности ===")
    for n in [1000, 2000, 4000]:
        g = generate_sparse(n)
        t0 = time.perf_counter()
        bip, colors = is_bipartite(g)
        t = time.perf_counter() - t0
        print(f"n={n:>5}: двудольный={bip}, время {t:.4f} с, "
              f"цвета 0/1: {colors.count(0)}/{colors.count(1)}")

    print("\n=== Доп. И4: пример недвудольного графа (треугольник) ===")
    g = ListGraph(3)
    g.add_edge(0,1); g.add_edge(1,2); g.add_edge(2,0)
    bip, _ = is_bipartite(g)
    print(f"Треугольник двудольный? {bip} (ожидается False)")
    print("Готово.")
