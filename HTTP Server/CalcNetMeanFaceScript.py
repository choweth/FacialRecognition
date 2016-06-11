import sys
import os
sys.path.insert(0, os.getcwd()+"/../src")

import Database
import ImgManipulation as iManip
import cv2

with open(os.getcwd()+"/Data/People/num.txt", 'r') as f:
    numPeople = int(f.readline())

people = []
for i in range(numPeople):
    people.append(Database.Database.getPerson(i))

meanFaces = []
for person in people:
    if person.faces != 0:
        meanFaces.append(Database.Database.getMeanFace(person.identifier))

netMeanFace = iManip.averageFaces(meanFaces)

cv2.imwrite(os.getcwd()+"/Data/MeanFace/meanFace.jpg", netMeanFace)
