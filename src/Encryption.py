import numpy as np
import cv2

def encode(image):
    flag, buf = cv2.imencode("return.jpg", image, [cv2.IMWRITE_JPEG_QUALITY, 90])
    return buf.tobytes()

def decode(file):
    buf = file.read()
    x = np.fromstring(buf, dtype = 'uint8')
    image = cv2.imdecode(x, cv2.IMREAD_UNCHANGED)
    return image

def localDecode(buf):
    x = np.fromstring(buf, dtype = 'uint8')
    image = cv2.imdecode(x, cv2.IMREAD_UNCHANGED)
    return image
