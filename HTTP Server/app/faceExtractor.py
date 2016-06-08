import sys
import os
sys.path.insert(0, os.getcwd()+"\..\src")

from app import app
from flask import request
import requests
import Extractor
import Encryption

@app.route('/FaceExtractor', methods = ['POST'])
def extractFace():
    image = Encryption.decode(files['image'])
    faces = Extractor.extractFaces(image, Extractor.detectFaces(image))

    files = {'faces': faces}

    return files