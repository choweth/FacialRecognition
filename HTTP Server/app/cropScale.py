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
    file = request.files['image'].open()
    x, y, w, h = request.data
    npData = np.fromstring(file, dtype = 'uint8')
    image = cv2.imdecode(npData, cv2.IMREAD_UNCHANGED)
    
    return