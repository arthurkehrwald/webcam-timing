import typing
import time
import os


def save_frame_times(frame_times: typing.List[float]):
    CSV_DIR = "measurements"
    if not os.path.exists(CSV_DIR):
        os.mkdir(CSV_DIR)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = os.path.join(CSV_DIR, f"frame_times_{timestamp}.csv")
    with open(filename, "w") as f:
        for d in frame_times:
            f.write(str(d) + "\n")


def read_frame_times(filename: str) -> typing.List[float]:
    frame_times: typing.List[float] = []
    with open(filename) as f:
        for line in f:
            frame_times.append(float(line))
    return frame_times
