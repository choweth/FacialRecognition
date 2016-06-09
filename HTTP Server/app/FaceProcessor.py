import sys
import os
sys.path.insert(0, os.getcwd()+"\..\src")

from app import app
from flask import request
import Database
import CalcDiffFace
import ImgManipulation as iManip
import Encryption

@app.route('/FaceProcessor', methods = ['GET'])
def atFaceProcessor():
    return "This page takes in a face, calculates the relevant data for it (such as the grayface), and stores it."

@app.route('/FaceProcessor', methods = ['POST'])
def faceProcessor():
    print "Processing a new face"
    image = Encryption.decode(request.files['image'])

    grayFace = iManip.grayFace(image)

    diffFace = CalcDiffFace.calc(grayFace)
    diffFace = iManip.imageToVector(diffFace)

    id = Database.Database.storeFace(grayFace, image, diffFace)
    
    return str(id)
