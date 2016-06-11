import sys
import os
sys.path.insert(0, os.getcwd()+'../../src')

from app import app
from flask import request
import Database
import Encryption

@app.route('/DownloadColoredImage', methods = ['GET'])
def atDownloadColoredImage():
    return "Use this endpoint to download the colored version of an image from the server"

@app.route('/DownloadColoredImage', methods = ['POST'])
def downloadColoredImage():
    ID = request.form['id']
    
    image = Database.Database.getColorFace(ID)
    return Encryption.encode(image)
