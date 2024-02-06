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


qsize = 1
qblock = False


class OakCamera(CameraBase):
    def __init__(
        self,
        resolution: dai.MonoCameraProperties.SensorResolution,
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

    def _start(self):
        pipeline = self._create_pipeline(self.resolution, self.fps)
        self.device = dai.Device(pipeline)
        self.device.startPipeline()
        if self.stereo_mode != StereoMode.RIGHT_ONLY:
            self.left_queue = self.device.getOutputQueue(
                name=dai.CameraBoardSocket.LEFT.name, maxSize=qsize, blocking=qblock
            )
        if self.stereo_mode != StereoMode.LEFT_ONLY:
            self.right_queue = self.device.getOutputQueue(
                name=dai.CameraBoardSocket.RIGHT.name, maxSize=qsize, blocking=qblock
            )

    def _stop(self):
        if self.device is not None:
            self.device.close()
            self.device = None
            self.left_queue = None
            self.right_queue = None

    def _read_frame(self) -> typing.Tuple[bool, cv2.typing.MatLike]:
        if (self.stereo_mode != StereoMode.RIGHT_ONLY and self.left_queue is None) or (
            self.stereo_mode != StereoMode.LEFT_ONLY and self.right_queue is None
        ):
            raise ValueError("Camera is not running. Call start first")
        l = None
        if self.left_queue is not None:
            l = self.left_queue.tryGet()
        r = None
        if self.right_queue is not None:
            r = self.right_queue.tryGet()
        l = self.convert_to_cv_frame(l) if l is not None else None
        r = self.convert_to_cv_frame(r) if r is not None else None
        if l is not None and r is not None:
            #return True, cv2.hconcat([l, r])
            return True, l
        elif l is not None:
            return True, l
        elif r is not None:
            return True, r
        return False, self.empty_frame

    def is_running(self) -> bool:
        return self.device is not None and self.device.isPipelineRunning()

    def _create_pipeline(
        self, resolution: dai.MonoCameraProperties.SensorResolution, fps: int
    ) -> dai.Pipeline:
        pipeline = dai.Pipeline()
        pipeline.setXLinkChunkSize(0)

        def add_cam(socket: dai.CameraBoardSocket):
            cam = pipeline.createMonoCamera()
            cam.setBoardSocket(socket)
            cam.setResolution(resolution)
            cam.setFps(float(fps))
            xout = pipeline.createXLinkOut()
            xout.setStreamName(socket.name)
            cam.raw.link(xout.input)

        if self.stereo_mode != StereoMode.RIGHT_ONLY:
            add_cam(dai.CameraBoardSocket.LEFT)
        if self.stereo_mode != StereoMode.LEFT_ONLY:
            add_cam(dai.CameraBoardSocket.RIGHT)
        return pipeline

    def get_dai_mono_resolution(
        self, width: int, height: int
    ) -> dai.MonoCameraProperties.SensorResolution:
        DAI_MONO_HEIGHTS = {
            800: dai.MonoCameraProperties.SensorResolution.THE_800_P,
            720: dai.MonoCameraProperties.SensorResolution.THE_720_P,
            480: dai.MonoCameraProperties.SensorResolution.THE_480_P,
            400: dai.MonoCameraProperties.SensorResolution.THE_400_P,
        }
        closest_res = min(DAI_MONO_HEIGHTS.keys(), key=lambda x: abs(x - height))
        return DAI_MONO_HEIGHTS[closest_res]

    def convert_to_cv_frame(self, data: dai.ADatatype) -> cv2.typing.MatLike:
        img_frame = typing.cast(dai.ImgFrame, data)
        obj = img_frame.getCvFrame()
        mat_like = typing.cast(cv2.typing.MatLike, obj)
        return mat_like
