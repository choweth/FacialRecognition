import cv2
import sys
import math
import time
import numpy
import DetectObject








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

def differenceFace(origFace, meanFace):
    diffPic = numpy.empty((600,500,3), int)
    for i in range(600):
        for j in range(500):
            try:
                x = origFace[i,j,0] - meanFace[i,j,0]
                for k in range(3):
                    diffPic[i,j,k] = x
            except(IndexError):
                print i, j
                print origFace
                return
    return diffPic

if __name__ =="__main__":

    now = time.time()           #start of time counter
    pic = "Images/crowd.jpg"

    image = cv2.imread(pic)
    #Compresses the picture down so the longest side is 1280 pixels. Keeps aspect ratio
    image = compressImage(image, 1280)
    faces = DetectObject.findObject(image,"Face")
    global rotatedImage
    
    # Rotates the image 30 degrees if no faces found
    if (len(faces) == 0):
        print "Rotating 30 counter clockwise..."
        rotatedImage = rotateImage(image, 30)
        faces = DetectObject.findObject(rotatedImage,"Face")
        if (len(faces) != 0): image = rotatedImage

    # Rotates 30 degrees in the opposite direction
    if (len(faces) == 0):
        print "Rotating 30 clockwise..."
        rotatedImage = rotateImage(image, -30)
        faces = DetectObject.findObject(rotatedImage,"Face")
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


   #    cv2.rectangle(img, (x, y-int(h*0.1)), (x+w, int(y+h*1.1)), (0, 0, 255), 2)
    for img in croppedFaces:       
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
