import numpy
import math
import numpy
import ImgManipulation as iManip
import traceback

class Person:
    # A class to contain anything a person may need to keep track of
#    comparisonThreshold = 0.3
    ##the constructor, accepts a list of images of the person, some identifying tag,
    ##and an optional name.
    def __init__(self, images, identification , name = "P.L. Faccia"):
        self.images = []
        try:
            
            for i in images:
                if (type(i) is not 'numpy.ndarray'):
                    raise TypeError("Person must be passed a list of images")
                self.images.append(i)
        except ZeroDivisionError as z:
            print "WHAT?"
            print traceback.print_exc(z)
        except TypeError as t:
            print "A type error was encountered"
        self.identifier = identification
        self.name = name

        
