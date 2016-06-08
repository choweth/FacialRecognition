### USEFUL CODE SNIPETS THAT WE DON'T WANT TO LOSE ###

# Draws a rectangle around each found face
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y-int(h*0.1)), (x+w, int(y+h*1.1)), (0, 255, 0), 2)

# Writes and image to a file
cv2.imwrite("Output/Output.jpg", image)
