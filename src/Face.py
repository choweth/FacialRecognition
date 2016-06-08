import numpy
import math
import time
import cv2
import ImgManipulation as iManip

class Face:
    # A class to contain anything a face may need to keep track of

    comparisonThreshold = 0.3

    def __init__(self, i, i2 = 0, image = [[[]]], x = -1, y = 0, w = 0, h = 0, name = "null"):
        now = time.time()
        self.ID = i
        if (x == -1):
            self.orig = cv2.imread("Data/OriginalFaces/OriginalFace_" + str(self.ID) + ".jpg")
            self.grayFace = cv2.imread("Data/GrayFaces/GrayFace_" + str(self.ID) + ".jpg")
        else:
            self.orig = iManip.cropScaleImage(image,x,y,w,h)    #The original image
            cv2.imwrite("Data/OriginalFaces/" + str(self.ID) + "_" + str(i2) +  ".jpg", self.orig)
            print "Crop/Scaled one face in:", time.time() - now
            self.grayFace = iManip.grayFace(self.orig)          #The grayscale face
            cv2.imwrite("Data/GrayFaces/" + str(self.ID) + "_" + str(i2) + ".jpg", self.grayFace)       # name + "_" + 
            print "Grayed one face in:", time.time() - now
    
    # Compares the calling face with the given face.
    # Returns the percent similarity
    def compare(self, compFace):
        #epsSquared = 0
        #for i in range(len(self.faceSpaceProj)):
        #    epsSquared += int(self.faceSpaceProj[i] - compFace.faceSpaceProj[i])^2
        epsSquared = numpy.dot(self.faceSpaceProj, compFace.faceSpaceProj)
        epsSquared = epsSquared / (numpy.linalg.norm(self.faceSpaceProj)*numpy.linalg.norm(compFace.faceSpaceProj))
        
        return epsSquared**2

    # Initializes the DifferenceFace and differenceVector
    def initDiff(self, meanFace):
        self.diffFace = iManip.differenceFace(self.grayFace, meanFace)
        cv2.imwrite("Data/DifferenceFaces/DifferenceFace_" + str(self.ID) +  ".jpg", self.diffFace)
        self.diffVec = iManip.imageToVector(self.diffFace)
    
    # Initializes the eigenFace and eigenVector
    def initEigenFace(self, eVec):
        self.eigenVec = eVec
        self.eigenFace = iManip.vectorToImage(iManip.scaleVals(eVec))
        cv2.imwrite("Data/EigenFaces/EigenFace_" + str(self.ID) +  ".jpg", self.eigenFace)

    # Projects the original image onto the faceSpace
    # This is used to compare an eigenface with the original face
    # This can be used to assure the picture even is a face to begin with
    def initProjections(self, faceSpace):
        self.faceSpaceProj = []

        for i in range(int(faceSpace.shape[0])):
            currentNumerator = numpy.dot(self.diffVec, faceSpace[i,:])
            currentDenominator = numpy.dot(faceSpace[i,:], faceSpace[i,:])
            self.faceSpaceProj.append((currentNumerator/currentDenominator))

    # Returns the percent probability that a face image actually contains a face
    #def isFace(self):
        #epsSquared = int(numpy.linalg.norm(self.grayFace[:,:,0].flatten() - self.grayProj)) ^ 2
        #return 1 - epsSquared
