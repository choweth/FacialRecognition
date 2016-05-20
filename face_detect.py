import cv2
import sys
import math
import time
import numpy

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
# Get user supplied values
    cascPath = "haarcascade_frontalface_default.xml"
    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)

    # Read the image
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

def rotateImage(img, angle):
    rows, cols = img.shape[:2]
    M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
    rotatedImage = cv2.warpAffine(img, M, (cols,rows))
    return rotatedImage

def compressImage(img, bound):
    rows, cols = img.shape[:2]
    rows = int(rows)
    cols = int(cols)

    if (rows > bound and rows >= cols):
        newRow = bound
        newCol = int(cols*(bound/float(rows)))
        img = cv2.resize(img, (newCol, newRow), interpolation = cv2.INTER_AREA)

    elif (cols > bound and rows < cols):
        newCol = bound
        newRow = int(rows*(bound/float(cols)))
        img = cv2.resize(img, (newCol, newRow), interpolation = cv2.INTER_AREA)

    return img

def imageToVector(img):
    l = []
    for i in range(600):
        for j in range(500):
            l.append(img[i,j,0])
    return l

def vectorToImage(vec):
    l = numpy.empty((600,500,3), int)
    for i in range(600):
        for j in range(500):
            for k in range(3):
                l[i,j,k] = vec[i*len(l[0])+j]
    return l

def scale(vec):
    minVal = vec[0]
    maxVal = vec[0]
    for i in range(len(vec)):
        if vec[i] < minVal:
            minVal = vec[i]
        if vec[i] > maxVal:
            maxVal = vec[i]
    print minVal, maxVal
    print vec[0]
    print (vec[0] - minVal), (maxVal-minVal)
    print 255*((vec[0] - minVal)/(maxVal-minVal))
    for i in range(len(vec)):
        x = 255*((vec[i] - minVal)/(maxVal-minVal))
        vec[i] = x
    return vec

def averageFaces(faces):
    newPic = numpy.empty((600,500,3), int)
    grayFaces = numpy.empty((len(faces),600,500,3), int)
    avgVal = 0
    y = 0
    # print len(newPic[0,0])
    for i in range(600):
        for j in range(500):
            for l in range(len(faces)):
                y = 0
                y = y + faces[l][i,j][0]
                y = y + faces[l][i,j][1]
                y = y + faces[l][i,j][2]
                avgVal = avgVal + int(y / 3)
                for m in range(3):
                    grayFaces[l][i][j][m] = avgVal
            x = int((avgVal / len(faces)))
            for k in range(3):
                newPic[i,j,k] = x
            avgVal = 0
    return newPic, grayFaces

if __name__ =="__main__":

    now = time.time()           #start of time counter
    pic = "Images/crowd.jpg"

    image = cv2.imread(pic)
    #Compresses the picture down so the longest side is 1280 pixels. Keeps aspect ratio
    image = compressImage(image, 1280)
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
        # Code to find left or right eyes
        #leftEye = findLeftEye(img)
        #for (x, y, w, h) in leftEye:
        #    cv2.rectangle(img, (x, y-int(h*0.1)), (x+w, int(y+h*1.1)), (255, 0, 0), 2)
        #rightEye = findRightEye(img)
        #for (x, y, w, h) in rightEye:
        #    cv2.rectangle(img, (x, y-int(h*0.1)), (x+w, int(y+h*1.1)), (0, 0, 255), 2)

        cv2.imwrite("Output/Output_" + str(i) +  ".jpg", img)
        i += 1

    meanFace, grayFaces = averageFaces(croppedFaces)
    # print meanFace
    # cv2.imshow("Mean Face", meanFace)
    cv2.imwrite("Output/mf_Output.jpg", meanFace)
    diffFace = differenceFace(grayFaces[0], meanFace)
    diffFace2 = differenceFace(grayFaces[1], meanFace)
    cv2.imwrite("Output/df_Output.jpg", diffFace)
    # print cv2.cvtColor(croppedFaces[0], cv2.COLOR_BGR2GRAY)
    diffVec = imageToVector(diffFace)
    diffVec2 = imageToVector(diffFace2)
    
    a = []
    a.append(diffVec)
    a.append(diffVec2)
    w, v = numpy.linalg.eig(numpy.matmul(a,zip(*a)))
    print v
    a = numpy.matmul(v,a)
    ef = a[0]
    print ef
    ef = scale(ef)
    ef = vectorToImage(ef)
    cv2.imwrite("Output/ef_Output.jpg", ef)
    print len(diffVec)
    print len(a[0])

    print "Found {0} faces!".format(len(faces))
    cv2.imshow("Faces found", image)
    cv2.imwrite("Output/Output.jpg", image)
    print time.time() - now                     #prints out time elapsed in program
    cv2.waitKey(0)
