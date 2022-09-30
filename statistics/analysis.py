import json
import sys
import os
import time
import numpy as np
from numpy import random
import matplotlib.pyplot as plt


class Axis:
    def __init__(self, name: str, data: list) -> None:
        self.name = name
        self.data = data


def paint(x_axis: Axis, y_axis: Axis):
    plt.xlabel(x_axis.name)
    plt.ylabel(y_axis.name)
    plt.plot(x_axis.data, y_axis.data)
    plt.show()


def analyze_RT(stats: list):
    avg_RTs = []
    alphas = []

    for stat in stats:
        # alpha
        alphas.append(stat['alpha'])

        # calculate average response time
        requests = stat['requests']
        RTs = []
        for request in requests:
            RTs.append(request['response_time'])
        avg_RTs.append(sum(RTs)/len(RTs))

    # print(alphas)
    # print(avg_RTs)
    paint(Axis("alpha", alphas), Axis("Average Response Time", avg_RTs))


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

    analyze_RT(stats)
