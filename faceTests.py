import unittest
import face_detect
import cv2
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
        
        return
    def test_PersonClass(self):
        faces = []
        for i in range(0,6):
            faces.append(cv2.imread("Images/Person_test_"+str(i)+".jpg"))
        print str(type(faces[0]))
        self.assertEqual(6,len(faces))
        pat = Person.Person(faces,10,"Patrick Nichols")
        self.assertEqual(pat.name,"Patrick Nichols")
        self.assertEqual(pat.identifier, 10)
        cv2.imwrite("Data/TestImages/Patricks_Mean_Face_Test.jpg", pat.meanFace)
        print "Please go to Data/TestImages to verify the accuracy of the meanface"
        return
        
try:
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFaces)
    unittest.TextTestRunner(verbosity=2).run(suite)
except (IOError):
    print "IOError, exiting"
