from app import app
from flask import request

@app.route('/test', methods = ['POST'])
def test():
    testData = request.form
    print testData
    return 'gj'