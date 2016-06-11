import sys
import os
sys.path.insert(0, os.getcwd()+'../../src')

from app import app
from flask import request
import Database
import Encryption

@app.route('/DownloadNetMeanFace', methods = ['GET'])
def atDownloadNetMeanFace():
    return "Use this endpoint to download the net mean face from the server"

@app.route('/DownloadNetMeanFace', methods = ['POST'])
def downloadNetMeanFace():
    image = Database.Database.getNetMeanFace()
    return Encryption.encode(image)
