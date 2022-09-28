from simulation import Simulation
from priority_queue import PriorityQueue
from numpy import random
from request import Request
import time


def test_priq():
    pq = PriorityQueue()
    samples = random.uniform(1024, 1024*1024, 10000)
    start_time = time.time()
    alpha = 2
    for i, sample in enumerate(samples):
        req = Request(i, sample, time.time()-start_time, 0)
        req.priority = req.create_moment + alpha*req.cost
        pq.enque(req)

    while not pq.empty():
        req = pq.deque()
        print(req.priority)


if __name__ == "__main__":
    test_priq()
