import cv2
import sys
import math
import time
import numpy
import ImgManipulation as iManip
import DetectObject
import Face

if __name__ =="__main__":
   
    now = time.time()           #start of time counter
    pic = "Images/crowd.jpg"

    image = cv2.imread(pic)
    #Compresses the picture down so the longest side is 1280 pixels. Keeps aspect ratio

    image = iManip.compressImage(image, 1280)
    faceLocs = DetectObject.findObject(image,"Face")
    
    global rotatedImage
    
    # Rotates the image 30 degrees if no faces found
    if (len(faceLocs) == 0):
        print "Rotating 30 counter clockwise..."
        
        rotatedImage = iManip.rotateImage(image, 30)
        faceLocs = DetectObject.findObject(rotatedImage,"Face")

        if (len(faceLocs) != 0): image = rotatedImage

    # Rotates 30 degrees in the opposite direction
    if (len(faceLocs) == 0):
        print "Rotating 30 clockwise..."

        rotatedImage = iManip.rotateImage(image, -30)
        faceLocs = DetectObject.findObject(rotatedImage,"Face")

        if (len(faceLocs) != 0): image = rotatedImage

##    # Draws a rectangle around each found face
##    for (x, y, w, h) in faces:
##            cv2.rectangle(image, (x, y-int(h*0.1)), (x+w, int(y+h*1.1)), (0, 255, 0), 2)

    faces = []
    for (x, y, w, h) in faceLocs:
        faces.append(Face.Face(image,x,y,w,h))

    meanFace = iManip.averageFaces(faces)

    for face in faces:
        face.initDiff(meanFace)

    cv2.imwrite("Output/mf_Output.jpg", meanFace)
   
    diffVecs = []
    for l in range(len(faces)):
        diffVecs.append(faces[l].diffVec)

    
    w, faceSpace = numpy.linalg.eig(numpy.matmul(diffVecs,zip(*diffVecs)))

    faceSpace = numpy.matmul(faceSpace,diffVecs)

    
    for i in range(len(faces)):
        faces[i].initEigenFace(faceSpace[i])
        # faces[i].initProjections(faceSpace)


    i = 0
    for face in faces:       
        cv2.imwrite("Output/EigenFace_" + str(i) +  ".jpg", face.eigenFace)
        i += 1

    print "Found {0} faces!".format(len(faceLocs))
##    cv2.imwrite("Output/Output.jpg", image)
    print time.time() - now                     #prints out time elapsed in program
    cv2.waitKey(0)
