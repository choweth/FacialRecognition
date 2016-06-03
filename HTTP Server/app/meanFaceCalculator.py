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
    print "Request recieved at meanFaceCalculator"
    faces = []
    i = 0
    print "Loading files...\n"
    for key in request.files:
        buf = request.files[key].read()
        x = np.fromstring(buf, dtype = 'uint8')
        faces.append(cv2.imdecode(x, cv2.IMREAD_UNCHANGED))
	print "Loaded face " + str(i)
	i += 1
    print "\nAll files loaded successfully!\n"
    grayFaces = []
    i = 0
    print "Greyscaling faces...\n"
    for face in faces:
        grayFaces.append(iManip.grayFace(face))
	print "Greysclaed face " + str(i)
	i += 1
    print "\nAll faces greyscaled successfully!\n"

    print "Calculating mean face..."
    meanFace = averageFaces(grayFaces)
    print "Success!\n"

    print "Encoding response..."
    flag, buf = cv2.imencode("return.jpg", meanFace, [cv2.IMWRITE_JPEG_QUALITY, 90])
    print "Success!\n"
    return buf.tobytes()

def averageFaces(faces):
    HEIGHT = 600
    WIDTH = 500
    DEPTH = 3
    newPic = np.empty((HEIGHT,WIDTH,DEPTH), int)
    for i in range(HEIGHT):
        for j in range(WIDTH):
            avgVal = 0
            for l in range(len(faces)):
                avgVal = avgVal + faces[l][i,j,0]
            x = int((avgVal / len(faces)))
            for k in range(DEPTH):
                newPic[i,j,k] = x
    return newPic
