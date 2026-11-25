"""
Лабораторная работа № 6. Вариант 11.
Кольцевой буфер и односвязный список.
Операции: постановка, извлечение, переполнение. n=5000,10000,20000.
Прикладная задача: буфер последних 100 событий.
"""
import time
from collections import deque


class Node:
    __slots__ = ("value", "next")
    def __init__(self, value, nxt=None):
        self.value = value
        self.next = nxt


class LinkedList:
    def __init__(self):
        self.head = self.tail = None
        self.size = 0

    def push_back(self, value):
        node = Node(value)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1

    def pop_front(self):
        if self.head is None:
            raise IndexError("Пусто")
        val = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.size -= 1
        return val

    def __len__(self):
        return self.size


class CircularQueue:
    def __init__(self, capacity):
        self.data = [None] * capacity
        self.capacity = capacity
        self.head = 0
        self.count = 0

    def enqueue(self, value):
        if self.count == self.capacity:
            raise OverflowError("Переполнение")
        tail = (self.head + self.count) % self.capacity
        self.data[tail] = value
        self.count += 1

    def dequeue(self):
        if self.count == 0:
            raise IndexError("Пусто")
        val = self.data[self.head]
        self.data[self.head] = None
        self.head = (self.head + 1) % self.capacity
        self.count -= 1
        return val

    def __len__(self):
        return self.count


class LastEventsBuffer:
    """Буфер последних 100 событий на основе кольцевой очереди."""
    def __init__(self, limit=100):
        self.q = CircularQueue(limit)

    def add(self, event):
        if len(self.q) == self.q.capacity:
            self.q.dequeue()  # вытеснение старого
        self.q.enqueue(event)

    def get_all(self):
        return list(self.q.data)  # упрощённо


def measure(action, repeats=5):
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        action()
        times.append(time.perf_counter() - t0)
    times.sort()
    return times[len(times)//2]


if __name__ == "__main__":
    print("=== ЛР6 вариант 11 ===")
    SIZES = [5000, 10000, 20000]

    print(f"{'n':>7}{'CQ enqueue':>14}{'LL push_back':>14}{'CQ dequeue':>14}")
    for n in SIZES:
        def cq_enq():
            q = CircularQueue(n)
            for i in range(n):
                q.enqueue(i)

        def ll_push():
            lst = LinkedList()
            for i in range(n):
                lst.push_back(i)

        def cq_deq():
            q = CircularQueue(n)
            for i in range(n):
                q.enqueue(i)
            for _ in range(n):
                q.dequeue()

        print(f"{n:>7}{measure(cq_enq):>14.5f}{measure(ll_push):>14.5f}{measure(cq_deq):>14.5f}")

    print("\n=== Прикладная задача: буфер последних 100 событий ===")
    buf = LastEventsBuffer(100)
    for i in range(250):
        buf.add(f"event-{i}")
    print(f"В буфере {len(buf.q)} событий (должно быть 100)")
    print("Примеры:", buf.get_all()[:5], "...", buf.get_all()[-5:])
    print("Готово.")
