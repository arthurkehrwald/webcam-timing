from camera_base import CameraBase
import depthai as dai
import cv2
import typing
from enum import Enum
import numpy as np


class StereoMode(Enum):
    STEREO = 0
    LEFT_ONLY = 1
    RIGHT_ONLY = 2


class OakResolution(Enum):
    P800 = dai.MonoCameraProperties.SensorResolution.THE_800_P
    P720 = dai.MonoCameraProperties.SensorResolution.THE_720_P
    P400 = dai.MonoCameraProperties.SensorResolution.THE_400_P


class OakCamera(CameraBase):
    def __init__(
        self,
        resolution: OakResolution,
        fps: int,
        qsize: int = 1,
        qblock: bool = False,
        stereo_mode: StereoMode = StereoMode.STEREO,
    ) -> None:
        super().__init__(fps)
        self.resolution = resolution
        self.device: dai.Device | None = None
        self.left_queue: dai.DataOutputQueue | None = None
        self.right_queue: dai.DataOutputQueue | None = None
        self.qsize = qsize
        self.qblock = qblock
        self.stereo_mode = stereo_mode
        self.empty_frame = cv2.Mat(np.array([]))
        self.read_left = self.stereo_mode != StereoMode.RIGHT_ONLY
        self.read_right = self.stereo_mode != StereoMode.LEFT_ONLY

    def _start(self):
        pipeline = self._create_pipeline()
        self.device = dai.Device(pipeline)
        self.device.startPipeline()
        if self.read_left:
            self.left_queue = self.device.getOutputQueue(
                name=dai.CameraBoardSocket.LEFT.name,
                maxSize=self.qsize,
                blocking=self.qblock,
            )
        if self.read_right:
            self.right_queue = self.device.getOutputQueue(
                name=dai.CameraBoardSocket.RIGHT.name,
                maxSize=self.qsize,
                blocking=self.qblock,
            )

    def _stop(self):
        if self.device is not None:
            self.device.close()
            self.device = None
            self.left_queue = None
            self.right_queue = None

    def read_frame(self) -> bool:
        if (self.read_left and self.left_queue is None) or (
            self.read_right and self.right_queue is None
        ):
            raise ValueError("Camera is not running. Call start first")
        need_left = self.read_left
        need_right = self.read_right
        while need_left or need_right:
            if self.left_queue is not None and need_left:
                l = self.left_queue.tryGet()
                if l is not None:
                    need_left = False
            if self.right_queue is not None and need_right:
                r = self.right_queue.tryGet()
                if r is not None:
                    need_right = False
        return True

    def is_running(self) -> bool:
        return self.device is not None and self.device.isPipelineRunning()

    def _create_pipeline(self) -> dai.Pipeline:
        pipeline = dai.Pipeline()
        pipeline.setXLinkChunkSize(0)

        def add_cam(socket: dai.CameraBoardSocket):
            cam = pipeline.createMonoCamera()
            cam.setBoardSocket(socket)
            cam.setResolution(self.resolution.value)
            cam.setFps(float(self.fps))
            xout = pipeline.createXLinkOut()
            xout.setStreamName(socket.name)
            cam.raw.link(xout.input)

        if self.stereo_mode != StereoMode.RIGHT_ONLY:
            add_cam(dai.CameraBoardSocket.LEFT)
        if self.stereo_mode != StereoMode.LEFT_ONLY:
            add_cam(dai.CameraBoardSocket.RIGHT)
        return pipeline

    def convert_to_cv_frame(self, data: dai.ADatatype) -> cv2.typing.MatLike:
        img_frame = typing.cast(dai.ImgFrame, data)
        obj = img_frame.getCvFrame()
        mat_like = typing.cast(cv2.typing.MatLike, obj)
        return mat_like
