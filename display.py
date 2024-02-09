import pygame
from create_camera import create_camera
import cv2
import numpy as np
from analyze import get_resolution


if __name__ == "__main__":

    pygame.init()
    with create_camera() as cam:
        # Fit window to camera resolution
        success, frame = cam.read_frame()
        if success:
            window_size = get_resolution(frame)
        else:
            window_size = (1280, 720)
        screen = pygame.display.set_mode(window_size)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            success, frame = cam.read_frame()
            if success:
                screen.fill("black")
                # Adjust to pygame coordinate system and color format
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = np.fliplr(frame)
                frame = np.rot90(frame)
                frame = pygame.surfarray.make_surface(frame)
                # Blit the frame to the screen
                screen.blit(frame, (0, 0))
                pygame.display.flip()

        pygame.quit()
