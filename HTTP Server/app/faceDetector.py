import sys
sys.path.insert(0, "/root/know-that-face/know-that-face/")

from app import app
from flask import request
import DetectObject
import ImgManipulation as iManip
import cv2
import numpy as np

@app.route('/faceDetector', methods = ['GET'])
def atFaceDetector():
	return "This page is for finding faces in an image"

@app.route('/faceDetector', methods = ['POST'])
def postFaceDetector():
    print "Request recieved at faceDetector\n"

    print "Loading file..."
    buf = request.files['image'].read()
    x = np.fromstring(buf, dtype = 'uint8')
    image = cv2.imdecode(x, cv2.IMREAD_UNCHANGED)
    print "Success!\n"

    print "Attempting to find objects..."
    faceLocs = DetectObject.findObject(image,"Face")
    print "Success!\n"

    #Used only if making images for each face
    #faces = []

    #print "Drawing rectangles..."
    #for (x, y, w, h) in faceLocs:
        #Crop out and scale the face
        #faces.append(iManip(image, x, y, w, h))

        #Draw box around the face
    #    cv2.rectangle(image, (x, y-int(h*0.1)), (x+w, int(y+h*1.1)), (0, 255, 0), 2)
    #print "Success!"
    print "Face locations:"
    print faceLocs    
    print
    # Encode boxed image
    print "Encoding response..."
    flag, buf = cv2.imencode("return.jpg", image, [cv2.IMWRITE_JPEG_QUALITY, 90])
    print "Success!\n"

    # Encode faces
    #bufFaces = []
    #faceMap = {}
    #i=0
    #for face in faces:
        #flag, buffer = cv2.imencode("return"+i+".jpg", face[i], [cv2.IMWRITE_JPEG_QUALITY, 90])
	#bufFaces.append(buffer)
        #faceMap['return'+i] = bufFaces[i].tobytes()
	#i += 1

    # Uncomment to return locations of bounding boxes
    return faceLocs.tobytes()

    # Uncomment to return original image with boxes drawn
    #return buf.tobytes()

    # Uncomment to return map of face images
    #return faceMap
