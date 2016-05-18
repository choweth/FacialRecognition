import unittest
import face_detect
class TestFaces(unittest.TestCase):
    def test_FrontFaces(self):
        self.assertEqual(len(face_detect.findFaces("Images/abba.png")),4)
        self.assertEqual(len(face_detect.findFaces("Images/a.png")),2)
        self.assertEqual(len(face_detect.findFaces("Images/a.jpg")),2)
        self.assertEqual(len(face_detect.findFaces("Images/f.jpg")),2)
        
try:
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFaces)
    unittest.TextTestRunner(verbosity=2).run(suite)
except (IOError):
    print "IOError, exiting"
