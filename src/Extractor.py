import DetectObject
import ImgManipulation as iManip

def detectFaces(image):
    return DetectObject.findObject(image,"Face")
def extractFaces(image, locations):
    faces = []
    for x, y, w, h in locations:
        faces.append(iManip.cropScaleImage(image, x, y, w, h))
    return faces