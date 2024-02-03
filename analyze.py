from dataclasses import dataclass
import typing
import sys
from fileio import read_frame_times


@dataclass
class Stats:
    capture_duration: float
    avg_frame_time: float
    avg_frame_rate: float
    mean_deviation: float


def calc_stats(frame_times: typing.List[float]) -> Stats:
    capture_duration = sum(frame_times)
    avg_frame_time = capture_duration / len(frame_times)
    avg_frame_rate = 1000 / avg_frame_time
    diff_from_avg = [abs(avg_frame_time - ft) for ft in frame_times]
    mean_deviation = sum(diff_from_avg) / len(diff_from_avg)
    return Stats(capture_duration, avg_frame_time, avg_frame_rate, mean_deviation)


def print_stats(stats: Stats):
    print(f"Capture duration: {stats.capture_duration:.2f} ms")
    print(f"Average frame time: {stats.avg_frame_time:.2f} ms")
    print(f"Average frame rate: {stats.avg_frame_rate:.2f} fps")
    print(f"Mean deviation: {stats.mean_deviation:.2f} ms")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing path to csv file!\nUsage: python plot.py <frame_times.csv>")
        exit(1)
    filename = sys.argv[1]
    frame_times = read_frame_times(filename)
    stats = calc_stats(frame_times)
    print_stats(stats)
