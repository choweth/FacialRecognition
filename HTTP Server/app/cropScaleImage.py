import sys
sys.path.insert(0, "/root/know-that-face/know-that-face/HTTP Server/src")

from app import app
from flask import request
import ImgManipulation as iManip
import cv2
import numpy as np

@app.route('/cropScale', methods = ['GET'])
def greetCropScale():
    return "This endpoint is for cropping a face out of a picture and scaling it to size"

@app.route('/cropScale', methods = ["POST"])
def cropScale():
    print "Request recieved at cropScale\n"

    print "Loading location data..."
    x = int(request.form['x'])
    y = int(request.form['y'])
    w = int(request.form['w'])
    h = int(request.form['h'])
    print "Success!\n"
    
    print "Loading file..."
    sentFile = request.files['image'].read()
    npData = np.fromstring(sentFile, dtype = 'uint8')
    image = cv2.imdecode(npData, cv2.IMREAD_UNCHANGED)
    print "Success!\n"
    
    print "Processing image..."
    processedImage = iManip.cropScaleImage(image, x, y, w, h)
    print "Success!\n"

    print "Encoding response..."
    flag, buf = cv2.imencode('return.jpg', processedImage, [cv2.IMWRITE_JPEG_QUALITY, 90])
    print "Success!\n"

    return buf.tobytes()
