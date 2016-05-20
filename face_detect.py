import cv2
import sys
import math
import time
import numpy
import ImgManipulation as iManip
import DetectObject

if __name__ =="__main__":

    now = time.time()           #start of time counter
    pic = "Images/crowd.jpg"

    image = cv2.imread(pic)
    #Compresses the picture down so the longest side is 1280 pixels. Keeps aspect ratio

    image = iManip.compressImage(image, 1280)
    faces = DetectObject.findObject(image,"Face")
    
    global rotatedImage
    
    # Rotates the image 30 degrees if no faces found
    if (len(faces) == 0):
        print "Rotating 30 counter clockwise..."
        
        rotatedImage = iManip.rotateImage(image, 30)
        faces = DetectObject.findObject(rotatedImage,"Face")

        if (len(faces) != 0): image = rotatedImage

    # Rotates 30 degrees in the opposite direction
    if (len(faces) == 0):
        print "Rotating 30 clockwise..."

        rotatedImage = iManip.rotateImage(image, -30)
        faces = DetectObject.findObject(rotatedImage,"Face")

        if (len(faces) != 0): image = rotatedImage

    i=0
    croppedFaces = [None] * len(faces)

    # Crops out and scales each found face
    for (x, y, w, h) in faces:
        croppedFaces[i] = iManip.cropScaleImage(image, x, y, w, h)
        i += 1

    # Draws a rectangle around each found face
    for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y-int(h*0.1)), (x+w, int(y+h*1.1)), (0, 255, 0), 2)

    # Writes each cropped face to its own file
    i = 0


    # cv2.rectangle(img, (x, y-int(h*0.1)), (x+w, int(y+h*1.1)), (0, 0, 255), 2)
    for img in croppedFaces:       
        cv2.imwrite("Output/Output_" + str(i) +  ".jpg", img)
        i += 1

    meanFace, grayFaces = iManip.averageFaces(croppedFaces)
    
    cv2.imwrite("Output/mf_Output.jpg", meanFace)
    diffFace = iManip.differenceFace(grayFaces[0], meanFace)
    diffFace2 = iManip.differenceFace(grayFaces[1], meanFace)
    cv2.imwrite("Output/df_Output.jpg", diffFace)

    diffVec = iManip.imageToVector(diffFace)
    diffVec2 = iManip.imageToVector(diffFace2)
    
    a = []
    
    a.append(diffVec)
    a.append(diffVec2)
    w, v = numpy.linalg.eig(numpy.matmul(a,zip(*a)))
    
    a = numpy.matmul(v,a)
    ef = a[1]

    ef = iManip.scaleVals(ef)
    ef = iManip.vectorToImage(ef)
    cv2.imwrite("Output/ef_Output.jpg", ef)

    print "Found {0} faces!".format(len(faces))
    cv2.imwrite("Output/Output.jpg", image)
    print time.time() - now                     #prints out time elapsed in program
    cv2.waitKey(0)
