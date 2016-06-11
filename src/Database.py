import Person
import Face
import ImgManipulation as iManip
import jsonpickle
import cv2
import os
import shlex

class Database:
    currentPerson = Person.Person(0,0)

    @staticmethod
    def getPerson(ID):
        with open(os.getcwd()+"/Data/People/" + str(ID) + ".json", 'r') as f:
            thawed = jsonpickle.decode(f.read())
        return thawed

    @staticmethod
    def getColorFace(ID):
        face = cv2.imread("Data/OriginalFaces/" + str(ID) + ".jpg")
        return face

    @staticmethod
    def getGrayFace(ID):
        face = cv2.imread("Data/GrayFaces/" + str(ID) + ".jpg")
        return face

    @staticmethod
    def getDiffFace(ID):
        thawed = []
        with open(os.getcwd()+"/Data/DifferenceFaces/" + str(ID) + ".txt", 'r') as f:
            for line in file:
                thawed.append(line)
        return thawed

    @staticmethod
    def getFaceSpace():
	faceSpace = []
        with open(os.getcwd()+"/Data/misc/FaceSpace.txt", 'r') as f:
	    for line in f:
		l = shlex.split(line)
		arr = []
		for i in l:
		    arr.append(int(i))
		faceSpace.append(arr)
        return faceSpace

    @staticmethod
    def getNetMeanFace():
        return cv2.imread("Data/MeanFace/meanFace.jpg")

    @staticmethod
    def getMeanFace(ID):
        return(cv2.imread('Data/MeanFace/' + str(ID) + '.jpg'))



    @staticmethod
    def storePerson(person, ID):
        with open(os.getcwd()+"/Data/People/" + str(ID) + ".json", 'w') as f:
            frozen = jsonpickle.encode(person)
            f.write(frozen)
    
    @staticmethod
    def storeOriginalFace(face, ID):
        path = os.getcwd()+"/Data/OriginalFaces/"
        path = path + str(ID) + ".jpg"
        cv2.imwrite(path, face)
    @staticmethod
    def storeGrayFace(face, ID):
        path = os.getcwd()+"/Data/GrayFaces/"
        path = path + str(ID) + ".jpg"
        cv2.imwrite(path, face)
    @staticmethod
    def storeDiffFace(face, ID):
        path = os.getcwd()+"/Data/DifferenceFaces/"
        path = path + str(ID) + ".txt"
        with open(path, 'w') as f:
            for i in face:
                f.write(str(i) + '\n')
    @staticmethod
    def storeFace(grayFace, originalFace):
        with open(os.getcwd()+"/Data/num.txt",'r') as f:
            ID = int(f.readline())
            f.close()
	with open(os.getcwd()+"/Data/num.txt",'w') as f:
            f.write(str(ID+1))
            f.close()
        Database.storeOriginalFace(originalFace, ID)
        Database.storeGrayFace(grayFace, ID)
        # Database.storeDiffFace(diffFace, ID)
        return ID
        

    ##Generates a facespace based off the list of pictures passed
    @staticmethod
    def makeFaceSpace(faces):
        import numpy
        meanFace = Database.getNetMeanFace()
        diffFaces = []

	for face in faces:
            diffFaces.append(iManip.differenceFace(face, meanFace))
        diffVecs = []
        for d in diffFaces:
            diffVecs.append(iManip.imageToVector(d))
        w, faceSpace = numpy.linalg.eig(numpy.dot(diffVecs,zip(*diffVecs)))
        faceSpace = numpy.dot(faceSpace,diffVecs)
        return faceSpace, diffVecs

    @staticmethod
    def makePerson(imgs, name = 'Pants Faccio'):
	# Replaces spaces in names with periods
	name = name.replace(' ', '.')

        #ID, image ID array
        with open(os.getcwd()+"/Data/People/num.txt",'r') as f:
            ID = int(f.readline())
        with open(os.getcwd()+"/Data/People/num.txt",'w') as f:
            f.write(str(ID+1))

        person = Person.Person(str(ID), imgs = imgs, name = name)
        Database.storePerson(person, ID)

        return person

    @staticmethod
    def makeWeights():
        with open(os.getcwd()+"/Data/People/num.txt",'r') as f:
            numPeople = int(f.readline())
        

        netMeanFace = Database.getNetMeanFace()
        faceSpace = Database.getFaceSpace()
        
        for i in range(numPeople):
            thisPerson = Database.getPerson(i)
            thisMeanFace = Database.getMeanFace(i)
            thisDiffVec = iManip.differenceFace(thisMeanFace, netMeanFace)
            theseWeights = iManip.makeProjections(thisDiffVec, faceSpace)
            thisPerson.setWeights(theseWeights)
