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
    
    def compare(compFace):
        epsSquared = abs(faceSpaceProj - compFace.faceSpaceProj)^2
        return epsSquared < comparisonThreshold

    def initDiff(self, meanFace):
        self.diffFace = iManip.differenceFace(self.grayFace, meanFace)
        cv2.imwrite("Data/DifferenceFaces/DifferenceFace_" + str(self.ID) +  ".jpg", self.diffFace)
        self.diffVec = iManip.imageToVector(self.diffFace)
        
    def initEigenFace(self, eVec):
        self.eigenVec = eVec
        self.eigenFace = iManip.vectorToImage(iManip.scaleVals(eVec))
        cv2.imwrite("Data/EigenFaces/EigenFace_" + str(self.ID) +  ".jpg", self.eigenFace)

    def initProjections(self, faceSpace):
        self.faceSpaceProj = numpy.matmul(faceSpace,self.diffVec)
        print faceSpaceProj.shape    

    def isFace(faceSpace):
        grayProj = numpy.matmul(numpy.matmul(faceSpace,faceSpace.transpose), grayFace)
        epsSquared = abs(grayFace - grayProj)^2
        return epsSquared < comparisonThreshold

