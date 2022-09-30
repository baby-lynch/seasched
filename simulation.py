from random import random
import threading
from client import Client
from server import Server
from scheduler import Scheduler
from request import Request
from priority_queue import PriorityQueue
from queue import Queue
from threading import Thread
from numpy import random
import time
import json


class Simulation:
    def __init__(self):
        #--------------Resources-------------#
        # for storing requests
        self.req_pool = Queue()
        # for thread safety
        self.lock = threading.RLock()
        # priority queue
        self.prique = PriorityQueue()
        #--------------Parameters-------------#
        self.sim_params = {}
        self.prob_params = {}
        self.client_params = {}
        self.scheduler_params = {}
        self.server_params = {}
        #--------------Components-------------#
        self.client: Client
        self.scheduler: Scheduler
        self.server: Server
        #--------------Threads-------------#
        self.thread_clients: list[Thread] = []
        self.thread_scheduler: Thread
        self.thread_server: Thread

        #---------- Global Init -----------#
        self.sim_init()

    def params_init(self):
        with open('sim.json', 'r') as f:
            params = json.load(f)

        self.sim_params = params['sim_params']
        self.sim_params['start_time'] = time.time()

        self.prob_params = params['prob_params']

        self.client_params = params['client_params']
        self.scheduler_params = params['scheduler_params']
        self.server_params = params['server_params']

    def components_init(self):
        self.client = Client(
            self.client_params, self.prob_params, self.sim_params
        )
        self.scheduler = Scheduler(
            self.scheduler_params, self.prob_params, self.sim_params
        )
        self.server = Server(
            self.server_params, self.prob_params, self.sim_params
        )

    def threads_init(self):
        for _ in range(self.client_params['clients_num']):
            self.thread_clients.append(
                (Thread(target=self.client_process))
            )

        self.thread_scheduler = Thread(
            target=self.scheduler_process
        )
        self.thread_server = Thread(
            target=self.server_process
        )

    def logs_init(self):
        with open('logs/client.log', 'w+', encoding='utf-8')as f:
            f.write(
                "*-----------------------------{} Client Simulation Results -----------------------------*\n".format(
                    time.strftime('%Y.%m.%d %H:%M:%S',
                                  time.localtime(int(time.time())))
                )
            )
        with open('logs/server.log', 'w+', encoding='utf-8')as f:
            f.write(
                "*-----------------------------{} Server Simulation Results -----------------------------*\n".format(
                    time.strftime('%Y.%m.%d %H:%M:%S',
                                  time.localtime(int(time.time())))
                )
            )

    def sim_init(self):
        self.params_init()
        self.components_init()
        self.threads_init()
        self.logs_init()

    def client_process(self):
        while True:
            if time.time() - self.sim_params['start_time'] > self.sim_params['sim_time']:
                break
            #-------------- Client Thread Task --------------#
            self.lock.acquire()
            try:
                req = self.client.generate_req()
            finally:
                self.lock.release()

            # uphold for an random expotential distributive time gap
            _lam = self.prob_params['time_params']['lam']
            _time_gap = random.exponential(scale=1/_lam)
            # print(_time_gap)
            time.sleep(_time_gap)

            self.lock.acquire()
            try:
                self.req_pool.put(req)
            finally:
                self.lock.release()

    def scheduler_process(self):
        while True:
            if time.time() - self.sim_params['start_time'] > self.sim_params['sim_time']:
                break
            #-------------- Scheduler Thread Task --------------#
            req = self.req_pool.get()
            self.scheduler.schedule(req)
            self.prique.enque(req)

    def server_process(self):
        # harvesting simulation results
        requests = []
        while True:
            if time.time() - self.sim_params['start_time'] > self.sim_params['sim_time']:
                break
            #-------------- Server Thread Task --------------#
            if not self.prique.empty():
                req = self.prique.deque()
                self.server.service(req)
                requests.append(
                    {
                        'id': req.id,
                        'cost': req.cost,
                        'priority': req.priority,
                        'arrive_moment': req.arrive_moment,
                        'sched_moment': req.sched_moment,
                        'finish_moment': req.finish_moment,
                        'response_time': req.response_time,
                        'service_time': req.service_time
                    }
                )
            else:
                continue

            alpha = self.scheduler_params['alpha']
            stats_filename = 'statistics/stats' + str(alpha)+".json"
            stats_data = {
                'alpha': alpha,
                'requests': requests
            }
            with open(stats_filename, 'w') as fp:
                json.dump(stats_data, fp)

    def run(self):
        for thread_client in self.thread_clients:
            thread_client.start()
        self.thread_scheduler.start()
        self.thread_server.start()

        for thread_client in self.thread_clients:
            thread_client.join()
        self.thread_scheduler.join()
        self.thread_server.join()

    def daemon(self):
        pass
