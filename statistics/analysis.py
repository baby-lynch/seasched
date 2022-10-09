import json
import sys
import os
from urllib import request
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


class Analysis:
    def __init__(self) -> None:
        # alpha value of each simulation result
        self.alphas = []
        # average response time of each simulation result
        self.avg_RTs = []
        # standard deviations of response times of each simulation result
        self.std_RTs = []
        '''
        # number of unscheduled requests
        self.ratios_unsched = []
        
        # number of requests who are treated in an unfair way of each simulation result
        self.nums_unfair = []
        '''


def analyze(stats: list):
    analysis = Analysis()

    #--------------- Calculation of Sim Results ---------------#
    for stat in stats:
        # alpha
        analysis.alphas.append(stat['alpha'])

        sched_requests = stat['sched_requests']
        RTs = []
        for sched_request in sched_requests:
            RTs.append(sched_request['response_time'])
        # calculate average response time
        analysis.avg_RTs.append(np.mean(RTs))
        # calculate standard deviation of response time
        analysis.std_RTs.append(np.std(RTs))

        '''
        # count number of unsched requests
        unsched_requests = stat['unsched_requests']
        requests = sched_requests + unsched_requests
        analysis.ratios_unsched.append(len(unsched_requests)/len(requests))
        '''

    #--------------- Evaluate Alpha based on Calculation ---------------#
    # alpha evaluation function : Q(alpha) = (1-w1-w2)*ratio_unsched + w1*avg_RT + w2*std_RT
    w = 0.5
    best_alpha = 0
    best_val = 1e9
    for i, alpha in enumerate(analysis.alphas):
        avgRT = analysis.avg_RTs[i]
        stdRT = analysis.std_RTs[i]
        '''
        ratio_unsched = analysis.ratios_unsched[i]
        norm_ratio_unsched = (ratio_unsched - min(analysis.ratios_unsched)) / \
            (max(analysis.ratios_unsched) - min(analysis.ratios_unsched))
            
        '''
        norm_avgRT = (avgRT - min(analysis.avg_RTs)) / \
            (max(analysis.avg_RTs) - min(analysis.avg_RTs))
        norm_stdRT = (stdRT - min(analysis.std_RTs)) / \
            (max(analysis.std_RTs) - min(analysis.std_RTs))

        val = (1-w)*norm_avgRT + w*norm_stdRT
        print("val:"+str(val))
        if val < best_val:
            best_val = min(best_val, val)
            best_alpha = alpha
    print("best alpha is:" + str(best_alpha))

    #--------------- Paint based on Calculation ---------------#
    fig, (latency, fairness) = plt.subplots(1, 2)
    fig.subplots_adjust(wspace=0.2)
    fig.set_size_inches(w=12, h=6)
    font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)

    #----- paint Latency -----#
    latency.plot(analysis.alphas, analysis.avg_RTs, color="blue",
                 linewidth=2, linestyle='-', marker='o')
    latency.set_title('Evaluation of Latency\n',
                      fontproperties=font, loc='center')
    latency.set_xlabel('Alpha', fontproperties=font)
    latency.set_ylabel('Average Response Time(s)', fontproperties=font)
    latency.set_xticks(analysis.alphas)
    for tick in latency.get_xticklabels():
        tick.set_rotation(300)
    latency.grid(axis='y')

    #----- paint fairness -----#
    fairness.plot(analysis.alphas, analysis.std_RTs, color="red",
                  linewidth=2, linestyle='-', marker='o')
    fairness.set_title('Evaluation of Fairness\n',
                       fontproperties=font, loc='center')
    fairness.set_xlabel('Alpha', fontproperties=font)
    fairness.set_ylabel('Standard Deviation of Response Time',
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
