import cv2
import typing
from plot import show_plot
from analyze import calc_stats, print_stats, get_resolution
from fileio import save_frame_times
import time
from camera_base import CameraBase
from opencv_camera import OpenCvCamera
from oak_camera import OakCamera, StereoMode
from depthai import MonoCameraProperties
daiRes = MonoCameraProperties.SensorResolution

WARMUP_FRAMES = 50
MEASURED_FRAMES = 500

# Camera settings, 0 to use default
CAMERA_INDEX = 0
DESIRED_FPS = 60
DESIRED_WIDTH = 2560
DESIRED_HEIGHT = 960
USE_MJPEG = False
CAP_BACKEND = cv2.CAP_DSHOW  # CAP_DSHOW works best for Windows, in my experience


def get_current_time_ms() -> float:
    return time.time() * 1000


def warmup_camera(cam: CameraBase, frames: int) -> None:
    print(f"Skipping {frames} frames to warm up camera...")
    frames_received = 0
    while frames_received < frames:
        success, frame = cam.read_frame()
        if success:
            frames_received += 1


def measure_frame_times(cam: CameraBase, frames: int) -> typing.List[float]:
    print(f"Measuring timing of {frames} frames...")
    prev_time = get_current_time_ms()
    frame_times: typing.List[float] = []
    while len(frame_times) < frames:
        success, image = cam.read_frame()
        if success:
            timestamp = get_current_time_ms()
            frame_times.append(timestamp - prev_time)
            prev_time = timestamp
    return frame_times


if __name__ == "__main__":
    with OakCamera(daiRes.THE_400_P, fps=120, stereo_mode=StereoMode.STEREO) as cam:
        success, frame = cam.read_frame()
        #width, height = get_resolution(frame)
        #print(f"Opened camera with resolution: {width}x{height}")

        warmup_camera(cam, WARMUP_FRAMES)

        capture_start = get_current_time_ms()
        frame_times = measure_frame_times(cam, MEASURED_FRAMES)
        capture_end = get_current_time_ms()

    stats = calc_stats(frame_times)
    print_stats(stats)
    save_frame_times(frame_times)
    show_plot(frame_times)  # This blocks until user closes plot window
