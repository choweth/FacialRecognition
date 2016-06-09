import numpy
import math
import cv2
import ImgManipulation as iManip
import traceback
import DetectObject as DO
import random
import Face
import os

class Person:
    # A class to contain anything a person may need to keep track of

    ##the constructor, accepts a list of images of the person, some identifying tag,
    ##and an optional name.
    def __init__(self, identification, name = "P.L. Faccio", imgs = []):
        ##Jed's refactored code to work with database:
        self.name = str(name)
        self.email = str(self.name) + "@fullcontact.com"
        print self.name
        self.identifier = identification
        self.faces = len(imgs)
        self.faceIDs = imgs

        if self.faces != 0:
            self.initMeanFace()
        
    def initMeanFace(self):

        ##Jed's code to work with databases
        faces = []
        for id in self.faceIDs:
            faces.append(cv2.imread(os.getcwd()+"/Data/GrayFaces/" + str(id) + ".jpg"))
        meanFace = iManip.averageImgArr(faces)
        cv2.imwrite("Data/MeanFace/" + str(self.identifier) + ".jpg", meanFace)

    def setWeights(weights):
        self.weights = weights

    def getWeights():
        return self.weights