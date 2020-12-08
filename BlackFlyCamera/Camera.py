import simple_pyspin
from PIL import Image


class Camera:
    def __init__(self, camera_index=0):
        self._cam_index = camera_index

        self.cam = simple_pyspin.Camera(index=self._cam_index)
        self.cam.init()
        self._init_camera()
        self.cam.start()

# region Properties

    @property
    def Width(self):
        return self.cam.Width

    @Width.setter
    def Width(self, value):
        if type(value) != int:
            raise ValueError
        self.cam.Width = value

    @property
    def Height(self):
        return self.cam.Height

    @Height.setter
    def Height(self, value):
        if value is not int:
            raise ValueError('Only integers accepted')
        self.cam.Height = value

    @property
    def X_Offset(self):
        return self.cam.OffsetX

    @X_Offset.setter
    def X_Offset(self, value):
        if value is not int:
            raise ValueError('Only integers accepted')
        self.cam.OffsetX = value

    @property
    def Y_Offset(self):
        return self.cam.OffsetY

    @Y_Offset.setter
    def Y_Offset(self, value):
        if value is not int:
            raise TypeError('Only integers accepted')
        self.cam.OffsetY = value

# endregion

    def _init_camera(self):
        try:
            self.cam.PixelFormat = 'BGR8'
            self.cam.Height = 800
            self.cam.Width = 600
        except simple_pyspin.CameraError as ex:
            self.cam.start()
            self.cam.stop()
            self._init_camera()

    def get_frame(self):
        return self.cam.get_array()

    def get_PIL_image(self):
        frame = self.get_frame()
        return Image.fromarray(frame)

    def end_camera(self):
        self.cam.close()


