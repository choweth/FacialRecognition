import ImgManipulation as iManip

def calc(image):
    meanFace = cv2.imread(os.getcwd +"/Data/MeanFace/meanFace.jpg")
    diffFace = iManip.differenceFace(image, meanFace)
    #TODO: Store the difference vector

    return diffFace
