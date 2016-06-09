import os
import sys
sys.path.insert(0, os.getcwd()+"\..\src")

from app import app
from flask import request
import requests
import Person
import Database
import shlex

@app.route('/MakePerson', methods = ['GET'])
def atMakePerson():
    return "This page makes a Person object"

@app.route('/MakePerson', methods = ['POST'])
def atmakeperson():
    string = request.form['imgs']
    a = shlex.split(string)
    imgs = []
    for i in a:
        imgs.append(int(i))
    faces = []
    print imgs
    for image in imgs:
        r = requests.post('https://localhost/FaceExtractor', files = {'image': open(os.getcwd()+"/Data/raw_images/IMG_" + str(image) + ".jpg",'rb').read()})
        faces.append(r.content['faces'])
    print faces
    ids = [0 for i in range(len(faces))]
    i = 0
    for face in faces:
        r = requests.post('http://localhost/FaceProcessor', files = {'image': face})
        ids[i] = r.content
        i += 1

    person = Database.Database.makePerson(ids)

    return person.identifier
