from app import app
from flask import request
import requests

@app.route('/WhoAmI', methods = ['GET'])
def atWhoAmI():
    return "Send me a picture and I'll tell you who's in it!"

@app.route('/WhoAmI', methods = ['POST'])
def whoAmI():
    r = requests.post('http://localhost/FaceExtractor', files = request.files)
    faces = r.content['faces']

    ids = [0 for i in range(len(faces))]
    i = 0
    for face in faces:
        r = requests.post('http://localhost/FaceProcessor', files = {'image': face})
        ids[i] = r.content
        i += 1
        
    return 'gj'