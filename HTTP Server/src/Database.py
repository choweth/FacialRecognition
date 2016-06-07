import Person, Face
import json
import cv2

class Database:
    currentPerson = Person()

    @staticmethod
    def getPerson(id):
        with open("/root/know-that-face/know-that-face/HTTP Server/Data/" + str(id) + "/info.txt", 'r') as f:
            currentPerson = json.load(f)
        return currentPerson

    @staticmethod
    def getFace(id):
        face = cv2.imread("/root/know-that-face/know-that-face/HTTP Server/Data/" + currentPerson.ID + "/face_" + str(id) + ".jpg")
        return face

    @staticmethod
    def storePerson(person, id):
        with open("/root/know-that-face/know-that-face/HTTP Server/Data/" + str(id) + "/info.txt", 'w') as f:
            json.dump(person, f)

    @staticmethod
    def storeFace(face):
        path = "/root/know-that-face/know-that-face/HTTP Server/Data/" + currentPerson.ID + "/face_"
        currentFace = currentPerson.Faces
        path = path + str(currentFace) + ".jpg"
        cv2.imwrite(path, face)