import os
import sys
sys.path.insert(0, os.getcwd()+"\..\src")

from app import app
from flask import request
import Database
import cv2

@app.route('/CompareToPeople', methods = ['GET'])
def atCompareToPeople():
    return "This endpoint will compare a given image to the mean face of all the people"

@app.route('/CompareToPeople', methods = ['POST'])
def compareToPeople():
    ID = request.form['id']

    grayFace = Database.Database.getGrayFace(ID)

    with open(os.getcwd() + "/Data/num.txt", 'r') as f:
        numPeople = int(f.readline())

    faces = [0 for i in range(numPeople)]

    for i in range(numPeople):
        faces[i] = cv2.imread("../Data/MeanFace/" + str(i) + ".jpg")

    netMeanFace = Database.Database.getNetMeanFace()
    diffFace = Database.Database.getDiffFace(ID)
    
    thing = findBestMatch(diffFace, faces)

    return 'gj'