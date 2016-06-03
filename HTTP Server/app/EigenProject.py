from app import app
from flask import request
import CalcDiffFace

@app.route('/EigenProject', methods = ['POST'])
def EigenProject():
    buf = request.files['image'].read()
    x = np.fromstring(buf, dtype = 'uint8')
    image = cv2.imdecode(x, cv2.IMREAD_UNCHANGED)
    
    diffFace = CalcDiffFace.calc(image)

    #implement eigenWeight code here
    eigenWeights = []

    return eigenWeights