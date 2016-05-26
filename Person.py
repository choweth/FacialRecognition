import numpy
import math
import numpy
import ImgManipulation as iManip

class Face:
    # A class to contain anything a person may need to keep track of
    comparisonThreshold = 0.3

    def __init__(self, images, identification , name = "P.L. Faccia"):
        for i in images:
            self.images.add
        self.grayFace = iManip.grayFace(self.orig)          #The grayscale face

    # Initializes the DifferenceFace and differenceVector
    def initDiff(self, meanFace):
        self.diffFace = iManip.differenceFace(self.grayFace, meanFace)
        self.diffVec = iManip.imageToVector(self.diffFace)
    
    # Initializes the eigenFace and eigenVector
    def initEigenFace(self, eVec):
        self.eigenVec = eVec
        self.eigenFace = iManip.vectorToImage(iManip.scaleVals(eVec))

    # Projects the original image onto the faceSpace
    # This is used to compare an eigenface with the original face
    # This can be used to assure the picture even is a face to begin with
    def initProjections(self, faceSpace):
        self.faceSpaceProj = numpy.matmul(faceSpace,self.diffVec)
        grayProj = numpy.matmul(numpy.matmul(faceSpace,faceSpace.transpose), grayFace)
        print faceSpaceProj.shape    

    # Returns the percent probability that a face image actually contains a face
    def isFace(faceSpace):
        epsSquared = abs(grayFace - grayProj) ^ 2
        return 1 - epsSquared
