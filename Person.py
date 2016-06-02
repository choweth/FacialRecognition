import numpy
import math
import cv2
import ImgManipulation as iManip
import traceback
import DetectObject as DO
import random
import Face

class Person:
    # A class to contain anything a person may need to keep track of

    ##the constructor, accepts a list of images of the person, some identifying tag,
    ##and an optional name.
    def __init__(self, identification, numImgs, name = "P.L. Faccia", imgs = []):
        if (len(imgs) == 0):
            blah = -1
            print blah
            self.name = name
            self.identifier = identification
            self.meanFace = cv2.imread("Data/MeanFace/" + str(self.identifier) + ".jpg")
        else:
            self.faces = []
            print len(imgs)
            if (len(imgs) == 0):
                for i in range(numImgs):
                    faces.append(Face.Face(self.identifier,numImgs))
            else:
                self.images = []
                self.numImgs = len(self.images)
                try:
                    image = numpy.empty([3,3,3],int)
                    if (type(imgs[0]) is not type(image)):
                        raise TypeError("Person must be passed a list of images, was passed a list of "
                                       +str(type(imgs[0])))
                    self.images = imgs
                except ZeroDivisionError as z:
                    print traceback.print_exc(z)
                    print z
                    print "WHAT? how?"
                except TypeError as t:
                    print traceback.print_exc(t)
                    print t 
                self.identifier = identification
                self.name = name
                self.initMeanFace()
        
    def initMeanFace(self):
        faces = []
        k = 0
        # rand = random.randint(0,100000000) ##assigns a random variable to the id for each face
        for img in self.images:
            boxes = DO.findObject(img,"Face")
            try:##this raises an exception if more than one face was found in the picture
                if( len(boxes)!=1):
                    raise Exception(self.name + "'s picture (ID: " +str(self.identifier)+") doesn't contain only one person:")
                for (x,y,w,h) in boxes:
                    faces.append(Face.Face(self.identifier,k,img,x,y,w,h,self.name))
                    k = k+1
            except Exception as e:
                print traceback.print_exc(e)
                print e
        
        self.meanFace = iManip.averageFaces(faces)
        cv2.imwrite("Data/MeanFace/" + str(self.identifier) + ".jpg", self.meanFace)

    def initDiffFace(self, mf):
        self.differenceFace = iManip.differenceFace(self.meanFace, mf)
        cv2.imwrite("Data/DifferenceFaces/" + str(self.identifier) + ".jpg", self.differenceFace)
