import cv2
import numpy


def findObject(image,thingToDetect): #Takes in a picture and a key word, if he keyword is
    #recognised, it will use the appropriate cascade file, and if it is not recognised, it
    #will try to use the input as a filepath to a coascade classifier.
    if (thingToDetect == "Eyes"):
        cascPath = "Resource files/eye_cascade.xml"
    elif (thingToDetect == "Left Eye"):
        cascPath = "Resource files/left_eye_cascade.xml"
    elif (thingToDetect ==  "Right Eye"):
        cascPath  = "Resource files/right_eye_cascade.xml"
    elif (thingToDetect == "Face"):
        cascPath = "Resource files/haarcascade_frontalface_default.xml"
    else:
        cascPath = thingToDetect


    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)
    #convert it to greyscale so the Haar cascade can use it 
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Detect things in the image
    things = faceCascade.detectMultiScale(
        gray, #The picture
        scaleFactor=1.1, #The method runs through the same piture multiple time, each time
        #reducing the size by the scale factor, this allows it to detect objects both close up and far
        #away. the closer scale facter is to 1, the longer it will take
        minNeighbors=25,
        #this is the minimum number of time the cascade has to recognize the object before it will accept it
        #increasing this number will remove excess false posatives
        minSize=(50, 50), #minimum size of crop region
        flags = 0
        )
    return things#returns a list of x, y, width and height that form a box around each point that it recognised as an object


#Everything below this is from before the refactor, it is all made obsoleate by the findObteft method,
#But we are going too keep it around incase its useful later.
def findEyes(image):
    cascPath = "eye_cascade.xml"
    eyeCascade = cv2.CascadeClassifier(cascPath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Detect eyes in the image
    eyes = eyeCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=30,
        minSize=(50, 50), #size of crop region
        flags = 0
    )
    return eyes

def findLeftEye(image):
    cascPath = "left_eye_cascade.xml"
    eyeCascade = cv2.CascadeClassifier(cascPath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Detect eyes in the image
    eyes = eyeCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=80,
        minSize=(50, 50), #size of crop region
        flags = 0
    )
    return eyes

def findRightEye(image):
    cascPath = "right_eye_cascade.xml"
    eyeCascade = cv2.CascadeClassifier(cascPath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Detect eyes in the image
    eyes = eyeCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=80,
        minSize=(50, 50), #size of crop region
        flags = 0
    )
    return eyes

def findFaces(image):
    #Pull in the Haar Cascade
    cascPath = "haarcascade_frontalface_default.xml"
    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)
    #convert it to greyscale so the Haar cascade can use it 
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray, #The picture
        scaleFactor=1.1, #The method runs through the same piture multiple time, each time
        #reducing the size by the scale factor, thos allows it to detect faces both close up and far
        #away. the closer scale facter is to 1, the longer it will take
        minNeighbors=30,
        minSize=(50, 50), #size of crop region
        flags = 0
    )
    return faces
