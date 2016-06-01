from app import app

@app.route('/faceDetector', methods = ['GET'])
def atFaceDetector():
	return "This page is for finding faces in an image"

@app.route('/faceDetector', methods = ['POST'])
def postFaceDetector():
	# Detect a face
	return "This will detect a face eventualy"
