class Request:

    def __init__(self, id, cost, create_moment, creator) -> None:
        # request id
        self.id = id
        # cost, ranging from 1024 ~ 1024*1024 bytes, was simulated by poisson distribution
        self.cost = cost

        # for debug's sake
        self.create_moment = create_moment
        self.creator = creator

        # gaps between diffirent arrive moment was simulated by expotential distribution
        self.arrive_moment: float
        # the moment when request was scheduled, i.e. deque
        self.sched_moment: float
        # finish_time = sched_moment + service_time
        self.finish_moment: float

        # response_time = sched_moment - arrive_moment
        self.response_time: float
        # service_time = cost / uplink_bandwidth
        self.service_time: float
        # this property is to be calculated for requests who are unscheduled during the whole simulation
        # wait_time = sim_time - arrive_moment
        self.wait_time: float

        # priority = arrive_time + alpha * cost
        self.priority: float

        return

    def __lt__(self, other):
        return self.priority < other.priority
