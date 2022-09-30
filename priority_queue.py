from request import Request
import heapq


class PriorityQueue:
    def __init__(self) -> None:
        self.heap = []

    def enque(self, req: Request) -> None:
        heapq.heappush(self.heap, req)
        return

    def deque(self) -> Request:
        if not self.heap:
            return None
        return heapq.heappop(self.heap)

    def empty(self) -> bool:
        return len(self.heap) == 0

    def length(self) -> int:
        return len(self.heap)
