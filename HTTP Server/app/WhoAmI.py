from app import app
from flask import request
import requests
import Encryption
import Extractor
import CompareToPeople

@app.route('/WhoAmI', methods = ['GET'])
def atWhoAmI():
    return "Send me a picture and I'll tell you who's in it!"

@app.route('/WhoAmI', methods = ['POST'])
def whoAmI():
    # Reads in the image from the sent file
    image = Encryption.decode(request.files['image'])

    # Finds and extracts the faces in the image
    # Saves any found faces into a list called 'faces'
    faces = Extractor.extractFaces(image, Extractor.detectFaces(image))


    # Processes each found face
    # Calculates and stores the grayscale version of the face,
    # the difference face (how far it is from the average face),
    # and the original face
    # Saves a list of the IDs of the faces found in the image
    ids = [0 for i in range(len(faces))]
    i = 0
    for face in faces:
        grayFace = iManip.grayFace(image)

        diffFace = CalcDiffFace.calc(grayFace)
        diffFace = iManip.imageToVector(diffFace)

        ids[i] = Database.Database.storeFace(grayFace, image, diffFace)
        i += 1

    # mostSimilars gets instantiated as a map so it can be returned in the request
    mostSimilars = {}

    # Creates a list of id's of the most similar person to each given face
    for i in range(len(ids)):
        mostSimilars[i] = CompareToPeople.compareToPeople(ID = i)

    return mostSimilars