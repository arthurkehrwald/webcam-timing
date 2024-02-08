from camera_base import CameraBase
from opencv_camera import OpenCvCamera
from oak_camera import OakCamera, OakRgbResolution, OakMonoResolution, OakCameraSockets

def create_camera() -> CameraBase:
    # return OakCamera()
    return OpenCvCamera()