from app import app
from flask import request
import requests
import Encryption
import Extractor

@app.route('/WhoAmI', methods = ['GET'])
def atWhoAmI():
    return "Send me a picture and I'll tell you who's in it!"

@app.route('/WhoAmI', methods = ['POST'])
def whoAmI():
    image = Encryption.decode(request.files['image'])
    #r = requests.post('http://localhost/FaceExtractor', files = request.files)
    faces = Extractor.extractFaces(image, Extractor.detectFaces(image))

    ids = [0 for i in range(len(faces))]
    i = 0
    for face in faces:
        #r = requests.post('http://localhost/FaceProcessor', files = {'image': face})
        grayFace = iManip.grayFace(image)

        diffFace = CalcDiffFace.calc(grayFace)
        diffFace = iManip.imageToVector(diffFace)

        ids[i] = Database.Database.storeFace(grayFace, image, diffFace)
        i += 1
        
    return 'gj'