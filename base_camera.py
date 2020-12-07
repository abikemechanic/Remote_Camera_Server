

class BaseCamera:

    def __init__(self):
        pass

    def get_frame(self):
        raise ValueError("Needs to be implemented in child class")
