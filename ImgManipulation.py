import numpy
import cv2

HEIGHT = 600     # Height of stored face images
WIDTH = 500      # Width of stored face images
DEPTH = 3        # Depth of stored face images (RGB values)

# Crops out a face, and scales the face to 600x500
def cropScaleImage(img, x, y, w, h):
    #Crops out the face given the coordinates and width and height of the face
    newImage = img[y:y+h, x:x+w]

    # Uses the INTER_AREA method to scale down
    if (h > HEIGHT):
        newerImage = cv2.resize(newImage,(WIDTH, HEIGHT), interpolation = cv2.INTER_AREA)

    # Uses the INTER_CUBIC method to scale up
    else:
        newerImage = cv2.resize(newImage,(WIDTH, HEIGHT), interpolation = cv2.INTER_CUBIC)

    return newerImage

# Rotates image based on angle passed in
def rotateImage(img, angle):
    rows, cols = img.shape[:2]
    M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
    rotatedImage = cv2.warpAffine(img, M, (cols,rows))
    return rotatedImage

# Takes an image and resizes to no greater than 1280 in the largest direction
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

# Creates a 1x(HEIGHT*WIDTH) vector with the greyscale value stored
def imageToVector(img):
    l = []
    for i in range(HEIGHT):
        for j in range(WIDTH):
            l.append(img[i,j,0])
    return l

# Deconstructs a imageVector into a HEIGHTxWIDTHxDEPTH array
def vectorToImage(vec):
    l = numpy.empty((HEIGHT,WIDTH,DEPTH), int)
    for i in range(HEIGHT):
        for j in range(WIDTH):
            for k in range(DEPTH):
                l[i,j,k] = vec[i*len(l[0])+j]
    return l

# Scales each value in the EigenFace between [0,255]
def scaleVals(vec):
    minVal = vec[0]
    maxVal = vec[0]
    for i in range(len(vec)):
        if vec[i] < minVal:
            minVal = vec[i]
        if vec[i] > maxVal:
            maxVal = vec[i]
    for i in range(len(vec)):
        x = 255*((vec[i] - minVal)/(maxVal-minVal))
        vec[i] = x
    return vec

# Averages all the faces to make the meanFace and saves the greyscale face
def averageFaces(faces):
    newPic = numpy.empty((HEIGHT,WIDTH,DEPTH), int)
    for i in range(HEIGHT):
        for j in range(WIDTH):
            avgVal = 0
            for l in range(len(faces)):
                avgVal = avgVal + faces[l].grayFace[i,j,0]
            x = int((avgVal / len(faces)))
            for k in range(DEPTH):
                newPic[i,j,k] = x
    return newPic

def grayFace(img):
    grayPic = numpy.empty((HEIGHT,WIDTH,DEPTH), int)
    avgVal = 0
    for i in range(HEIGHT):
        for j in range(WIDTH):
            y = 0
            avgVal = 0
            for m in range(DEPTH):
                y = y + img[i,j][m]
            avgVal = avgVal + int(y / 3)
            for m in range(DEPTH):
               grayPic[i][j][m] = avgVal
    return grayPic

# Creates the differenceFace (i.e. greyFace - meanFace) 
def differenceFace(origFace, meanFace):
    diffPic = numpy.empty((HEIGHT,WIDTH,DEPTH), dtype='int64')
    for i in range(HEIGHT):
        for j in range(WIDTH):
            try:
                if (origFace[i,j,0] < meanFace[i,j,0]):
                    x = 0
                else:
                    x = origFace[i,j,0] - meanFace[i,j,0]
                for k in range(3):
                    diffPic[i,j,k] = x
            except(IndexError):
                print i, j
                print origFace
                return
    return diffPic

def addToMeanFace(origFace, meanFace, numPeople):
    # diffPic = numpy.empty((HEIGHT,WIDTH,DEPTH), dtype='int64')
    # print meanFace
    for i in range(HEIGHT):
        for j in range(WIDTH):
            for k in range(DEPTH):
                meanFace[i,j,k] = int(((meanFace[i,j,k] * numPeople) + origFace[i,j,k])/(numPeople+1))
    # print meanFace
    return meanFace

def averageImgArr(faces):
    newPic = numpy.empty((HEIGHT,WIDTH,DEPTH), int)
    for i in range(HEIGHT):
        for j in range(WIDTH):
            avgVal = 0
            for l in range(len(faces)):
                avgVal = avgVal + faces[l][i,j,0]
            x = int((avgVal / len(faces)))
            for k in range(DEPTH):
                newPic[i,j,k] = x
    return newPic
