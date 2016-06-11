import os
import cv2
import math
import time
import numpy
import ImgManipulation as iManip
import DetectObject
import Person
import Face
import shlex
import Database

##This (In Theory) should run through the full contact faceset and return the pictur that is cl
        ##closest to the original image

def doTheThing():
    compImage = cv2.imread("Data/trial.jpg")
##    face = DetectObject.findObject(compImage,"Face")
##    for (x,y,w,h) in face:
##        compImage = iManip.cropScaleImage(compImage,x,y,w,h)
    compImage = iManip.grayFace(compImage)
    cv2.imwrite("Data/trialResult.jpg",compImage)
    file = open("Data/neededShit.txt", "r")

    for line in file:
        s = line;
        splitarr = shlex.split(s)
        people.append(Person.Person(splitarr[0],splitarr[1],splitarr[2]))
    file.close()
    faces = []
    for i in people:
        faces.append(i.meanFace)
    netMeanFace = cv2.imread("Data/MeanFace/meanFace.jpg")
    diffFace = iManip.differenceFace(compImage, netMeanFace)
    diffVec = iManip.imageToVector(diffFace)
    x = findBestMatch(diffVec,faces)
    
    x = iManip.additionFace(iManip.vectorToImage(x),netMeanFace)
    cv2.imwrite("Data/AHAHAHAHAHAHA.jpg",x)
##this, when given a image of a face and a list of other faces should return
##the face in the list that most resembles the original face
def findBestMatch(originalDiffVec, comparableImages):
    
    faceSpace,diffVecs = makeFaceSpace(comparableImages)
    faceSpace = Database.Database.getFaceSpace


    maxScore = 0
    bestMatch = 0
    projs = []
    original = iManip.makeProjections(originalDiffVec, faceSpace)
    tempcount = 1
    for i in diffVecs:
        w = iManip.makeProjections(i,faceSpace)
        x = iManip.compare(w,original)
        y = iManip.compare(original,w)
        print "Similarity level to face ", tempcount,": ",x
        tempcount +=1
        if (x>maxScore):
            maxScore = x
            bestMatch = i
    
    return bestMatch

##Generates a facespace based off the list of pictures passed
def makeFaceSpace(faces):
    meanFace = iManip.averageImgArr(faces)
    diffFaces = []
    for face in faces:
        diffFaces.append(iManip.differenceFace(face, meanFace))
    diffVecs = []
    for d in diffFaces:
        diffVecs.append(iManip.imageToVector(d))
    w, faceSpace = numpy.linalg.eig(numpy.dot(diffVecs,zip(*diffVecs)))
    # print w
    faceSpace = numpy.dot(faceSpace,diffVecs)
    return faceSpace, diffVecs

 ##returns a list of all the pictures in the given directory
def loadPictures(filePath):
    picList = []
    for i in os.listdir(filePath):
        picList.append(cv2.imread(filePath+i))
    return picList

    
if __name__ =="__main__":
    print "0. Old faces code"
    print "1. More old faces code"
    print "2. Read saved data and make difference faces"
    print "3. Add a new person"
    print "6. Do The Thing!"
    user = raw_input("Please pick an option: ")
    userInt = int(user)
    now = time.time()   #start of time counter
    option = userInt    # 0 for read saved data (faces)
                        # 1 for remake everything (faces)
                        # 2 for read saved data (people) and make difference faces
                        # 3 for remake everything (people)
                        # 4 
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
        
        print "Read/Calculated meanFace in:", time.time() - now

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

        print "The first two faces are " + faces[0].compare(faces[1]) + " percent similar"
        print "The first face is " + faces[0].compare(faces[0]) + " percent similar with itself"

        text_file = open("Data/data.txt", "w")
        # text_file.write("Purchase Amount: %s" % TotalAmount)
        text_file.write(str(len(faces)))
        text_file.close()
        
        print time.time() - now         #prints out time elapsed in program
        cv2.waitKey(0)

    elif (option == 2): # reads in all saved people
        meanFace = cv2.imread("Data/MeanFace/meanFace.jpg")
        file = open("Data/neededShit.txt", "r")
        for line in file:
            s = line
            splitarr = shlex.split(s)
            people.append(Person.Person(splitarr[0],splitarr[1],splitarr[2]))
        file.close()
        for person in people:
            person.initDiffFace(meanFace)

        diffVecs = []
        for l in range(len(people)):
            diffVecs.append(people[l].differenceVec)
        
        w, faceSpace = numpy.linalg.eig(numpy.dot(diffVecs,zip(*diffVecs)))
        
        faceSpace = numpy.dot(faceSpace,diffVecs)

        file = open("Data/FaceSpace.txt", "w")
        for i in range(len(people[0].differenceVec)):
            for j in range(len(people)):
                file.write(str(people[j].differenceVec[i]) + " ")
            file.write("\n")
        
##        file = open("Data/num.txt", "w")
##        file.write(str(len(people)))
##        file.close()

    elif (option == 3):
        pics = []
        # meanFace = numpy.empty((iManip.HEIGHT,iManip.WIDTH,iManip.DEPTH), dtype='int64')
        meanFace = cv2.imread("Data/MeanFace/meanFace.jpg")
        file = open("Data/num.txt", "r")
        n = file.readline()
        n = int(n)
        file.close()
        print n
        x = raw_input("Who is this face: ")
        for i in range(0, 0):    
            pic = "Images/fullcontact/IMG_" + str(i) + ".JPG"
            print i
            image = cv2.imread(pic)
            image = iManip.compressImage(image, 1280)
            pics.append(image)
        p = Person.Person(n,len(pics),x,pics)
        meanFace = iManip.addToMeanFace(p.meanFace,meanFace,n)
        cv2.imwrite("Data/MeanFace/meanFace.jpg",meanFace)
        # p.initDiffFace(meanFace)
        file = open("Data/neededShit.txt", "a")
        file.write(str(p.identifier) + " " + str(len(p.images)) + " " + p.name + "\n")
        file.close()
        file = open("Data/num.txt", "w")
        n += 1
        file.write(str(n))
        file.close()
        # cv2.imwrite("Data/TestImages/Barbra_Mean_Face_Test.jpg", p.meanFace)

    elif (option == 4):
        faces = []
        for i in range(18):
            faces.append(cv2.imread("Data/MeanFace/" + str(i) + ".jpg"))
        mf = iManip.averageImgArr(faces)
        cv2.imwrite("Data/MeanFace/meanFace1.jpg",mf)

        
    elif (option == 5):
        plfaccio = Person.Person(0, 0)
        print "About to store mr pants person"
        Database.Database.storePerson(plfaccio, plfaccio.identifier)
        print '"Probably" stored the person. Maybe.'
        print "About to reload the person."
        newPerson = Database.Database.getPerson(plfaccio.identifier)
        print "'Probably' loaded the person. Maybe."
        if (newPerson == plfaccio):
            print "They're equal!"
        else:
            print "They're not equal..."

        print "The first person is named " + plfaccio.name
        print "The second person is named " + newPerson.name
        print "Done."
    elif (option == 6):
        doTheThing()
