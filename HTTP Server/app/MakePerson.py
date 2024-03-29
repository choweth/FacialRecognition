import os
import sys
sys.path.insert(0, os.getcwd()+"\..\src")

from app import app
from flask import request
import requests
import Person
import Database
import shlex
import Extractor
import cv2
import ImgManipulation as iManip
import CalcDiffFace

@app.route('/MakePerson', methods = ['GET'])
def atMakePerson():
    return "This page makes a Person object"

@app.route('/MakePerson', methods = ['POST'])
def atmakeperson():
    name = request.form['name']
    print name
    imgs = []
    for key in request.form:
	if key != 'name':
            imgs.append(int(request.form[key]))
    faces = []

    for image in imgs:
        faceImage = cv2.imread(os.getcwd()+"/Data/fullcontact/IMG_" + str(image) + ".JPG")
        foundFaces = Extractor.extractFaces(faceImage, Extractor.detectFaces(faceImage))
        for each in foundFaces:
            faces.append(each)

    ids = [0 for i in range(len(faces))]
    i = 0
    for face in faces:
	grayFace = iManip.grayFace(face)
	#diffFace = CalcDiffFace.calc(grayFace)
	#diffFace = iManip.imageToVector(diffFace)

        ids[i] = Database.Database.storeFace(grayFace, face)
        i += 1
        
    person = Database.Database.makePerson(ids, name = name)

    return person.identifier
