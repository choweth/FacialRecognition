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
        self.diffVec = iManip.imageToVector(self.diffFace)
    
    # Initializes the eigenFace and eigenVector
    def initEigenFace(self, eVec):
        self.eigenVec = eVec
        self.eigenFace = iManip.vectorToImage(iManip.scaleVals(eVec))

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
