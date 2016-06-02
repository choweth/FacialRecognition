from flask import Flask

app = Flask(__name__)
from app import home
from app import faceDetector
from app import meanFaceCalculator
