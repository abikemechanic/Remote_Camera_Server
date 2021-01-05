import cv2
import imagezmq
import zmq
import time
import func_timeout
import json
from image_sender import ImageSender


def get_config():
    with open('server_config.cfg') as f:
        return json.load(f)

@func_timeout.func_set_timeout(2)
def get_format_image():
    if cfg['camera_type'] == "Blackfly":
        img = vid_cam.get_frame()
    else:
        ret, img = vid_cam.read()

    time_string = time.strftime('%H:%M:%S', time.localtime())

    # black outline
    cv2.putText(img, text=time_string, org=(10, 40),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 0),
                thickness=4)

    # white text
    cv2.putText(img, text=time_string, org=(10, 40),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255,255,255),
                thickness=1)

    # cv2.imshow('t', img)
    # print(time.time())
    return img


def get_camera(camera_spec, recursion_count=0):
    if camera_spec == 'Blackfly':
        # import FlirCamera only if necessary
        # it is difficult to install the needed libraries and I don't want to everytime
        from flir_camera import FlirCamera
        return FlirCamera()
    elif camera_spec == 'USB':
        return cv2.VideoCapture(0)
    else:
        raise ValueError("Need a camera specification in the config")


if __name__ == '__main__':
    cfg = get_config()
    sender_name = cfg['sender_name']
    server_address = cfg['server_address']

    sender = ImageSender(server_address, sender_name)

    vid_cam = get_camera(cfg['camera_type'])

    while 1:
        try:
            if sender is None:
                sender = ImageSender(server_address, sender_name)

            ret_code, jpg = cv2.imencode('.jpg', get_format_image(), [int(cv2.IMWRITE_JPEG_QUALITY), 95])
            resp = sender.send_image_with_timeout(jpg)
        except func_timeout.FunctionTimedOut as ex:
            print(ex)

        except cv2.error as ex:
            print(ex)

        except zmq.error.ZMQError as ex:
            print(ex)
            sender = None

        except AttributeError:
            sender = None
            print("Attribure Error")
            time.sleep(10)


