import abc
import cv2
import typing


class CameraBase(abc.ABC):
    def __init__(self, fps: int) -> None:
        self.fps = fps

    def start(self) -> None:
        if self.is_running():
            return
        self._start()
        if not self.is_running():
            raise Exception("Failed to start camera")

    @abc.abstractmethod
    def _start(self) -> None:
        pass

    def stop(self):
        if not self.is_running():
            return
        self._stop()
        if self.is_running():
            raise Exception("Failed to stop camera")

    @abc.abstractmethod
    def _stop(self) -> None:
        pass

    @abc.abstractmethod
    def read_frame(self) -> bool:
        pass

    @abc.abstractmethod
    def is_running(self) -> bool:
        pass

    def __enter__(self) -> "CameraBase":
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.stop()
