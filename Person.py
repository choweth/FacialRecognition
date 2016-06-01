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
    def __init__(self, imgs, identification , name = "P.L. Faccia"):
        self.images = []
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
        rand = random.randint(0,100000000) ##assigns a random variable to the id for each face
        for i in self.images:
            boxes = DO.findObject(i,"Face")
            try:##this raises an exception if more than one face was found in the picture
                if( len(boxes)!=1):
                    raise Exception(self.name + "'s picture (ID: " +self.identifier+") doesn't contain only one person:")
                
                for (x,y,w,h) in boxes:
                    faces.append(Face.Face(rand,i,x,y,w,h))
            except Exception as e:
                print traceback.print_exc(e)
                print e
        
        c = iManip.averageFaces(faces)
        self.meanFace = c
        
