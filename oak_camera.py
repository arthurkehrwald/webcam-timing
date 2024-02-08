from camera_base import CameraBase
import depthai as dai
import cv2
import typing
from enum import Enum
import numpy as np
from threading import Thread


class OakRgbResolution(Enum):
    P1080 = dai.ColorCameraProperties.SensorResolution.THE_1080_P
    P2160 = dai.ColorCameraProperties.SensorResolution.THE_4_K
    P3040 = dai.ColorCameraProperties.SensorResolution.THE_12_MP


class OakMonoResolution(Enum):
    P800 = dai.MonoCameraProperties.SensorResolution.THE_800_P
    P720 = dai.MonoCameraProperties.SensorResolution.THE_720_P
    P400 = dai.MonoCameraProperties.SensorResolution.THE_400_P


class OakCamera(CameraBase):
    def __init__(
        self,
        enable_rgb: bool = True,
        enable_left: bool = False,
        enable_right: bool = False,
        rgb_resolution: OakRgbResolution = OakRgbResolution.P1080,
        rgb_fps: float = 30,
        mono_resolution: OakMonoResolution = OakMonoResolution.P720,
        mono_fps: float = 30,
        qsize: int = 1,
        qblock: bool = False,
    ) -> None:
        self.device: dai.Device | None = None
        self.queues: typing.List[dai.DataOutputQueue] = []
        self.qsize = qsize
        self.qblock = qblock
        self.sockets: typing.List[dai.CameraBoardSocket] = []
        if enable_rgb:
            self.sockets.append(dai.CameraBoardSocket.CAM_A)
        if enable_left:
            self.sockets.append(dai.CameraBoardSocket.CAM_B)
        if enable_right:
            self.sockets.append(dai.CameraBoardSocket.CAM_C)
        self.rgb_resolution = rgb_resolution
        self.rgb_fps = rgb_fps
        self.mono_resolution = mono_resolution
        self.mono_fps = mono_fps
        self.empty_frame = cv2.Mat(np.array([]))

    def _start(self):
        pipeline = self._create_pipeline()
        self.device = dai.Device(pipeline)
        self.device.startPipeline()
        for socket in self.sockets:
            q = self.device.getOutputQueue(
                name=socket.name,
                maxSize=self.qsize,
                blocking=self.qblock,
            )
            self.queues.append(q)

    def _stop(self):
        if self.device is not None:
            self.device.close()
            self.device = None
            self.left_queue = None
            self.right_queue = None

    def read_frame(self) -> typing.Tuple[bool, cv2.typing.MatLike]:
        frames: typing.List[cv2.typing.MatLike | None] = [None] * len(self.queues)
        read_threads: typing.List[Thread] = []
        for i, q in enumerate(self.queues):
            t = Thread(target=self._read_queue_thread, args=[q, frames, i])
            t.start()
            read_threads.append(t)
        for t in read_threads:
            t.join()
        framestack = np.hstack([f for f in frames if f is not None])
        return True, framestack

    def _read_queue_thread(
        self,
        q: dai.DataOutputQueue,
        results: typing.List[cv2.typing.MatLike],
        index: int,
    ) -> None:
        results[index] = self.convert_to_cv_frame(q.get())

    def is_running(self) -> bool:
        return self.device is not None and self.device.isPipelineRunning()

    def _create_pipeline(self) -> dai.Pipeline:
        pipeline = dai.Pipeline()
        pipeline.setXLinkChunkSize(0)

        def _add_cam(socket: dai.CameraBoardSocket):
            xout = pipeline.createXLinkOut()
            xout.setStreamName(socket.name)
            is_rgb = socket in [
                dai.CameraBoardSocket.CAM_A,
                dai.CameraBoardSocket.RGB,
                dai.CameraBoardSocket.CENTER,
            ]
            if is_rgb:
                cam = pipeline.createColorCamera()
                cam.setResolution(self.rgb_resolution.value)
                cam.preview.link(xout.input)
            else:
                cam = pipeline.createMonoCamera()
                cam.setResolution(self.mono_resolution.value)
                cam.raw.link(xout.input)
            cam.setBoardSocket(socket)
            cam.setFps(self.rgb_fps if is_rgb else self.mono_fps)

        for socket in self.sockets:
            _add_cam(socket)
        return pipeline

    def convert_to_cv_frame(self, data: dai.ADatatype) -> cv2.typing.MatLike:
        img_frame = typing.cast(dai.ImgFrame, data)
        obj = img_frame.getCvFrame()
        mat_like = typing.cast(cv2.typing.MatLike, obj)
        return mat_like
