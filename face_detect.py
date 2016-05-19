import cv2
import sys
import math
import time
import numpy

def findFaces(imagePath):
# Get user supplied values
    cascPath = "haarcascade_frontalface_default.xml"
    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)

    # Read the image
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=30,
        minSize=(50, 50), #size of crop region
        flags = 0
    )
    #print time.time() - now
    #print "Found {0} faces!".format(len(faces))

    # Draw a rectangle around the faces
    #cv2.imshow("Faces found", image)
    #cv2.imwrite("Output.jpg", image)
    #cv2.waitKey(0)
    return faces

def cropScaleImage(img, x, y, w, h):
    newImage = img[y:y+h, x:x+w]

    height = 600
    width = 500

    if (h > height):
        newerImage = cv2.resize(newImage,(width, height), interpolation = cv2.INTER_AREA)

    else:
        newerImage = cv2.resize(newImage,(width, height), interpolation = cv2.INTER_CUBIC)

    return newerImage

if __name__ =="__main__":
    pic = "Images/crowd.jpg"

    faces = findFaces(pic)
    image = cv2.imread(pic)

    i=0
    newFaces = [None] * len(faces)

    for (x, y, w, h) in faces:
        newFaces[i] = cropScaleImage(image, x, y, w, h)
        i += 1

    for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y-int(h*0.1)), (x+w, int(y+h*1.1)), (0, 255, 0), 2)

    i = 0
    for img in newFaces:
        cv2.imwrite("Output/Output_" + str(i) +  ".jpg", img)
        i += 1

    print "Found {0} faces!".format(len(faces))
    cv2.imshow("Faces found", image)
    cv2.imwrite("Output/Output.jpg", image)
    cv2.waitKey(0)
