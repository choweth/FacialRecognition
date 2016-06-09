import Person, Face, ImgManipulation as iManip
import jsonpickle
import cv2
import os

class Database:
    currentPerson = Person.Person(0,0)

    @staticmethod
    def getPerson(ID):
        with open(os.getcwd()+"/Data/People/" + str(ID) + ".json", 'r') as f:
            thawed = jsonpickle.decode(f.read())
        return thawed

    @staticmethod
    def getColorFace(ID):
        face = cv2.imread(os.getcwd()+"/Data/OriginalFaces/" + str(ID) + ".jpg")
        return face

    @staticmethod
    def getGrayFace(ID):
        face = cv2.imread(os.getcwd()+"/Data/GrayFaces/" + str(ID) + ".jpg")
        return face

    @staticmethod
    def getDiffFace(ID):
        thawed = []
        with open(os.getcwd()+"/Data/DifferenceFaces/" + str(ID) + ".json", 'r') as f:
            for line in file:
                thawed.append(line)
        return thawed

    @staticmethod
    def getFaceSpace():
        with open(os.getcwd()+"/Data/misc/FaceSpace.json", 'r') as f:
            thawed = jsonpickle.decode(f.read())
        return thawed

    @staticmethod
    def getNetMeanFace():
        return cv2.imread("/Data/MeanFace/meanFace.jpg")



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
        path = path + str(ID) + ".json"
        with open(path, 'w') as f:
            for i in face:
                f.write(str(i) + '\n')
    @staticmethod
    def storeFace(grayFace, originalFace, diffFace):
        with open(os.getcwd()+"/Data/num.txt",'r') as f:
            ID = int(f.readline())
            f.close()
	with open(os.getcwd()+"/Data/num.txt",'w') as f:
            f.write(str(ID+1))
            f.close()
        Database.storeOriginalFace(originalFace, ID)
        Database.storeGrayFace(grayFace, ID)
        Database.storeDiffFace(diffFace, ID)
	print "Stored all faces"
        return ID
        

    ##Generates a facespace based off the list of pictures passed
    @staticmethod
    def makeFaceSpace(faces):
        import numpy
        meanFace = iManip.averageImgArr(faces)
        diffFaces = []
        for face in faces:
            diffFaces.append(iManip.differenceFace(face, meanFace))
        diffVecs = []
        for d in diffFaces:
            diffVecs.append(iManip.imageToVector(d))
        w, faceSpace = numpy.linalg.eig(numpy.dot(diffVecs,zip(*diffVecs)))
        faceSpace = numpy.dot(faceSpace,diffVecs)
        with open(os.getcwd()+"/Data/misc/FaceSpace.json", 'w') as f:
            frozen = jsonpickle.encode(person)
            f.write(frozen)
        return faceSpace, diffVecs

    @staticmethod
    def makePerson(imgs):
        #ID, image ID array
        with open(os.getcwd()+"/Data/People/num.txt",'r') as f:
            ID = int(f.readline())
        with open(os.getcwd()+"/Data/People/num.txt",'w') as f:
            f.write(str(ID+1))

        person = Person.Person(str(ID), imgs = imgs)
        Database.storePerson(person, ID)

        return person
