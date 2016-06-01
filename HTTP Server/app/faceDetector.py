from app import app
from flask import request
from src import DetectObject
from scr import ImgManipulation as iManip
import cv2
import numpy as np

@app.route('/faceDetector', methods = ['GET'])
def atFaceDetector():
	return "This page is for finding faces in an image"

@app.route('/faceDetector', methods = ['POST'])
def postFaceDetector():
    print "Removing outer layer of file..."
    buf = request.files['image'].read()
    print "Success!"

    print "Removing inner layer of file..."
    x = np.fromstring(buf, dtype = 'uint8')
    image = cv2.imdecode(x, cv2.IMREAD_UNCHANGED)
    print "Success!"

    print "Attempting to find objects..."
    faceLocs = DetectObject.findObject(image,"Face")
    print "Success!"

    #Used only if making images for each face
    i = 0
    faces = []

    print "Drawing rectangles..."
    for (x, y, w, h) in faceLocs:
        #Crop out and scale the face
        faces[i] = iManip(image, x, y, w, h)
        i += 1

        #Draw box around the face
        cv2.rectangle(image, (x, y-int(h*0.1)), (x+w, int(y+h*1.1)), (0, 255, 0), 2)
    print "Success!"
    
    # Encode boxed image
    print "Encoding picture for response..."
    flag, buf = cv2.imencode("return.jpg", image, [cv2.IMWRITE_JPEG_QUALITY, 90])
    print "Success!"

    # Encode faces
    bufFaces = []
    i=0
    faceMap = {}
    for face in faces:
        flag, bufFaces[i] = cv2.imencode("return"+i+".jpg", face[i], [cv2.IMWRITE_JPEG_QUALITY, 90])
        i += 1
        faceMap['return'+i] = bufFaces[i].tobytes()

    # Uncomment to return locations of bounding boxes
    #return faceLocs.tobytes()

    # Uncomment to return original image with boxes drawn
    return buf.tobytes()

    # Uncomment to return map of face images
    return faceMap