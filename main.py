import cv2
import imagezmq
import zmq
import time
import func_timeout
import json
from flir_camera import FlirCamera


def get_config():
    with open('server_config.cfg') as f:
        return json.load(f)


def connect_to_zmq_server(address):
    try:
        sndr = imagezmq.ImageSender(connect_to=f'tcp://{address}:555')
        return sndr
    except zmq.error.ZMQError as ex:
        print(ex)
        time.sleep(10)
        return False


@func_timeout.func_set_timeout(2)
def send_image_to_hub(jpg_img):
    reply_from_server = sender.send_jpg(sender_name, jpg_img)
    print(reply_from_server)


@func_timeout.func_set_timeout(2)
def get_format_image():
    img = vid_cam.get_frame()
    time_string = time.strftime('%H:%M:%S', time.localtime())

    # black outline
    cv2.putText(img, text=time_string, org=(10, 40),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 0),
                thickness=4)

    # white text
    cv2.putText(img, text=time_string, org=(10, 40),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255,255,255),
                thickness=1)

    return img


def get_camera(camera_spec):
    if camera_spec == 'Blackfly':
        return FlirCamera();
    elif camera_spec == 'USB':
        return cv2.VideoCapture(0)
    else:
        raise ValueError("Need a camera specification in the config")


if __name__ == '__main__':
    cfg = get_config()
    sender_name = cfg['sender_name']
    server_address = cfg['server_address']

    sender = False
    while not sender:
        sender = connect_to_zmq_server(server_address)

    vid_cam = get_camera(cfg['camera_type'])

    while 1:
        try:
            ret_code, jpg = cv2.imencode('.jpg', get_format_image(), [int(cv2.IMWRITE_JPEG_QUALITY), 95])
            send_image_to_hub(jpg)
            time.sleep(1/28)

        except cv2.error as ex:
            print('cv2.error')
            print(ex)

        except func_timeout.FunctionTimedOut as ex:
            print(ex)
            del sender
            del vid_cam

            vid_cam = get_camera(cfg['camera_type'])
            sender = connect_to_zmq_server(server_address)

