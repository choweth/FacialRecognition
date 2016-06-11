import sys
import os
sys.path.insert(0,os.getcwd()+'/../src')

import Database
import cv2
import ImgManipulation as iManip
import Person

with open('Data/People/num.txt', 'r') as f:
    numPeople = int(f.readline())

meanFaces = []
people = []
for i in range(numPeople):
    person = Database.Database.getPerson(i)
    if person.faces >0:
	meanFaces.append(Database.Database.getMeanFace(i))
	people.append(person)
    print "Loaded person " + str(i)

faceSpace, diffVecs = Database.Database.makeFaceSpace(meanFaces)
print "calculated the faceSpace"

with open("Data/misc/FaceSpace.txt", 'w') as f:
    for i in range(len(faceSpace)):
	for j in range(len(faceSpace[i])):
	    f.write(str(faceSpace[i][j]) + ' ')
	f.write('\n')    
print "Wrote the faceSpace to file"	

for i in range(len(people)):
    projections = iManip.makeProjections(diffVecs[i], faceSpace)
    people[i].setWeights(projections)
    Database.Database.storePerson(people[i], people[i].identifier)
    print "Updated person " + str(i)
