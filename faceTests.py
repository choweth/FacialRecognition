import unittest
import face_detect
import cv2
import numpy
import Face
import ImgManipulation as iManip
import Person
##Some test may export picture for verification, please navigate to
##Data/TestImages to verify their accuracy
class TestFaces(unittest.TestCase):
    def test_FrontFaces(self):
        image = cv2.imread("Images/abba.png")
        self.assertEqual(len(face_detect.DetectObject.findObject(image,"Face")),4)
        image = cv2.imread("Images/a.png")
        self.assertEqual(len(face_detect.DetectObject.findObject(image,"Face")),2)
        image = cv2.imread("Images/a.jpg")
        self.assertEqual(len(face_detect.DetectObject.findObject(image, "Face")),2)
        image = cv2.imread("Images/f.jpg")
        self.assertEqual(len(face_detect.DetectObject.findObject(image, "Face")),2)
        return
    def test_Eigenstuff(self):
        
        self.assertTrue(False)
        return
    def test_PersonClass(self):
        faces = []
        for i in range(0,6): ##reads in some pictures from the file
            faces.append(cv2.imread("Images/Person_test_"+str(i)+".jpg"))
     
        self.assertEqual(6,len(faces))
        pat = Person.Person(faces,10,"Patrick Nichols")
        self.assertEqual(pat.name,"Patrick Nichols")##make sure name and ID number got read in correctly
        self.assertEqual(pat.identifier, 10)
        cv2.imwrite("Data/TestImages/Patricks_Mean_Face_Test.jpg", pat.meanFace)
        ##should I get rid of this part of the test?
        ##It seems like needing human verification is counter productive.
        print "Please go to Data/TestImages to verify the accuracy of the meanface"
        return
    def test_PersonComparison(self):
        self.assertTrue(False)
        return
    def test_averageFaceCalc(self):
        iManip.WIDTH = 2
        iManip.HEIGHT = 3
        newPic1 = numpy.zeros((3,2,3),int)
        ##This block of code is just initializing two arrays that look like this:
        #(1 2 )     (3 0 )
        #(4 5 ) and (5 5 )
        #(6 10)     (2 20)
        for i in range(0,3):
            newPic1[0][0][i] = 1
            newPic1[1][0][i] = 4
            newPic1[2][0][i] = 6
            newPic1[0][1][i] = 2
            newPic1[1][1][i] = 5
            newPic1[2][1][i] = 10
        newPic2 = numpy.zeros((3,2,3),int)
        for i in range(0,3):
            newPic2[0][0][i] = 3
            newPic2[1][0][i] = 5
            newPic2[2][0][i] = 2
            newPic2[0][1][i] = 0
            newPic2[1][1][i] = 5
            newPic2[2][1][i] = 20
        newFace1 = Face.Face(0,newPic1,0,0,2,3)
        newFace2 = Face.Face(0,newPic2,0,0,2,3)
        faces = [newFace1,newFace2]
        #we then run the two faces through the avergae faces code
        result = iManip.averageFaces(faces)
        ##And them we make sure that the result is the average of the pictures
        #(2   1 )
        #(4.5 5 )
        #(4   15)
        for i in range(0,3):
            self.assertEqual(result[0][0][i],2)
            self.assertEqual(result[1][0][i],4.5)##Should the meanface be a double?
            self.assertEqual(result[2][0][i],4)
            self.assertEqual(result[0][1][i],1)
            self.assertEqual(result[1][1][i],5)
            self.assertEqual(result[2][1][i],15)
        return
try:
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFaces)
    unittest.TextTestRunner(verbosity=2).run(suite)
except (IOError):
    print "IOError, exiting"

    #Inversion Of control
    #
