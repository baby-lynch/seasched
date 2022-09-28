from numpy import random
from request import Request
import threading
import time


class Client:
    def __init__(self, client_params: dict, prob_params: dict, sim_params: dict) -> None:
        # uique request id
        self.u_id = 0
        # to ensure uniqueness of uid
        self.lock = threading.RLock()

        # simuation_parameters
        self.sim_params = sim_params
        # probility_parameters
        self.prob_params = prob_params

    def generate_req(self) -> Request:
        # set request id, lock to ensure the uniqueness of uid
        _id = self.u_id
        self.u_id += 1

        # set creator
        _creator_thread = threading.current_thread().ident

        # set request create_moment
        _cur_moment = time.time()-self.sim_params['start_time']
        # set request cost
        min_cost = self.prob_params['cost_params']['min_cost']
        max_cost = self.prob_params['cost_params']['max_cost']
        _cost = random.uniform(max_cost, min_cost)

        req = Request(_id,
                      _cost,
                      _cur_moment,
                      _creator_thread
                      )
        # print('Request{} create at time:{}, cost is {}'.format(
        #     req.id, req.create_moment, req.cost)
        # )

        with open('logs/client.log', 'a', encoding='utf-8')as f:
            f.write(('Request{} (cost={}) create at time:{} by thread{}\n'.format(
                req.id, req.cost, req.create_moment, req.creator))
            )

        return req
