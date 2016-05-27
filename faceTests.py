import unittest
import face_detect
import cv2
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
    def test_Eigenstuff(self):
        
        return
try:
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFaces)
    unittest.TextTestRunner(verbosity=2).run(suite)
except (IOError):
    print "IOError, exiting"
