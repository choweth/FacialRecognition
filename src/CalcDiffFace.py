import ImgManipulation as iManip
import os
sys.path.insert(0, os.getcwd()+"\HTTP Server\src")

def calc(image):
    meanFace = cv2.imread(os.getcwd +"/Data/MeanFace/meanFace.jpg")
    diffFace = iManip.differenceFace(image, meanFace)
    #TODO: Store the difference vector

    return diffFace
