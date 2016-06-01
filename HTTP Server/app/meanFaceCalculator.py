from app import app

@app.route('/meanFaceCalculator', methods = ['GET'])
def atMeanFaceCalc():
	return "This page is for calculating mean faces"

@app.route('/meanFaceCalculator', methods = ['POST'])
def postMeanFaceCalc():
	# Calculate the mean face
	return "This page will calculate the mean face"
