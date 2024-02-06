import cv2
import typing
from plot import show_plot
from analyze import calc_stats, print_stats, get_resolution
from fileio import save_frame_times

WARMUP_FRAMES = 50
MEASURED_FRAMES = 500

# Camera settings, 0 to use default
CAMERA_INDEX = 0
DESIRED_FPS = 60
DESIRED_WIDTH = 2560
DESIRED_HEIGHT = 960
USE_MJPEG = False
CAP_BACKEND = cv2.CAP_DSHOW # CAP_DSHOW works best for Windows, in my experience


def get_current_time_ms() -> float:
    return cv2.getTickCount() / cv2.getTickFrequency() * 1000


def start_camera() -> cv2.VideoCapture:
    print("Starting camera...")
    cap = cv2.VideoCapture(CAMERA_INDEX + CAP_BACKEND)
    if DESIRED_FPS > 0:
        cap.set(cv2.CAP_PROP_FPS, DESIRED_FPS)
    if DESIRED_WIDTH > 0:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, DESIRED_WIDTH)
    if DESIRED_HEIGHT > 0:
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, DESIRED_HEIGHT)
    if USE_MJPEG:
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc("m", "j", "p", "g"))
    if not cap.isOpened():
        raise ValueError("Cannot open camera")
    return cap


def warmup_camera(cap: cv2.VideoCapture, frames: int):
    print(f"Skipping {frames} frames to warm up camera...")
    for _ in range(frames):
        cap.read()


def measure_frame_times(cap: cv2.VideoCapture, frames: int) -> typing.List[float]:
    print(f"Measuring timing of {frames} frames...")
    prev_time = get_current_time_ms()
    frame_times: typing.List[float] = []
    while cap.isOpened() and len(frame_times) < frames:
        success, image = cap.read()
        if success:
            timestamp = get_current_time_ms()
            frame_times.append(timestamp - prev_time)
            prev_time = timestamp
    return frame_times


if __name__ == "__main__":
    try:
        cap = start_camera()
    except ValueError as e:
        print(e)
        exit(1)

    width, height = get_resolution(cap)
    print(f"Opened camera with resolution: {width}x{height}")

    warmup_camera(cap, WARMUP_FRAMES)

    capture_start = get_current_time_ms()
    frame_times = measure_frame_times(cap, MEASURED_FRAMES)
    capture_end = get_current_time_ms()

    cap.release()

    stats = calc_stats(frame_times)
    print_stats(stats)
    save_frame_times(frame_times)
    show_plot(frame_times)  # This blocks until user closes plot window
