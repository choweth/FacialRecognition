import numpy
import math
class Face:
    # A class to contain anything a face may need to keep track of

    comparisonThreshold = 0.3

    def __init__(self):
        self.orig            #The original image
        self.diffFace        #The difference face
        self.grayFace        #The grayscale face
        self.diffVec         #The difference vector
        self.eigenFace       #The eigenface
        self.faceSpaceProj   #The projection onto the facespace
    
    def compare(compFace):
        epsSquared = abs(faceSpaceProj - compFace.faceSpaceProj) ^ 2
        return 1 - epsSquared

    def isFace(faceSpace):
        grayProj = numpy.matmul(numpy.matmul(faceSpace,faceSpace.transpose), grayFace)
        epsSquared = abs(grayFace - grayProj) ^ 2
        return 1 - epsSquared