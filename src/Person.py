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
    def __init__(self, identification, numImgs, name = "P.L. Faccio", imgs = []):
        ##Jed's refactored code to work with database:
        self.name = name
        print self.name
        self.identifier = identification
        self.meanFace = "Data/MeanFace/" + str(self.identifier) + ".jpg"
        self.faces = len(imgs)
        self.faceIDs = imgs

        if self.faces != 0:
            self.initMeanFace()
        
    def initMeanFace(self):

        ##Jed's code to work with databases
        faces = []
        for id in faceIDs:
            faces.append(cv2.imread(os.getcwd()+"/HTTP Server/Data/GrayFaces/" + str(id) + ".jpg"))
        
        #self.meanFace = iManip.averageFaces(faces)
        cv2.imwrite("Data/MeanFace/" + str(self.identifier) + ".jpg", self.meanFace)

        
    ##This might not be necessary, but we're not comfortable deleting it yet
##    def initDiffFace(self, mf):
##        self.differenceFace = iManip.differenceFace(self.meanFace, mf)
##        cv2.imwrite("Data/DifferenceFaces/" + str(self.identifier) + ".jpg", self.differenceFace)
##        self.differenceVec = iManip.imageToVector(self.differenceFace)
##        file = open("Data/DifferenceVectors/" + str(self.identifier) + ".txt", "w")
##        for i in range(len(self.differenceVec)):
##            file.write(str(self.differenceVec[i]) + "\n")
