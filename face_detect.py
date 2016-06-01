import cv2
import sys
import math
import time
import numpy
import ImgManipulation as iManip
import DetectObject
import Person
import Face
import shlex


if __name__ =="__main__":
    now = time.time()   #start of time counter
    option = 3  # 0 for read saved data (faces)
                # 1 for remake everything (faces)
                # 2 for read saved data (people)
                # 3 for remake everything (people)
    people = []

    if (option ==0):
        meanFace = cv2.imread("Data/MeanFace/meanFace.jpg")
        text_file = open("Data/data.txt", "r")
        numFaces = int(text_file.readline())
        print type(meanFace)
        faces = []
        diffVecs = []
        for i in range(numFaces):
            faces.append(Face.Face(i))
            faces[i].initDiff(meanFace)
            diffVecs.append(faces[i].diffVec)
        print "Initialized Faces and diffFace/DiffVec in:", time.time() - now
       
        w, faceSpace = numpy.linalg.eig(numpy.dot(diffVecs,zip(*diffVecs)))
        faceSpace = numpy.dot(faceSpace,diffVecs)
        print "Calculated faceSpace in:", time.time() - now
        
        for i in range(len(faces)):
            faces[i].initEigenFace(faceSpace[i])
            # faces[i].initProjections(faceSpace)
        print "Calculated eigenFace/eigenVec in:", time.time() - now
        
        text_file.close()
        
    elif (option == 1):
        pic = "Images/crowd.jpg"


        image = cv2.imread(pic)
        #Compresses the picture down so the longest side is 1280 pixels. Keeps aspect ratio

        image = iManip.compressImage(image, 1280)
        print "Compressed image in:", time.time() - now
        faceLocs = DetectObject.findObject(image,"Face")
        print "Found Faces in:", time.time() - now
        
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

        faces = []
        i = 0
        for (x, y, w, h) in faceLocs:
            faces.append(Face.Face(i,0,image,x,y,w,h))
            cv2.rectangle(image, (x, y-int(h*0.1)), (x+w, int(y+h*1.1)), (0, 255, 0), 2)
            i += 1
        
        print "Created the faces array (original, gray) in:", time.time() - now

        meanFace = iManip.averageFaces(faces)
        # meanFace = cv2.imread("Data/MeanFace/meanFace.jpg")
        
        print "Read meanFace in:", time.time() - now

        for face in faces:
            face.initDiff(meanFace)
        print "Initialized diffFace/DiffVec in:", time.time() - now

        # cv2.imwrite("Data/MeanFace/meanFace.jpg", meanFace)
       
        diffVecs = []
        for l in range(len(faces)):
            diffVecs.append(faces[l].diffVec)
        
        w, faceSpace = numpy.linalg.eig(numpy.dot(diffVecs,zip(*diffVecs)))
        
        faceSpace = numpy.dot(faceSpace,diffVecs)
        print "Calculated faceSpace in:", time.time() - now

        for i in range(len(faces)):
            faces[i].initEigenFace(faceSpace[i])
            # faces[i].initProjections(faceSpace)
        print "Calculated eigenFace/eigenVec in:", time.time() - now
        cv2.imshow("Output/Output.jpg", image)
        print "Found {0} faces!".format(len(faceLocs))

        text_file = open("Data/data.txt", "w")
        # text_file.write("Purchase Amount: %s" % TotalAmount)
        text_file.write(str(len(faces)))
        text_file.close()
        
        print time.time() - now         #prints out time elapsed in program
        cv2.waitKey(0)

    elif (option == 2): # reads in all saved people
        file = open("Data/neededShit.txt", "r")
        for line in file:
            s = line;
            splitarr = shlex.split(s)
            people.append(Person.Person(splitarr[0],splitarr[1],splitarr[2]))
        file.close()
        file = open("Data/num.txt", "w")
        file.write(str(len(people)))
        file.close()

    elif (option == 3):
        pics = []
        file = open("Data/num.txt", "r")
        n = file.readline()
        n = int(n)
        file.close()
        print n
        x = raw_input("Who is this face: ")
        for i in range(7207, 7210):    
            pic = "Images/IMG_" + str(i) + ".JPG"
            image = cv2.imread(pic)
            image = iManip.compressImage(image, 1280)
            pics.append(image)
        p = Person.Person(n,len(pics),x,pics)
        file = open("Data/neededShit.txt", "a")
        file.write(str(p.identifier) + " " + str(len(p.images)) + " " + p.name + "\n")
        file.close()
        file = open("Data/num.txt", "w")
        n += 1
        file.write(str(n))
        file.close()
        # cv2.imwrite("Data/TestImages/Barbra_Mean_Face_Test.jpg", p.meanFace)
