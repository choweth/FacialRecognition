from app import app
from flask import request
import requests
import Extractor

@app.route('/faceExtractor', methods = ['POST'])
def extractFace():
    buf = request.files['image'].read()
    x = np.fromstring(buf, dtype = 'uint8')
    image = cv2.imdecode(x, cv2.IMREAD_UNCHANGED)

    faces = Extractor.extractFaces(image, Extractor.detectFaces(image))

    return faces