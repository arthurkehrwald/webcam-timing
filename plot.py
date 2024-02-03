import matplotlib.pyplot as plt
import sys
import typing
import os
from fileio import read_frame_times


def show_plot(frame_times: typing.List[float], name: str = "Frame timings"):
    plt.plot(frame_times)
    plt.xlabel("Frame number")
    plt.ylabel("Frame time (ms)")
    plt.title(name)
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing path to csv file!\nUsage: python plot.py <frame_times.csv>")
        exit(1)
    filename = sys.argv[1]
    frame_times = read_frame_times(filename)
    name = os.path.basename(filename).split(".")[0]
    show_plot(frame_times, name)
