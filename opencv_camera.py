import cv2
import typing
from camera_base import CameraBase
import sys
import numpy as np


class OpenCvCamera(CameraBase):
    def __init__(
        self,
        resolution: typing.Tuple[int, int] = (640, 480),
        fps: int = 30,
        index: int = 0,
        use_mjpeg: bool = True,
    ) -> None:
        self.resolution = resolution
        self.fps = fps
        self.index = index
        self.use_mjpeg = use_mjpeg
        self.cap: cv2.VideoCapture | None = None

    def _start(self):
        if self.cap is not None:
            self.cap.release()
        is_windows = sys.platform.startswith("win")
        cap_backend = cv2.CAP_DSHOW if is_windows else cv2.CAP_ANY
        self.cap = cv2.VideoCapture(self.index + cap_backend)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, float(self.resolution[0]))
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, float(self.resolution[1]))
        self.cap.set(cv2.CAP_PROP_FPS, float(self.fps))
        if self.use_mjpeg:
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))

    def _stop(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def read_frame(self) -> typing.Tuple[bool, cv2.typing.MatLike]:
        if self.cap is not None:
            success, frame = self.cap.read()
            return success, frame
        return False, np.array([])

    def is_running(self) -> bool:
        return self.cap is not None and self.cap.isOpened()
