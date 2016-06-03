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
    print "Request recieved"
    sentFile = request.files['image'].read()
    print "File loaded"
    x = int(request.form['x'])
    print x
    print type(x)
    y = int(request.form['y'])
    print y
    w = int(request.form['w'])
    print w
    h = int(request.form['h'])
    print h
    npData = np.fromstring(sentFile, dtype = 'uint8')
    print "Converted from numpy array"
    image = cv2.imdecode(npData, cv2.IMREAD_UNCHANGED)
    print "Decoded image"
    
    processedImage = iManip.cropScaleImage(image, x, y, w, h)
    print "Processed image"
    flag, buf = cv2.imencode('return.jpg', processedImage, [cv2.IMWRITE_JPEG_QUALITY, 90])
    print "Encoded image"
    return buf.tobytes()
