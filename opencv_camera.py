import cv2
import typing
from camera_base import CameraBase
import sys


class OpenCvCamera(CameraBase):
    def __init__(self, resolution: typing.Tuple[int, int], fps: int) -> None:
        super().__init__(fps)
        self.resolution = resolution
        self.cap: cv2.VideoCapture | None = None

    def _start(self):
        if self.cap is not None:
            self.cap.release()
        is_windows = sys.platform.startswith("win")
        cap_backend = cv2.CAP_DSHOW if is_windows else cv2.CAP_ANY
        self.cap = cv2.VideoCapture(0 + cap_backend)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, float(self.resolution[0]))
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, float(self.resolution[1]))
        self.cap.set(cv2.CAP_PROP_FPS, float(self.fps))

    def _stop(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def _read_frame(self) -> typing.Tuple[bool, cv2.typing.MatLike]:
        if self.cap is not None:
            return self.cap.read()
        return False, cv2.Mat([])

    def is_running(self) -> bool:
        return self.cap is not None and self.cap.isOpened()
