import json
import sys
import os
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


class Analysis:
    def __init__(self) -> None:
        # alpha value of each simulation result
        self.alphas = []
        # average response time of each simulation result
        self.avg_RTs = []
        # number of requests who are treated in an unfair way of each simulation result
        self.nums_unfair = []


def analyze(stats: list):
    analysis = Analysis()

    #--------------- Calculation of Sim Results ---------------#
    for stat in stats:
        # alpha
        analysis.alphas.append(stat['alpha'])

        # calculate average response time
        sched_requests = stat['sched_requests']
        RTs = []
        for sched_request in sched_requests:
            RTs.append(sched_request['response_time'])
        analysis.avg_RTs.append(sum(RTs)/len(RTs))

        # count number of unfairly treated requests
        unsched_requests = stat['unsched_requests']
        num_unfair_treated_req = 0
        for unsched_request in unsched_requests:
            if unsched_request['wait_time'] > analysis.avg_RTs[-1]:
                num_unfair_treated_req += 1
        analysis.nums_unfair.append(num_unfair_treated_req)

    #--------------- Evaluate Alpha based on Calculation ---------------#
    # alpha evaluation function : Q(alpha) = (1-w)*avg_RT + w*num_unfair
    w = 0.5
    best_alpha = 0
    best_val = 1e9
    for i, alpha in enumerate(analysis.alphas):
        avgRT = analysis.avg_RTs[i]
        num_unfair = analysis.nums_unfair[i]

        norm_avgRT = (avgRT - min(analysis.avg_RTs)) / \
            (max(analysis.avg_RTs) - min(analysis.avg_RTs))
        norm_num_unfair = (num_unfair - min(analysis.nums_unfair)) / \
            (max(analysis.nums_unfair) - min(analysis.nums_unfair))

        val = (1-w)*norm_avgRT + w*norm_num_unfair
        print("val:"+str(val))
        if val < best_val:
            best_val = min(best_val, val)
            best_alpha = alpha
    print("best alpha is:" + str(best_alpha))

    #--------------- Paint based on Calculation ---------------#
    fig, (efficiency, fairness) = plt.subplots(1, 2)
    fig.subplots_adjust(wspace=0.2)
    fig.set_size_inches(w=12, h=6)
    font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)

    #----- paint efficiency -----#
    efficiency.plot(analysis.alphas, analysis.avg_RTs, color="blue",
                    linewidth=2, linestyle='-', marker='o')
    efficiency.set_title('Evaluation of Efficiency\n',
                         fontproperties=font, loc='center')
    efficiency.set_xlabel('Alpha', fontproperties=font)
    efficiency.set_ylabel('Average Response Time(s)', fontproperties=font)
    efficiency.set_xticks(analysis.alphas)
    for tick in efficiency.get_xticklabels():
        tick.set_rotation(300)
    efficiency.grid(axis='y')

    #----- paint fairness -----#
    fairness.plot(analysis.alphas, analysis.nums_unfair, color="red",
                  linewidth=2, linestyle='-', marker='o')
    fairness.set_title('Evaluation of Fairness\n',
                       fontproperties=font, loc='center')
    fairness.set_xlabel('Alpha', fontproperties=font)
    fairness.set_ylabel('Number of Unfairly-Treated Requests',
                        fontproperties=font)
    fairness.set_xticks(analysis.alphas)
    for tick in fairness.get_xticklabels():
        tick.set_rotation(300)
    fairness.grid(axis='y')

    plt.show()


if __name__ == "__main__":
    cur_dir = (sys.argv[0]).rstrip("analysis.py")
    stats = []

    filenames = []

    # collect stats.json files under current directory and sort them in ascending order by alpha
    for filename in os.listdir(cur_dir):
        if filename.startswith("stats"):
            filenames.append(filename)
    filenames.sort(key=lambda x: float((x.lstrip("stats")).rstrip(".json")))

    # extract data from stats.json files
    for filename in filenames:
        with open(cur_dir+filename, 'r') as f:
            stat = json.load(f)
            stats.append(stat)

    analyze(stats)
