import os
import sys
sys.path.insert(0, os.getcwd()+"\..\src")

from app import app
from flask import request
import requests
import Person
import Database

@app.route('MakePerson', methods = ['GET'])
def atMakePerson():
    return "This page makes a Person object"

@app.route('makeperson', methods = ['post'])
def atmakeperson():
    
    imgs = request.form['imgs']
    #raw_images = [0 for i in range(len(imgs))]
    #i = 0
    #for img in imgs:
    #    raw_images[i] = cv2.imread(os.getcwd+"/Data/raw_images/IMG_" + str(img) + ".jpg")
    #    i += 1
    faces = []
    for image in imgs:
        r = requests.post('https://localhost/FaceExtractor', files = {'image': open(os.getcwd+"/Data/raw_images/IMG_" + str(img) + ".jpg",'rb').read()})
        faces.append(r.content['faces'])

    ids = [0 for i in range(len(faces))]
    i = 0
    for face in faces:
        r = requests.post('http://localhost/FaceProcessor', files = {'image': face})
        ids[i] = r.content
        i += 1

    person = Database.Database.makePerson(ids)

    return person.identifier
