import threading
from request import Request
import time


class Server:
    def __init__(self, server_params, prob_params, sim_params) -> None:
       # simuation_parameters
        self.sim_params = sim_params
        # probility_parameters
        self.prob_params = prob_params

        # uplink bandwidth simulation for server
        self.uplink_bdw = server_params['uplink_bdw']

    def service(self, req: Request):
        _cur_moment = time.time()-self.sim_params['start_time']
        req.sched_moment = _cur_moment
        req.response_time = req.sched_moment - req.arrive_moment
        req.service_time = (req.cost * 8) / (self.uplink_bdw * 1e6)
        time.sleep(req.service_time)
        req.finish_time = req.sched_moment + req.service_time

        with open('logs/server.log', 'a', encoding='utf-8') as f:
            f.write(('Request{} (cost={}, priority={}) arrive at time:{}, scheduled by server at time:{}, Response time:{}, ETA is:{}, Finish Time is:{}\n'.format(
                req.id, req.cost, req.priority, req.arrive_moment, req.sched_moment, req.response_time, req.service_time, req.finish_time))
            )
