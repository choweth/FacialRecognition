import numpy
import math
import numpy
import ImgManipulation as iManip

class Face:
    # A class to contain anything a face may need to keep track of

    comparisonThreshold = 0.3

    def __init__(self, image, x, y, w, h):
        self.orig = iManip.cropScaleImage(image,x,y,w,h)    #The original image
        self.grayFace = iManip.grayFace(self.orig)          #The grayscale face
    
    def compare(compFace):
        epsSquared = abs(faceSpaceProj - compFace.faceSpaceProj) ^ 2
        return 1 - epsSquared

    def initDiff(self, meanFace):
        self.diffFace = iManip.differenceFace(self.grayFace, meanFace)
        self.diffVec = iManip.imageToVector(self.diffFace)
        
    def initEigenFace(self, eVec):
        self.eigenVec = eVec
        self.eigenFace = iManip.vectorToImage(iManip.scaleVals(eVec))

    def initProjections(self, faceSpace):
        self.faceSpaceProj = numpy.matmul(faceSpace,self.diffVec)
        print faceSpaceProj.shape    

    def isFace(faceSpace):
        grayProj = numpy.matmul(numpy.matmul(faceSpace,faceSpace.transpose), grayFace)
        epsSquared = abs(grayFace - grayProj) ^ 2
        return 1 - epsSquared
