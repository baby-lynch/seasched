from request import Request
import time


class Scheduler:

    def __init__(self, scheduler_params, prob_params, sim_params) -> None:
        # simuation_parameters
        self.sim_params = sim_params
        # probility_parameters
        self.prob_params = prob_params

        # alpha parameters for simulating request cost by poisson distribution
        self.alpha = scheduler_params['alpha']

    def schedule(self, req: Request):
        _cur_moment = time.time()-self.sim_params['start_time']
        req.arrive_moment = _cur_moment

        # parameters should be normalized first
        min_cost = self.prob_params['cost_params']['min_cost']
        max_cost = self.prob_params['cost_params']['max_cost']
        norm_arrive_moment = req.arrive_moment / self.sim_params['burst_time']
        norm_cost = (req.cost - min_cost) / (max_cost - min_cost)

        req.priority = norm_arrive_moment + (self.alpha * norm_cost)

        # print('Request{} arrive at time:{}, cost is {}'.format(
        #     req.id, req.arrive_moment, req.cost)
        # )
