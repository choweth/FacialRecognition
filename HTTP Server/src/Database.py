import Person, Face
import json
import cv2

class Database:
    currentPerson = Person.Person(0,0)

    @staticmethod
    def getPerson(id):
        with open("/root/know-that-face/know-that-face/HTTP Server/Data/People/" + str(id) + ".txt", 'r') as f:
            currentPerson = json.load(f)
        return currentPerson

    @staticmethod
    def getFace(id):
        face = cv2.imread("C:/Users/Jed/Desktop/know-that-face/HTTP Server/Data/OriginalFaces/" + str(id) + ".jpg")
        #face = cv2.imread("/root/know-that-face/know-that-face/HTTP Server/Data/OriginalFaces/" + str(id) + ".jpg")
        return face

    @staticmethod
    def storePerson(person, id):
        with open("C:/Users/Jed/Desktop/know-that-face/HTTP Server/Data/People/" + str(id) + ".txt", 'w') as f:
        #with open("/root/know-that-face/know-that-face/HTTP Server/Data/People/" + str(id) + ".txt", 'w') as f:
            json.dump(person, f)

    @staticmethod
    def storeOriginalFace(face, ID):
        path = "/root/know-that-face/know-that-face/HTTP Server/Data/OriginalFaces/"
        path = path + str(ID) + ".jpg"
        cv2.imwrite(path, face)
    @staticmethod
    def storeGrayFace(face, ID):
        path = "/root/know-that-face/know-that-face/HTTP Server/Data/GrayFaces/"
        path = path + str(ID) + ".jpg"
        cv2.imwrite(path, face)
    @staticmethod
    def storeFace(grayFace, originalFace):
        with open("/root/know-that-face/know-that-face/HTTP Server/Data/num.txt",'r') as f:
            ID = int(f.readline())
            f.clsoe()
        with open("/root/know-that-face/know-that-face/HTTP Server/Data/num.txt",'w') as f:
            f.write(str(ID+1))
            f.close()
        storeOriginalFace(originalFace, ID)
        storeGrayFace(grayFace, ID)
        
