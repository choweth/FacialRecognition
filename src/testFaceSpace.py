import Database
import shlex

newFaceSpace = Database.Database.getFaceSpace()

with open("Data/misc/FaceSpace.txt", 'w') as f:
    for i in range(len(newFaceSpace)):
	for j in range(len(newFaceSpace[i])):
	    f.write(str(newFaceSpace[i][j]) + ' ')
	f.write('\n')
