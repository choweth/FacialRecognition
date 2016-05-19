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
    #now = time.time()
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=10,
        minSize=(50, 50), #size of crop region
        flags = 0
    )
    #print time.time() - now
    #print "Found {0} faces!".format(len(faces))

    # Draw a rectangle around the faces
    #for (x, y, w, h) in faces:
    #    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

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

def imageToVector(img):
    l = []
    for i in range(0, 599):
        for j in range(0, 499):
            l.append(img[i,j])

def averageFaces(faces):
    newPic = numpy.empty((600,500,3), int)
    avgVal = 0
    print len(newPic[0,0])
    for i in range(600):
        for j in range(500):
            for l in range(len(faces)):
                avgVal = avgVal + faces[l][i,j][0]
            x = int((avgVal / len(faces)))
            for k in range(3):
                newPic[i,j,k] = x
            avgVal = 0
    return newPic

if __name__ =="__main__":
    pic = "Images/abba.png"

    faces = findFaces(pic)
    image = cv2.imread(pic)

    i=0
    newFaces = [None] * len(faces)

    for (x, y, w, h) in faces:
        newFaces[i] = cropScaleImage(image, x, y, w, h)
        i += 1

    meanFace = averageFaces(newFaces)
    print meanFace
    cv2.imshow("Mean Face", meanFace)
    cv2.imwrite("Output/mf_Output.jpg", meanFace)

    for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y-int(h*0.1)), (x+w, int(y+h*1.1)), (0, 255, 0), 2)

    i = 0
    for img in newFaces:
        cv2.imwrite("Output/Output_" + str(i) +  ".jpg", img)
        i += 1

    # print image
    print "Found {0} faces!".format(len(faces))
    cv2.imshow("Faces found", image)
    cv2.imwrite("Output/Output.jpg", image)
    cv2.waitKey(0)
