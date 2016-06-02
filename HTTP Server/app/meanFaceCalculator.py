import sys
sys.path.insert(0, "/root/know-that-face/know-that-face/HTTP Server/src")

from app import app
from flask import request
from src import ImgManipulation as iManip
import cv2
import numpy as np

@app.route('/meanFaceCalculator', methods = ['GET'])
def atMeanFaceCalc():
	return "This page is for calculating mean faces"

@app.route('/meanFaceCalculator', methods = ['POST'])
def postMeanFaceCalc():
    # Read the faces from the files sent
    faces = []
    i =0
    for key in request.files:
        buf = request.files[key].read()
        x = np.fromstring(buf, dtype = 'uint8')
        faces[i] = cv2.imdecode(x, cv2.IMREAD_UNCHANGED)
        i += 1

    meanFace = iManip.averageFaces(faces)

    flag, buf = cv2.imencode("return.jpg", meanFace, [cv2.IMWRITE_JPEG_QUALITY, 90])

    return buf.tobytes()