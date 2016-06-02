import sys
sys.path.insert(0, "/root/know-that-face/know-that-face/HTTP Server/src")

from app import app
from flask import request
import ImgManipulation as iManip
import cv2
import numpy as np

@app.route('/meanFaceCalculator', methods = ['GET'])
def atMeanFaceCalc():
	return "This page is for calculating mean faces"

@app.route('/meanFaceCalculator', methods = ['POST'])
def postMeanFaceCalc():
    # Read the faces from the files sent
    faces = []
    for key in request.files:
        buf = request.files[key].read()
        x = np.fromstring(buf, dtype = 'uint8')
        faces.append(cv2.imdecode(x, cv2.IMREAD_UNCHANGED))
    grayFaces = []
    for face in faces:
        grayFaces.append(iManip.grayFace(face))

    meanFace = averageFaces(grayFaces)

    flag, buf = cv2.imencode("return.jpg", meanFace, [cv2.IMWRITE_JPEG_QUALITY, 90])

    return buf.tobytes()

def averageFaces(faces):
    newPic = numpy.empty((HEIGHT,WIDTH,DEPTH), int)
    for i in range(HEIGHT):
        for j in range(WIDTH):
            avgVal = 0
            for l in range(len(faces)):
                avgVal = avgVal + faces[l,i,j,0]
            x = int((avgVal / len(faces)))
            for k in range(DEPTH):
                newPic[i,j,k] = x
    return newPic
