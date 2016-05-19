import cv2
import sys
import time

def findFaces(imagePath):
# Get user supplied values
<<<<<<< HEAD
    cascPath = "haarcascade_frontalface_default.xml"
=======
imagePath = "b.png"
cascPath = "haarcascade_frontalface_default.xml"
>>>>>>> d0ca85bb8aa0557c054f31146fa34f61a138cacb

    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)

    # Read the image
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

<<<<<<< HEAD
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
=======
# Detect faces in the image
now = time.time()
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=10,
    minSize=(50, 50), #size of crop region
    flags = 0
)
print time.time() - now
print "Found {0} faces!".format(len(faces))
>>>>>>> d0ca85bb8aa0557c054f31146fa34f61a138cacb

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    #cv2.imshow("Faces found", image)
    #cv2.imwrite("Output.jpg", image)
    #cv2.waitKey(0)
    return faces
if __name__ =="__main__":
    faces = findFaces("Images/abba.png")
    image = cv2.imread("Images/abba.png")
    for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    print "Found {0} faces!".format(len(faces))
    cv2.imshow("Faces found", image)
    cv2.imwrite("Output.jpg", image)
    cv2.waitKey(0)
