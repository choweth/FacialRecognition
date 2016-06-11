import sys
import os
sys.path.insert(0, os.getcwd()+'../../src')

from app import app
from flask import request
import Database
import Encryption

@app.route('/DownloadMeanFace', methods = ['GET'])
def atDownloadMeanFace():
    return "Use this endpoint to download the mean face of a person from the server"

@app.route('/DownloadMeanFace', methods = ['POST'])
def downloadMeanFace():
    ID = request.form['id']
    person = Database.Database.getPerson(ID)
    if person.faces != 0: 
	image = Database.Database.getMeanFace(ID)
	return Encryption.encode(image)
    else:
	return "There are no faces associated with that person"
