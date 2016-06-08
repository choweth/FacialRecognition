import Person, Face, ImgManipulation as iManip
import jsonpickle
import cv2
import os

class Database:
    currentPerson = Person.Person(0,0)

    @staticmethod
    def getPerson(id):
        with open(os.getcwd()+"/HTTP Server/Data/People/" + str(id) + ".json", 'r') as f:
            thawed = jsonpickle.decode(f.read())
        return thawed

    @staticmethod
    def getColorFace(id):
        face = cv2.imread(os.getcwd()+"/HTTP Server/Data/OriginalFaces/" + str(id) + ".jpg")
        return face

    @staticmethod
    def getGrayFace(id):
        face = cv2.imread(os.getcwd()+"/HTTP Server/Data/GrayFaces/" + str(id) + ".jpg")
        return face

    @staticmethod
    def getDiffFace(id):
        with open(os.getcwd()+"/HTTP Server/Data/DifferenceFaces/" + str(id) + ".json", 'r') as f:
            thawed = jsonpickle.decode(f.read())
        return thawed

    @staticmethod
    def getFaceSpace():
        with open(os.getcwd()+"/HTTP Server/Data/misc/FaceSpace.json", 'r') as f:
            thawed = jsonpickle.decode(f.read())
        return thawed



    @staticmethod
    def storePerson(person, id):
        with open(os.getcwd()+"/HTTP Server/Data/People/" + str(id) + ".json", 'w') as f:
            frozen = jsonpickle.encode(person)
            f.write(frozen)
    
    @staticmethod
    def storeOriginalFace(face, ID):
        path = os.getcwd()+"/HTTP Server/Data/OriginalFaces/"
        path = path + str(ID) + ".jpg"
        cv2.imwrite(path, face)
    @staticmethod
    def storeGrayFace(face, ID):
        path = os.getcwd()+"/HTTP Server/Data/GrayFaces/"
        path = path + str(ID) + ".jpg"
        cv2.imwrite(path, face)
    @staticmethod
    def storeDiffFace(face, ID):
        path = os.getcwd()+"/HTTP Server/Data/DifferenceFaces/"
        path = path + str(ID) + ".jpg"
        cv2.imwrite(path, face)
    @staticmethod
    def storeFace(grayFace, originalFace, diffFace):
        with open(os.getcwd()+"/HTTP Server/Data/num.txt",'r') as f:
            ID = int(f.readline())
            f.close()
        with open(os.getcwd()+"/HTTP Server/Data/num.txt",'w') as f:
            f.write(str(ID+1))
            f.close()
        Database.storeOriginalFace(originalFace, ID)
        Database.storeGrayFace(grayFace, ID)
        Database.storeDiffFace(diffFace, ID)
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
        with open(os.getcwd()+"/HTTP Server/Data/misc/FaceSpace.json", 'w') as f:
            frozen = jsonpickle.encode(person)
            f.write(frozen)
        return faceSpace, diffVecs

    @staticmethod
    def makePerson(imgs):
        #id, image id array
        with open(os.getcwd()+"/HTTP Server/Data/People/num.txt",'r') as f:
            ID = int(f.readline())
        with open(os.getcwd()+"/HTTP Server/Data/People/num.txt",'w') as f:
            f.write(str(ID+1))

        person = Person.Person(str(ID), imgs = imgs)
        Database.storePerson(person, id)

        return person