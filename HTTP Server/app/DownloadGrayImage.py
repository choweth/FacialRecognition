import sys
import os
sys.path.insert(0, os.getcwd()+'../../src')

from app import app
from flask import request
import Database
import Encryption

@app.route('/DownloadGrayImage', methods = ['GET'])
def atDownloadGrayImage():
    return "Use this endpoint to download the gray version of an image from the server"

@app.route('/DownloadGrayImage', methods = ['POST'])
def downloadGrayImage():
    ID = request.form['id']
    
    image = Database.Database.getGrayFace(ID)
    return Encryption.encode(image)
