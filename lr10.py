"""
Лабораторная работа № 10. Вариант 11.
Дейкстра на решётке k×k (k=25,45,65), веса 1..50.
Доп. К4: число кратчайших путей.
"""
import heapq
import random
import time

INF = float("inf")


def dijkstra_count(adj, s):
    """Дейкстра с подсчётом числа кратчайших путей."""
    n = len(adj)
    dist = [INF] * n
    count = [0] * n
    dist[s] = 0
    count[s] = 1
    heap = [(0, s)]
    while heap:
        d, v = heapq.heappop(heap)
        if d > dist[v]:
            continue
        for u, w in adj[v]:
            if dist[v] + w < dist[u]:
                dist[u] = dist[v] + w
                count[u] = count[v]
                heapq.heappush(heap, (dist[u], u))
            elif dist[v] + w == dist[u]:
                count[u] += count[v]
    return dist, count


def make_grid(k, max_w=50, seed=42):
    """Решётка k×k, вершины 0..k*k-1, рёбра вправо и вниз."""
    n = k * k
    adj = [[] for _ in range(n)]
    rng = random.Random(seed)
    for i in range(k):
        for j in range(k):
            v = i * k + j
            if j + 1 < k:
                adj[v].append((v + 1, rng.randint(1, max_w)))
            if i + 1 < k:
                adj[v].append((v + k, rng.randint(1, max_w)))
    return adj


if __name__ == "__main__":
    print("=== ЛР10 вариант 11: решётка + число кратчайших путей ===")
    for k in [25, 45, 65]:
        adj = make_grid(k)
        n = k * k
        t0 = time.perf_counter()
        dist, count = dijkstra_count(adj, 0)
        t = time.perf_counter() - t0
        target = n - 1
        print(f"k={k:>3} (n={n:>5}): расстояние до правого нижнего {dist[target]}, "
              f"число путей {count[target]}, время {t:.4f} с")
    print("Готово.")
