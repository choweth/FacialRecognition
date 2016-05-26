import numpy
import math
import time
import cv2
import ImgManipulation as iManip

class Face:
    # A class to contain anything a face may need to keep track of

    comparisonThreshold = 0.3

    def __init__(self, i, image = [[[]]], x = -1, y = 0, w = 0, h = 0):
        now = time.time()
        self.ID = i
        if (x == -1):
            self.orig = cv2.imread("Data/OriginalFaces/OriginalFace_" + str(self.ID) + ".jpg")
            self.grayFace = cv2.imread("Data/GrayFaces/GrayFace_" + str(self.ID) + ".jpg")
        else:
            self.orig = iManip.cropScaleImage(image,x,y,w,h)    #The original image
            cv2.imwrite("Data/OriginalFaces/OriginalFace_" + str(self.ID) +  ".jpg", self.orig)
            print "Crop/Scaled one face in:", time.time() - now
            self.grayFace = iManip.grayFace(self.orig)          #The grayscale face
            cv2.imwrite("Data/GrayFaces/GrayFace_" + str(self.ID) +  ".jpg", self.grayFace)
            print "Grayed one face in:", time.time() - now
    
    # Compares the calling face with the given face.
    # Returns the percent similarity
    def compare(compFace):
        epsSquared = abs(faceSpaceProj - compFace.faceSpaceProj) ^ 2
        return 1 - epsSquared

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
        self.faceSpaceProj = numpy.matmul(faceSpace,self.diffVec)
        grayProj = numpy.matmul(zip(*faceSpace), numpy.matmul(faceSpace, self.grayFace[:,:,0].flatten()))

    # Returns the percent probability that a face image actually contains a face
    def isFace(self):
        epsSquared = abs(self.grayFace[:,:,0].flatten() - self.grayProj) ^ 2
        return 1 - epsSquared
