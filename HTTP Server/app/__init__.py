from flask import Flask

app = Flask(__name__)
from app import home
from app import faceExtractor
from app import meanFaceCalculator
from app import MakePerson
from app import FaceProcessor
