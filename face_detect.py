import cv2
import sys
import math
import time
import numpy

def findFaces(image):
# Get user supplied values
    cascPath = "haarcascade_frontalface_default.xml"


    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)

    # Read the image
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

def rotateImage(img, angle):
    rows, cols = img.shape[:2]
    M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
    rotatedImage = cv2.warpAffine(img, M, (cols,rows))
    return rotatedImage

if __name__ =="__main__":
    pic = "Images/c.jpg"
    image = cv2.imread(pic)
    faces = findFaces(image)
    global rotatedImage
    
    # Rotates the image 30 degrees if no faces found
    if (len(faces) == 0):
        print "Rotating 30 counter clockwise..."
        rotatedImage = rotateImage(image, 30)
        faces = findFaces(rotatedImage)
        if (len(faces) != 0): image = rotatedImage

    # Rotates 30 degrees in the opposite direction
    if (len(faces) == 0):
        print "Rotating 30 clockwise..."
        rotatedImage = rotateImage(image, -30)
        faces = findFaces(rotatedImage)
        if (len(faces) != 0): image = rotatedImage

    i=0
    croppedFaces = [None] * len(faces)

    # Crops out and scales each found face
    for (x, y, w, h) in faces:
        croppedFaces[i] = cropScaleImage(image, x, y, w, h)
        i += 1

    # Draws a rectangle around each found face
    for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y-int(h*0.1)), (x+w, int(y+h*1.1)), (0, 255, 0), 2)

    # Writes each cropped face to its own file
    i = 0
    for img in croppedFaces:
        cv2.imwrite("Output/Output_" + str(i) +  ".jpg", img)
        i += 1

    print "Found {0} faces!".format(len(faces))
    cv2.imshow("Faces found", image)
    cv2.imwrite("Output/Output.jpg", image)
    cv2.waitKey(0)
