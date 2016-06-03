import numpy as np
import requests
import cv2
import time

url = 'http://54.86.99.237/'
files = {'image': open("C:\Users\Jed\Desktop\know-that-face\Images/crowd.jpg",'rb').read()}

print "Beginning demo for mean face calculator!\n"
start = time.time()

now = start
print "Finding faces..."
r = requests.post(url+'faceDetector', files=files)
print "Success!"
print "Faces found in " + str(time.time()-now) + " seconds.\n"


locations = np.fromstring(r.content, dtype = 'uint32')
locations = locations.astype('int')
locations = np.reshape(locations, (-1, 4))

now = time.time()
print "Cropping out and scaling faces from the original image...\n"
i = 1
faces = []
for x,y,w,h in locations:
    data = {'x':x, 'y':y, 'w':w, 'h':h}
    print "Face " + str(i) + '...'
    r = requests.post(url+'cropScale', data = data, files = files)
    faces.append(r.content)
    print "Success!\n"
    i += 1
print "All faces processed!"
print "Faces processed in " + str(time.time()-now) + " seconds.\n"

files = {}
for i in range(len(faces)):
    files[str(i)] = faces[i]

now = time.time()
print "Calculating mean face..."
r = requests.post(url+'meanFaceCalculator', files = files)
print "Success!"
print "Mean face calculated in " + str(time.time()-now) + " seconds.\n"

byteString = r.content
npImage = np.fromstring(byteString, dtype = 'uint8')
image = cv2.imdecode(npImage, cv2.IMREAD_UNCHANGED)
cv2.imwrite("C:\Users\Jed\Desktop\know-that-face\Output/ServerOutput.jpg", image)
print "The whole process took " + str(time.time()-start) + " seconds."
print "Image saved to ServerOutput.jpg"
