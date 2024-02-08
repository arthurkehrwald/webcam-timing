import cv2
from create_camera import create_camera

if __name__ == "__main__":
    with create_camera() as cam:
        while True:
            success, frame = cam.read_frame()
            if success:
                cv2.imshow("Frame", frame)
            if cv2.waitKey(1) == ord('q'):
                break
