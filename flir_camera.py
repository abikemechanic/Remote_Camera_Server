from BlackFlyCamera import Camera
import base_camera


class FlirCamera(base_camera.BaseCamera):
    def __init__(self, camera_index=0):
        super().__init__()

        self.cam = Camera.Camera(camera_index)

    def get_frame(self):
        return self.cam.get_frame()
