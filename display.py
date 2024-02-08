import cv2
from opencv_camera import OpenCvCamera
from oak_camera import OakCamera, OakRgbResolution, OakMonoResolution, OakCameraSockets

if __name__ == "__main__":
    with OakCamera(
        sockets=OakCameraSockets.LEFT_AND_RIGHT,
        mono_resolution=OakMonoResolution.P400,
        mono_fps=100,
    ) as cam:
        while True:
            success, frame = cam.read_frame()
            if success:
                cv2.imshow("Frame", frame)
            if cv2.waitKey(1) == ord('q'):
                break
