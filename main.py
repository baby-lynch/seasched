from simulation import Simulation
import json
import sys
import os


def update_json(filepath: str, alpha: float):
    data = {}
    # read json and updatedata
    with open(filepath, 'rb') as f:
        data = json.load(f)
        data["scheduler_params"]["alpha"] = alpha
    f.close()
    # print(data)

    # write back data to json file
    with open(filepath, 'w') as f:
        json.dump(data, f)
    f.close()


def init():
    cur_dir = (sys.argv[0]).rstrip("main.py")
    stats_dir = cur_dir + "statistics/"
    # remove old stats.json files first
    for filename in os.listdir(stats_dir):
        if filename.startswith("stats"):
            print(filename)
            os.remove(stats_dir+filename)


if __name__ == "__main__":
    alphas = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6, 7, 8, 9, 10]
    # alphas = [0, 0.2, 1]

    init()

    for alpha in alphas:
        update_json("sim.json", alpha)
        print("******* Simulation (alpha = " + str(alpha) + ")" + " Starts *******")
        sim = Simulation()
        sim.run()
        print("******* Simulation (alpha = " + str(alpha) + ")" + " Ends *******\n")
