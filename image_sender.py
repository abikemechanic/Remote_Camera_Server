import imagezmq
import zmq
import func_timeout
import time


class ImageSender:
    def __init__(self, host_address, sender_id):
        self.host_address = host_address
        self.sender_id = sender_id
        self.sender: imagezmq.ImageSender = None
        self.connected = False
        self.rest_time = 1/5

        self.connect_to_host()

    @func_timeout.func_set_timeout(2)
    def connect_to_host(self):
        if not self.connected:
            self.sender = None
            try:
                self.sender = imagezmq.ImageSender(
                    connect_to=f'tcp://{self.host_address}:555')
                self.connected = True
                return True

            except zmq.error.ZMQError as ex:
                self.connected = False
                return False

    def send_image_without_timeout(self, jpg_buffer):
        server_reply = self.sender.send_jpg(self.sender_id, jpg_buffer)

    @func_timeout.func_set_timeout(2)
    def send_image_with_timeout(self, jpg_buffer):
        if self.connected:
            server_reply = self.sender.send_jpg(self.sender_id, jpg_buffer)
            time.sleep(self.rest_time)
            return server_reply
        else:
            if self.connect_to_host():
                server_reply = self.sender.send_jpg(
                    self.sender_id,
                    jpg_buffer
                )
                time.sleep(self.rest_time)
                return server_reply
            else:
                return False

