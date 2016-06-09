import os
import sys
sys.path.insert(0, os.getcwd()+"\..\src")

from app import app
from flask import request
import Database
import cv2
import ImgManipulation as iManip

@app.route('/CompareToPeople', methods = ['GET'])
def atCompareToPeople():
    return "This endpoint will compare a given image to the mean face of all the people"

@app.route('/CompareToPeople', methods = ['POST'])
def compareToPeople(ID = -1):
    
    # If the function is reached via the endpoint, ID will be -1
    # Otherwise, ID will be some integer >= 0
    if (ID == -1):
        ID = request.form['id']

    grayFace = Database.Database.getGrayFace(ID)

    with open(os.getcwd() + "/Data/num.txt", 'r') as f:
        numPeople = int(f.readline())

    weights = [0 for i in range(numPeople)]

    for i in range(numPeople):
        weights[i] = Database.Database.getPerson(i).getWeights()

    netMeanFace = Database.Database.getNetMeanFace()
    diffFace = Database.Database.getDiffFace(ID)
    faceSpace = Database.Database.getFaceSpace()

    theseWeights = iManip.makeProjections(diffFace, faceSpace)

    maxCount = 0
    foundID = 0
    count = 0
    for i in weights:
        temp = iManip.compare(i, theseWeights)
        if (temp > maxCount):
            maxCount = temp
            foundID = count
        count += 1


    return str(foundID)